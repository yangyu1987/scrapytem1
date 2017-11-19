#! -*- coding:utf-8 -*-
from scrapy.selector import Selector
import re
import pymongo
import time
import random

def script_html(htm):
    #页面转为可用的Selector对象(新浪微博)
    res = Selector(text=htm)
    script_set = res.xpath('//script')

    for s in script_set:
        s_text = s.xpath('text()').extract()[0].replace(r'\"', r'"').replace(r'\/', r'/')
        if s_text.find('WB_feed_detail') > 0:
            script = s_text
            # print(script)
            break
    return Selector(text=script)

def script_html_counter(htm):
    #页面转为可用的Selector对象(新浪微博)
    res = Selector(text=htm)
    script_set = res.xpath('//script')

    for s in script_set:
        s_text = s.xpath('text()').extract()[0].replace(r'\"', r'"').replace(r'\/', r'/')
        if s_text.find('PCD_counter') > 0:
            script = s_text
            # print(script)
            break
    return Selector(text=script)


def script_html_person_info(htm):
    #页面转为可用的Selector对象(新浪微博)
    res = Selector(text=htm)
    script_set = res.xpath('//script')

    for s in script_set:
        s_text = s.xpath('text()').extract()[0].replace(r'\"', r'"').replace(r'\/', r'/')
        if s_text.find('PCD_person_info') > 0:
            script = s_text
            # print(script)
            break
    return Selector(text=script)


def del_html_tag(html):
    #除去微博正文html标签和开头的：号
    html_temp = re.compile('</?\w+[^>]*>').sub('', html)
    html = re.compile('^:').sub('', html_temp)
    text = html.replace(' ', '').replace(r'\n', '')
    return text

s = '去除多余的\n\r\t除多余'
def replace_rtn(text):
    #去除多余的\n\r\t
    text = ''.join(text.split())
    return text


def del_dupl():
    #去重复
    pass

class Mogo_helper(object):

    def __init__(self,db):
        self.client = pymongo.MongoClient('localhost',27017)
        self.db = self.client[db]  # 选择数据库

    def save_data(self,table,datas):
        #保存数据
        table = self.db[table]  # 选择表
        table.insert_one(datas) #插入数据
        # time.sleep(random.random())

    def data_count(self,table):
        #查询数量
        table = self.db[table]  # 选择表
        return table.find().count()

    # def find_all(self,table):
    #     table = self.db[table]  # 选择表
    #     return table.find()

