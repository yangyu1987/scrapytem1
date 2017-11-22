# -*- coding: utf-8 -*-
import re
from datetime import datetime

import scrapy

from BaseTemp.items import BasetempItem
from BaseTemp.tools import header_list
from BaseTemp.utils.common import *


class ChahaoSpider(scrapy.Spider):
    name = 'chahao'
    allowed_domains = ['chahaoba.com']
    start_urls = ['https://www.chahaoba.com/index.php?title=%E5%88%86%E7%B1%BB:%E9%AA%97%E5%AD%90%E5%8F%B7%E7%A0%81&amp%3Bpagefrom=%2B02227393016%EF%BC%9B%2B37911183&pagefrom=%2B0222999767#mw-pages']

    custom_settings = {
        # do not needs login project
        'COOKIES_ENABLED': False,
        # 'ITEM_PIPELINES': {
        #     'BaseTemp.pipelines.ImdbMongoPipeline': 300,
        # },
        # do not needs login project
        'DOWNLOADER_MIDDLEWARES': {
            'BaseTemp.middlewares.UserAgentMiddleware': 200,
        },
        # 'MONGO_DB': 'imdb',
        # 'JOBDIR': 'info/chahao/001',
        # 'LOG_FILE':'imdb_log.txt',
    }
    headers = header_list.get_header()
    page = 1

    def parse(self, response):

        nums = response.xpath('//div[@class="mw-category"]//li')
        for num in nums:
            phone_nums = get_num(num.xpath('a/text()').extract()[0])
            if len(phone_nums) == 11 and phone_nums.startswith('1'):
                num_link = response.urljoin(phone_nums)
                phone_num = phone_nums
                yield scrapy.Request(url=num_link, headers=self.headers, meta={'phone_num': phone_num},
                                     callback=self.parse_detail)

        try:
            next_page = re.search('.*<a href="(.*?)" title=".*?">下一页</a>',response.text).group(1)
            next_page = response.urljoin(next_page.replace('amp;', '').replace('amp', ''))
            yield scrapy.Request(next_page,headers=self.headers,callback=self.parse)

        except Exception as e:
            print('已经是最后一页')


    def parse_detail(self,response):
        # 解析详情页面
        try:
            area = re.search('归属省份地区：<a href=".*?">(.*?)</a>',response.text).group(1)
        except:
            area = '未知'
        try:
            provider = re.search('电信运营商：<a href=".*?">(.*?)</a>',response.text).group(1)
        except:
            provider = '未知'

        title = '诈骗电话'

        print(title)
        print(area)
        print(provider)


