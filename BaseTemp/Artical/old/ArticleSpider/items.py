# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ZhihuQItem(scrapy.Item):
    #zhihu qusetion Item
    zhihu_id = scrapy.Field()
    topic = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    answer_num = scrapy.Field()
    comments_num = scrapy.Field()
    watch_num = scrapy.Field()
    click_num = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        #get insert sql
        insert_sql = '''
            insert into zhihu_q(tittle, content, url, comment, zan, fav_num, front_img, create_date)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        params = ((self['tittle'], self['content'], self['url'], self['comment'], self['zan'], self['fav_num'], self['front_img_url'], self['create_date']))

        return params, insert_sql

class ZhihuAItem(scrapy.Item):
    #zhihu answer item
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    praise_num = scrapy.Field()
    comments_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_update_time = scrapy.Field()

    def get_insert_sql(self):
        #get insert sql
        insert_sql = '''
            insert into zhihu_a(tittle, content, url, comment, zan, fav_num, front_img, create_date)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        params = ((self['tittle'], self['content'], self['url'], self['comment'], self['zan'], self['fav_num'], self['front_img_url'], self['create_date']))

        return params, insert_sql
