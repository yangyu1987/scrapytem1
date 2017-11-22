# -*- coding: utf-8 -*-
import re
from datetime import datetime

import scrapy

from BaseTemp.items import BasetempItem
from BaseTemp.tools import header_list


class ChahaoSpider(scrapy.Spider):
    name = 'chahao'
    allowed_domains = ['chahaoba.com']
    start_urls = ['https://www.chahaoba.com/index.php?title=分类:骗子号码']

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

    def parse(self, response):
        next_page = response.xpath('//div[@id="mw-pages"]/a[1]/@href').extract()[0]
        print(response.url_join(next_page))