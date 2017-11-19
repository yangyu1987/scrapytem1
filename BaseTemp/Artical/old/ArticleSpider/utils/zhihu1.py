#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 8/12/17 8:21 AM
# @Author  : Yang

import scrapy
import re
import time
from PIL import Image
import json

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/']
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Host': 'www.zhihu.com'

    }

    def parse(self, response):
        pass

    def start_requests(self):
        yield scrapy.Request('https://www.zhihu.com',headers=self.header,callback=self.get_login_info)

    def get_login_info(self,response):

        #qingqiu yici huo qu xsrf
        re_obj = '.*name="_xsrf" value="(.*?)"'
        match_obj = re.match(re_obj, response.text, re.DOTALL)
        xsrf = ''
        if match_obj:
            xsrf = match_obj.group(1)

        if xsrf:
            t = str(int(time.time() * 1000))
            captcha_url = 'https://www.zhihu.com/captcha.gif?r={0}&type=login'.format(t)
            yield scrapy.Request(captcha_url,headers=self.header,callback=self.captcha_in,meta={'xsrf':xsrf})

    def captcha_in(self,response):
        #login
        with open('captcha.jpg', 'wb') as f:
            f.write(response.body)
        try:
            im = Image.open('captcha.jpg')
            im.show()
            im.close()
        except:
            pass

        captcha = input('captch\n')
        xsrf = response.meta.get('xsrf')
        post_data = {
            'xsrf': xsrf,
            'password': '123123',
            'phone_num': '15251769161',
            'captcha':captcha
        }

        return [scrapy.FormRequest(
            url='https://www.zhihu.com/login/phone_num',
            formdata=post_data,
            headers=self.header,
            callback=self.check_login
        )]

    def check_login(self,response):
        #login check
        text_json = json.loads(response.text)
        if 'msg' in text_json and text_json['msg'] == '登录成功':
            for url in self.start_urls:
                yield scrapy.Request(url, headers=self.header)
