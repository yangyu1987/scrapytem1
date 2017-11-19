# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import pymongo


class BasetempItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #抓取时间
    crawl_time = scrapy.Field()
    # 电影标题
    title = scrapy.Field()
    # 上演时间
    time = scrapy.Field()
    # 出品地区
    area = scrapy.Field()

    mongo_collection = scrapy.Field()

    def mongo_insert(self):

        data = {
            'crawl_time':self['crawl_time'],
            'title': self['title'],
            'time': self['time'],
            'area': self['area'],
        }
        mongo_collection = self['mongo_collection']

        return mongo_collection,data

