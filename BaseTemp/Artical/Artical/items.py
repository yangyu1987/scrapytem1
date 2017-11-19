# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BoleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class WeiboInfoItem(scrapy.Item):
    timestamp = scrapy.Field()
    industry = scrapy.Field()
    account_id = scrapy.Field()
    account_name = scrapy.Field()
    account_url = scrapy.Field()
    following = scrapy.Field()
    follwers = scrapy.Field()
    post_count = scrapy.Field()
    account_note = scrapy.Field()
    # account_label = scrapy.Field()
    account_info = scrapy.Field()

class WeiboPostItem(scrapy.Item):
    timestamp = scrapy.Field()
    account_id = scrapy.Field()
    account_name = scrapy.Field()
    post_id = scrapy.Field()
    post_date = scrapy.Field()
    post_content = scrapy.Field()
    post_image = scrapy.Field()
    post_url = scrapy.Field()
    like = scrapy.Field()
    comment = scrapy.Field()
    forward = scrapy.Field()


class ImdbMovieItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()