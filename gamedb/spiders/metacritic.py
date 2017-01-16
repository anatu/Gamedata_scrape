# -*- coding: utf-8 -*-
import scrapy
import time
import urllib
from gamedb.items import MetaCriticItem
import re


class MetaCriticSpider(scrapy.Spider):

    name = "metacritic"
    allowed_domains = ["metacritic.com"]
    start_urls = (
        'http://www.metacritic.com/browse/games/score/metascore/all/all/filtered?view=detailed&sort=desc',
    )


    # get the urls to specific industries
    def parse(self, response):

        stats = response.xpath("//div[@class = 'module products_module list_product_summaries_module ']//div[@class='wrap product_wrap']")

        # topstats = response.xpath('//div[@class="main_stats"]')
        # morestats = response.xpath('//div[contains(@class, "more_stats")]')



        for stat in stats:

            item = MetaCriticItem() 

            item["game_name"]=stat.xpath('div/div/div/div/h3[@class="product_title"]/a/text()').extract()

            item["metascore"]=stat.xpath('div/div/div/a/span[contains(@class,"metascore_w")]/text()').extract()

            item["release_date"]=stat.xpath('div/div/div[contains(@class, "extended_stats")]/ul/li[contains(@class, "release_date")]/span[@class="data"]/text()').extract()

            item["publisher"]=stat.xpath('div/div/div[contains(@class, "extended_stats")]/ul/li[contains(@class,"publisher")]/span[@class="data"]/text()').extract()

            item["userscore"]=stat.xpath('div/div/div[contains(@class, "extended_stats")]/ul/li[contains(@class,"product_avguserscore")]/span[contains(@class,"textscore") and contains(@class, "data")]/text()').extract()

            item["rating"] = stat.xpath('div/div/div[contains(@class, "extended_stats")]/ul/li[contains(@class, "maturity_rating")]/span[@class="data"]/text()').extract()

            item["platform"] = stat.xpath('div/div/div[contains(@class, "extended_stats")]/ul/li[contains(@class, "platform_list")]/span[@class="data"]/a/text()').extract()

            item["genre"] = stat.xpath('div/div/div[contains(@class, "extended_stats")]/ul/li[contains(@class, "genre")]/span[@class="data"]/text()').extract()

            yield item



        for key, value in item.iteritems():
            item[key] = ''.join(str(c) for c in value).strip()


        baseurl = "http://www.metacritic.com"
        nextpg = response.xpath('//span[contains(@class, "flipper") and contains(@class, "next")]/a/@href').extract()[0]
        nexturl = baseurl + nextpg

        # yield None
        yield scrapy.Request(nexturl, callback = self.parse)

    # get the urls to companies
    # def parse_url(self, response):
    #     # logic to get the urls for each company in the specific industry
    #     baseurl = "http://contracts.onecle.com/"
    #     companies = response.xpath('//div[@class="index"]/ul/li')

    #     for company in companies:
    #         url = company.xpath('a/@href').extract()
    #         yield scrapy.Request(baseurl + url[0], callback=self.parse_company_url)

    # # get the urls to documents
    # def parse_company_url(self, response):
    #     documents = response.xpath('//div[@class="index"]/ul/li')
    #     baseurl = "http://contracts.onecle.com/"


    #     for document in documents:
    #         name = document.xpath('a/text()').extract()
    #         url = document.xpath('a/@href').extract()
    #         url = baseurl + url[0]
    #         filename = re.sub('[\\\/\:\*\?\"\<\>\|\.\,"\&\[\]\-]',r'',name[0])
            
    #         basepath = 'C:/users/anatu/desktop/keyscrape/coke/outputs/.shtml'
    #         baselen = len(basepath)
    #         maxlen = 259 - baselen

    #         if len(filename) > maxlen:
    #             filename = filename[:maxlen]

    #         outfile.write(url + "\n")


    #         # urllib.urlretrieve(url, 'C:/users/anatu/desktop/keyscrape/coke/outputs/%s.shtml' % (filename))
    #         # yield scrapy.Request(baseurl + url[0], callback=self.extract_document)
    #         yield None


    # extract and store the document on disk
    # def extract_document(self, response):
    #     #Extract the dcoument and save to disk

    #     docName = response.xpath('//title/text()').extract()
    #     docContent = response.xpath('//body//text()').extract()

    #     item = CokeItem()
    #     item['document_name'] = docName
    #     item['document_content'] = docContent
    #     yield item




        # for stat in stats:
        #     try:
        #         title=stat.xpath('div/div/div/div/h3[@class="product_title"]/a/text()').extract()
        #         title = [str(c) for c in title]
        #     except IndexError:
        #         title="N/A"
        #     try:
        #         metascore=stat.xpath('div/div/div/a/span[contains(@class,"metascore_w")]/text()').extract()[0]
        #     except IndexError:
        #         metascore="N/A"
        #     try:
        #         rel_date=stat.xpath('div/div/div[contains(@class, "extended_stats")]/ul/li[contains(@class, "release_date")]/span[@class="data"]/text()').extract()[0]
        #     except IndexError:
        #         rel_date="N/A"
        #     try:
        #         publisher=stat.xpath('div/div/div[contains(@class, "extended_stats")]/ul/li[contains(@class,"publisher")]/span[@class="data"]/text()').extract()[0]
        #     except IndexError:
        #         publisher="N/A"
        #     try:
        #         userscore=stat.xpath('div/div/div[contains(@class, "extended_stats")]/ul/li[contains(@class,"product_avguserscore")]/span[contains(@class,"textscore") and contains(@class, "data")]/text()').extract()[0]
        #     except IndexError:
        #         userscore="N/A"
        #     try:
        #         rating = stat.xpath('div/div/div[contains(@class, "extended_stats")]/ul/li[contains(@class, "maturity_rating")]/span[@class="data"]/text()').extract()[0]
        #     except IndexError:
        #         rating = "N/A"
        #     try:
        #         platform = stat.xpath('div/div/div[contains(@class, "extended_stats")]/ul/li[contains(@class, "platform_list")]/span[@class="data"]/a/text()').extract()[0]
        #     except IndexError:
        #         platform = "N/A"
        #     try:
        #         genre = stat.xpath('div/div/div[contains(@class, "extended_stats")]/ul/li[contains(@class, "genre")]/span[@class="data"]/text()').extract()[0].replace(" ","").replace("\n","")
        #     except IndexError:
        #         genre = "N/A"
