# -*- coding: utf-8 -*-
import scrapy
from gamedb.items import IgnItem
import os
import string
import time
import re

raw_outpath = "C:/users/anatu/desktop/ZZ_Tech/keyscrape/gamedba/ign/outputs/raw/"
base_list = "http://www.ign.com/games?startIndex=0&letter=A"

class IgnSpider(scrapy.Spider):
    name = "ign"
    allowed_domains = ["www.ign.com"]
    # start_urls = ['httsp://www.ign.com/games?startIndex=0?letter=A']

    def start_requests(self):
        yield scrapy.Request(base_list, callback = self.parse, headers = {'User-Agent': 'Mozilla/5.0'})


    def parse(self, response):
        # base_index = 0
        # letter_iterator = 1
        increment = 50
        letters = string.ascii_uppercase

        if response.xpath("//div[@class='itemList']/text()").extract()[0].strip() != "No Results.":

            gamelinks = response.xpath("//div[contains(@class, 'item-title')]/a/@href").extract()

            for gameurl in gamelinks:
                yield scrapy.Request("http://www.ign.com" + gameurl, callback = self.parse_game, headers = {'User-Agent': 'Mozilla/5.0'})

            current_index = int(re.search("startIndex\=[0-9]+", response.url).group().replace("startIndex=", ""))
            next_index = current_index + increment 

            next_index_list = response.url.replace(re.search("startIndex\=[0-9]+", response.url).group(), "startIndex=" + str(next_index))

            yield scrapy.Request(next_index_list, callback = self.parse, headers = {'User-Agent': 'Mozilla/5.0'})

        else:

            current_letter = re.search("letter\=[A-Z]", response.url).group().replace("letter=", "")
            next_letter = letters[letters.find(current_letter) + 1]
            next_letter_list = response.url.replace(re.search("letter\=[A-Z]", response.url).group(), "letter=" + next_letter)
            next_letter_list = next_letter_list.replace(re.search("startIndex\=[0-9]+", next_letter_list).group(), "startIndex=0")
            yield scrapy.Request(next_letter_list, callback = self.parse, headers = {'User-Agent': 'Mozilla/5.0'})



    def parse_game(self, response):

        raw_filename = response.xpath("//title/text()").extract()[0]
        raw_filename = "".join([c for c in raw_filename if c.isalnum()]).strip()
        
        try:
            with open(raw_outpath + "%s" % (raw_filename) + ".html", 'wb') as rawfile:
                rawfile.write(response.body)
        except IOError:
            None

        item = IgnItem()


        item["scrape_time"] = time.strftime("%H:%M:%S, %d/%m/%Y")
        item["game_name"] = response.xpath("//title/text()").extract()[0]


        try:
            item["release_date"] = response.xpath("//div[contains(@class, 'releaseDate')]/strong/text()").extract()[0]
        except IndexError:
            item["release_date"] = ""

        try:
            item["genre"] = response.xpath("//div[@class = 'gameInfo-list']/div[strong/text() = 'Genre']/a/text()").extract()[0]
        except IndexError:
            item["genre"] = ""

        try:
            item["publisher"] = response.xpath("//div[@class = 'gameInfo-list']/div[strong/text() = 'Publisher']/a/text()").extract()[0]
        except IndexError:
            item["publisher"] = ""

        try:
            item["developer"] = response.xpath("//div[@class = 'gameInfo-list']/div[strong/text() = 'Developer']/a/text()").extract()[0]
        except IndexError:
            item["developer"] = ""

        ignrating = response.xpath("//div[@class = 'ratingRows']/div[@class = 'ignRating ratingRow']")

        try:
            item["ign_rating"] = ignrating.xpath("div[@class = 'ratingValue']/text()").extract()[0]
        except IndexError:
            item["ign_rating"] = ""


        commrating = response.xpath("//div[@class = 'ratingRows']/div[@class = 'communityRating ratingRow']")

        try:
            item["community_rating"] = commrating.xpath("div[@class = 'ratingValue']/text()").extract()[0]
            item["community_N"] = commrating.xpath("div[@class = 'ratingCount']/b/text()").extract()[0]
        except IndexError:
            item["community_rating"] = ""
            item["community_N"] = ""

        for key, value in item.items():
            item[key] = value.strip()

        yield item



        # for rating in ratings:
        #   if rating.xpath("div[@class='smallPrint']/text()").extract()[0] == "IGN Rating":
        #       ign_rating = rating.xpath("div[@class='ratingValue']/text()").extract()[0]
        #   if rating.xpath("div[@class='smallPrint']/text()").extract()[0] == "Community":
        #       community_rating = rating.xpath("div[@class='ratingValue']/text()").extract()[0]

