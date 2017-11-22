# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from BaseTemp.items import BasetempItem
from BaseTemp.tools import header_list


class LieSpider(CrawlSpider):
    name = 'lie'
    allowed_domains = ['chahaoba.com']
    start_urls = ['https://www.chahaoba.com/分类:骗子号码']

    rules = (
        Rule(LinkExtractor(allow=r'.*pagefrom.*'), follow=True),
        Rule(LinkExtractor(allow=r'.*?\d{11}'), callback='parse_item', follow=True),
    )

    headers = header_list.get_header()

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
        'JOBDIR': 'info/chahao/001',

    }

    def parse_item(self, response):
        print(response.url)
