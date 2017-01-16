# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class GiantbombItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    scrape_time = Field()
    game_name = Field()
    release_date = Field()
    platforms = Field()
    developers = Field()
    publishers = Field()
    genres = Field()
    themes = Field()
    franchises = Field()
    pass

class IgnItem(Item):
    scrape_time = Field()
    game_name = Field()
    release_date = Field()
    genre = Field()
    publisher = Field()
    developer = Field()
    ign_rating = Field()
    community_rating = Field()  
    community_N = Field()


class VgChartzMetaItem(Item):
    game_name = Field()
    scrape_time = Field()
    platform = Field()
    developer = Field()
    genre = Field()

class VgChartzSalesItem_10wks(Item):
    game_name = Field()
    region = Field()
    week_ending = Field()
    week = Field()
    weekly = Field()
    change = Field()
    total = Field()

class VgChartzSalesItem_annual(Item):
    game_name = Field()
    region = Field()
    year = Field()
    yearly = Field()
    change = Field()
    total = Field()


class MetaCriticItem(Item):
    game_name = Field()
    metascore = Field()
    release_date = Field()
    publisher = Field()
    userscore = Field()
    rating = Field()
    platform = Field()
    genre = Field()

    
