# -*- coding: utf-8 -*-
import re
from datetime import datetime

import scrapy

from BaseTemp.items import PhoneItem
from BaseTemp.tools import header_list
from BaseTemp.utils.common import get_num


class PhonenumSpider(scrapy.Spider):
    name = 'phonenum'
    allowed_domains = ['www.so.com']
    start_urls = ['https://www.so.com/s?q=13716919636']

    custom_settings = {
        # do not needs login project
        'COOKIES_ENABLED': False,
        'ITEM_PIPELINES': {
            'BaseTemp.pipelines.MongoPipeline': 300,
        },
        # do not needs login project
        'DOWNLOADER_MIDDLEWARES': {
            'BaseTemp.middlewares.UserAgentMiddleware': 200,
        },
        'MONGO_DB': 'phone',
        'JOBDIR': 'info/phone/001',
        # 'LOG_FILE':'imdb_log.txt',
    }
    headers = header_list.get_header()

    def parse(self, response):
        # 解析电话号码
        item = PhoneItem()
        msg = response.xpath('//p[@class="mh-detail"]/text()').extract()[0].split()
        item['crawl_time'] = datetime.now().strftime('%Y-%m-%d')
        item['phone_num'] = msg[0]
        item['area'] = msg[1]
        item['service_provider'] = msg[2]
        item['mongo_collection'] = 'info'

        yield item

