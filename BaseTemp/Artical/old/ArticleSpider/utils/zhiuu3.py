#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 8/14/17 6:25 AM
# @Author  : Yang

import scrapy
from PIL import Image

class Zhihu3Spider(scrapy.spider):
    name = 'zhihu3'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com']
    header = {
        'User-Agent':'',
        'referer':'https://www.zhihu.com'
    }

    def parse(self, response):
        pass

    def start_requests(self):
        #send request
        return [scrapy.Request(url='https://www.zhihu.com',headers = self.header, callback=self.get_login_info)]

    def get_login_info(self,response):
        #get login info
        xrsf = response.xpath('').extraxt()[0]
        yield scrapy.Request(url='',headers=self.header, callback=self.get_captcha, meta={'xrsf':xrsf})

    def get_captcha(self,reponse):
        #captcha
        xrsf = reponse.meta.get('xrsf')
        with open('catpcha.jpg', 'wb') as f:
            f.write(reponse.body)

        try:
            im = Image.open('captcha.jpg')
            im.show()
            im.close()
        except:
            pass

        captcha = input('captch\n')

        post_data = {
            'num':'123123',
            'passwd':'123123',
            'captcha':captcha,
            'xrsf':xrsf
        }

        return [scrapy.FormRequest(
            url = 'https://www.zhihu.com/login/phone_num',
            formdata = post_data,
            headers= self.header,
            callback= self.strat_zhihu_spider
        )]

    def strat_zhihu_spider(self, response):
        text_json = json.loads(response.text)
        if 'msg' in text_json and text_json['msg'] =='':
            for url in self.start_urls:
                yield scrapy.Request(url, headers=self.header)


