# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

from weibo.common import Mogo_helper


# class WeiboInfoJsonPipeline(object):
#     def process_item(self, item, spider):
#         text = json.dumps(dict(item), ensure_ascii = False) + '\n'
#         fileName = 'account_info:'
#         with open('weibo/weibo_info/'+fileName + '.json', 'ab+') as f:
#             f.write(text.encode('utf-8'))
#         return item


class WeiboPostJsonPipeline(object):
    def process_item(self, item, spider):
        text = json.dumps(dict(item), ensure_ascii=False) + '\n'
        fileName = 'Post' + item.get('account_name')
        with open('weibo/weibo_post/' + fileName + '.json', 'ab+') as f:
            f.write(text.encode('utf-8'))
        return item


class ImdbMoviePipeline(object):
    #imdb电影保存到mongodb
    def __init__(self):
        self.mogo = Mogo_helper('imdb')

    def process_item(self, item, spdier):
        self.mogo.save_data('movie',dict(item))
        return item
