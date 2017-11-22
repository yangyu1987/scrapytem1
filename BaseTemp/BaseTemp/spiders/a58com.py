# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from BaseTemp.items import BasetempItem
from BaseTemp.tools import header_list


class A58comSpider(CrawlSpider):
    name = '58com'
    allowed_domains = ['58.com']
    start_urls = ['http://nj.58.com/hezu/0/']

    rules = (
        Rule(LinkExtractor(allow=r'hezu/0/pn\d+/'), follow=True),
        Rule(LinkExtractor(allow=r'hezu/.*?shtml'), callback='parse_item', follow=True),
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
        'JOBDIR': 'info/58crawl/001',

    }


    def parse_item(self, response):
        print(response.text)
        pass
