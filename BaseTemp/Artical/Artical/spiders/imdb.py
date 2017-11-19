# -*- coding:utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from header_list import get_header
from Artical.items import ImdbMovieItem


class ImdbSpider(CrawlSpider):
    name = 'imdb'
    allowed_domains = ['imdb.cn']
    start_urls = ['http://www.imdb.cn/NowPlaying/']

    rules = (
        Rule(LinkExtractor(allow=r'Sections/.*'), follow=True),
        Rule(LinkExtractor(allow=r'title/tt\d+'), callback='parse_item', follow=True),
        # Rule(),
        # Rule(),
    )

    headers = get_header()

    custom_settings = {
        'COOKIES_ENABLED' : False,
        'ITEM_PIPELINES':{'Artical.pipelines.ImdbMoviePipeline': 300,}
    }


    # def start_requests(self):
    #     for i in range(1,10000):
    #         url = 'http://www.imdb.cn/nowplaying/{0}'.format(i)
    #         yield scrapy.Request(url, callback=self.parse, headers=self.headers)

    def parse_item(self, response):
        #解析电影详情页
        item = ImdbMovieItem()
        item['url'] = response.url
        item['title'] = response.xpath('//div[@class="fk-3"]/div/h3/text()').extract()[0]

        yield item