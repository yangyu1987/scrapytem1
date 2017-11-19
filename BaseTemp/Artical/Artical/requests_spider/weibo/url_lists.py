#! -*- coding:utf-8 -*-
import random

#待爬取URL列表
START_URL_LIST = [
    'https://www.weibo.com/eauthermaleavene',
    'https://www.weibo.com/acquadiparma',
    'https://www.weibo.com/AlfredDunhill',
    'https://www.weibo.com/AmorepacificHongKong',
    'https://www.weibo.com/annasuicosmetics',
    'https://www.weibo.com/artistry',
    'https://www.weibo.com/vaupres',
    'https://www.weibo.com/avenedermatologist',
    'https://www.weibo.com/avonvoices',
    'https://www.weibo.com/benefit',
    'https://www.weibo.com/biotherm',
    'https://www.weibo.com/bobbibrownchina',
    'https://www.weibo.com/bulgari',
    'https://www.weibo.com/burberry',
    'https://www.weibo.com/ckBeauty',
    'https://www.weibo.com/52carslan',
    'https://www.weibo.com/chcedo',
    'https://www.weibo.com/chanel',
    'https://www.weibo.com/cijiws',
    'https://www.weibo.com/chloeparis',
    'https://www.weibo.com/clarins',
    'https://www.weibo.com/clarisonicchina',
    'https://www.weibo.com/CledepeauBeaute',
    'https://www.weibo.com/cliniqueu',
    'https://www.weibo.com/dabaohuodong',
    'https://www.weibo.com/dhcsh',
    'https://www.weibo.com/dior',
    'https://www.weibo.com/elizabetharden',
    'https://www.weibo.com/esteelauder',
    'https://www.weibo.com/etudehousechina',
    'https://www.weibo.com/freshBeauty',
    'https://www.weibo.com/gf1992',
    'https://www.weibo.com/giorgioarmaniBeauty',
    'https://www.weibo.com/parfumsgivenchy'
]


class UrlList(object):
    # 链接列表
    def __init__(self):
        self.url_list = []#待爬取
        self.done_list = []#已爬取

    def get_url(self):
        #取出url，方式可在setting中配置
        # url = self.url_list.pop()
        url = self.url_list.pop(0)
        self.done_list.append(url)#存入已爬取列表
        return url

    def save_url(self,url):
        #加入新的url并去重
        if url not in self.done_list:
            self.url_list.append(url)
            self.url_list = list(set(self.url_list))
        else:
            print('已爬取')