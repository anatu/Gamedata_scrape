# -*- coding: utf-8 -*-
# SCRAPE TARGETS
# Under each game page:
# First Ten Weeks + Annual Summary for Global + USA, Europe, Japan breakouts
# Game name, platform, developer, genre info

import scrapy
import re
import csv
import time
from gamedb.items import VgChartzMetaItem
from gamedb.items import VgChartzSalesItem_10wks
from gamedb.items import VgChartzSalesItem_annual
# import pandas as pd

meta_counter = 0
sales_counter = 0

class VgchartzSpider(scrapy.Spider):
    name = "vgchartz"
    allowed_domains = ["www.vgchartz.com"]
        

    def start_requests(self):
        start_url = "http://www.vgchartz.com/gamedb/?page=1&results=200&name=&platform=&minSales=0&publisher=&genre=&sort=GL"
        yield scrapy.Request(start_url, callback = self.parse, headers = {'User-Agent': 'Mozilla/5.0'})


    def parse(self, response):

        gamelinks = response.xpath("//table[@class='chart']/tr/td/a[contains(@href, '/game/')]/@href").extract()

        for gamelink in gamelinks:
            yield scrapy.Request(gamelink, callback = self.parse_game_summary, headers = {'User-Agent': 'Mozilla/5.0'})

        current_page_number = int(re.search("page=[0-9]+", response.url).group().replace("page=", ""))

        if current_page_number <= 673:
            next_page_number = current_page_number + 1
            next_page_string = "page=" + str(next_page_number)
            next_url = response.url.replace(re.search("page=[0-9]+", response.url).group(), next_page_string)

            yield scrapy.Request(next_url, callback = self.parse, headers = {'User-Agent': 'Mozilla/5.0'})


        
    def parse_game_summary(self, response):


        item = VgChartzMetaItem()

        item["game_name"] = response.xpath("//h1/a/text()").extract()[0]
        item["scrape_time"] = time.strftime("%H:%M:%S, %d/%m/%Y")

        try:
            item["platform"] = response.xpath("//td[text() = 'Platform: ']/a/text()").extract()[0]
        except IndexError:
            item["platform"] = ""

        try:
            item["developer"] = response.xpath("//tr/td[text() = 'Developer: ']/a/text()").extract()[0]
        except IndexError:
            item["developer"] = ""

        try:
            item["genre"] = response.xpath("//tr/td[text() = 'Genre: ']/a/text()").extract()[0]
        except IndexError:
            item["genre"] = ""


        region_urls = response.xpath("//div[@id='tabs']/ul/li/a[not(text()='Comments') and not(text()='Summary')]/@href").extract()

        for region in region_urls:
            yield scrapy.Request(region, callback = self.parse_game_sales, headers = {'User-Agent': 'Mozilla/5.0'})

        yield item

        # global_url = response.xpath("//div[@id='tabs']/ul/li/a[text()='Global']/@href").extract()[0]
        # usa_url = response.xpath("//div[@id='tabs']/ul/li/a[text()='USA']/@href").extract()[0]
        # europe_url = response.xpath("//div[@id='tabs']/ul/li/a[text()='Europe']/@href").extract()[0]
        # uk_url = response.xpath("//div[@id='tabs']/ul/li/a[text()='Europe']/@href").extract()[0]
        # japan_url = response.xpath("//div[@id='tabs']/ul/li/a[text()='Global']/@href").extract()[0] 


    def parse_game_sales(self, response):
        
        sales_item_10wks = VgChartzSalesItem_10wks()
        sales_item_annual = VgChartzSalesItem_annual()


        # first10wks_table_headers = response.xpath("//div[@id='game_table_box' and contains(h2/text(), 'First Ten Weeks')]/table/tr/th/text()").extract()
        # annual_table_headers = response.xpath("//div[@id='game_table_box' and contains(h2/text(), 'Annual Summary')]/table/tr/th/text()").extract()

        first10wks_table_rows = response.xpath("//div[@id='game_table_box' and contains(h2/text(), 'First Ten Weeks')]/table/tr")[1:]
        annual_table_rows = response.xpath("//div[@id='game_table_box' and contains(h2/text(), 'Annual Summary')]/table/tr")[1:]


        for html_row in first10wks_table_rows:
            row = html_row.xpath("child::node()//text()").extract()
            sales_item_10wks["game_name"] = response.xpath("//h1/a/text()").extract()[0]
            sales_item_10wks["region"] = response.xpath("//div[@id='tabs']/ul/li[@class='selected']/a/text()").extract()[0]
            sales_item_10wks["week_ending"] = row[0]
            sales_item_10wks["week"] = row[1]
            sales_item_10wks["weekly"] = row[2]
            sales_item_10wks["change"] = row[3]
            sales_item_10wks["total"] = row[4]
            yield sales_item_10wks

        for html_row in annual_table_rows:
            row = html_row.xpath("child::node()//text()").extract()
            sales_item_annual["game_name"] = response.xpath("//h1/a/text()").extract()[0]
            sales_item_annual["region"] = response.xpath("//div[@id='tabs']/ul/li[@class='selected']/a/text()").extract()[0]
            sales_item_annual["year"] = row[0]
            sales_item_annual["yearly"] = row[1]
            sales_item_annual["change"] = row[2]
            sales_item_annual["total"] = row[3]
            yield sales_item_annual



        # for table_header in table_headers:





















