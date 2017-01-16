# -*- coding: utf-8 -*-
import scrapy
import time
import urllib
import csv
import os 
from gamedb.items import GiantbombItem

items = []
raw_outpath = "C:/users/anatu/desktop/ZZ_Tech/keyscrape/gamedb/giantbomb/outputs/raw/"

class GiantbombSpider(scrapy.Spider):
    name = "giantbomb"
    allowed_domains = ["giantbomb.com"]
    start_urls = ['http://giantbomb.com/games/']

    

    def parse(self, response):

        baseurl = "http://giantbomb.com"

        games = response.xpath("//ul[contains(@class,'editorial  grid')]/li/a/@href").extract()

        for game in games:
            yield scrapy.Request(baseurl + game, callback = self.parse_game_info)   

        nexturl = response.xpath("//li[contains(@class, 'paginate__item skip next')]/a/@href").extract()[0]

        yield scrapy.Request(baseurl + nexturl, callback = self.parse)




    def parse_game_info(self, response):
        raw_filename = response.xpath("//title/text()").extract()[0]
        raw_filename = "".join([c for c in raw_filename if c.isalnum()]).strip()
        
        try:
            with open(raw_outpath + "%s" % (raw_filename) + ".html", 'wb') as rawfile:
                rawfile.write(response.body)
        except IOError:
            None

        # info_elements = response.xpath("//div[contains(@class,'wiki-details') and \
        # (child::h3[text()='Game details'])]/table[contains(@class, 'table')]/tbody/tr/")
        # game_name = info_elements[0].xpath("td/div/span/a/text()").extract()[0]

        game_name = response.xpath("//div[contains(@class,'wiki-details') and \
        (child::h3[text()='Game details'])]/table[contains(@class, 'table')]/tbody/tr/td/div/span/a/text()").extract()[0]

        release_date = response.xpath("//td/div[contains(@data-field, 'release_date')]/text()").extract()[0].strip()

        platforms = response.xpath("//td/div[contains(@data-field, 'platforms')]/a/text()").extract()
        platforms = ','.join(platforms).strip()

        developers = response.xpath("//td/div[contains(@data-field, 'developers')]/a/text()").extract()
        developers = ','.join(developers).strip()

        publishers = response.xpath("//td/div[contains(@data-field, 'publishers')]/a/text()").extract()
        publishers = ','.join(publishers).strip()

        genres = response.xpath("//td/div[contains(@data-field, 'genres')]/a/text()").extract()
        genres = ','.join(genres).strip()

        themes = response.xpath("//td/div[contains(@data-field, 'themes')]/a/text()").extract()
        themes = ','.join(themes).strip()

        franchises = response.xpath("//td/div[contains(@data-field, 'franchises')]/a/text()").extract()
        franchises = ','.join(franchises).strip()


        item = GiantbombItem()

        item["scrape_time"] = time.strftime("%H:%M:%S, %d/%m/%Y")
        item["game_name"] = game_name
        item["release_date"] = release_date
        item["platforms"] = platforms
        item["developers"] = developers
        item["publishers"] = publishers
        item["genres"] = genres
        item["themes"] = themes
        item["franchises"] = franchises

        items.append(item)

        # item = [element.strip().replace("\n", "") for element in item]

        for item in items:
            yield item
        
