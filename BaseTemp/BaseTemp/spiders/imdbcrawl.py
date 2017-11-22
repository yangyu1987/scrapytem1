# -*- coding: utf-8 -*-
# scrapy genspider -t imdbcrawl www.imdb.com
import re
from datetime import datetime

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from BaseTemp.items import BasetempItem
from BaseTemp.tools import header_list


class ImdbcrawlSpider(CrawlSpider):
    name = 'imdbcrawl'
    allowed_domains = ['www.imdb.cn']
    start_urls = ['http://www.imdb.cn/NowPlaying/']


    rules = (
        Rule(LinkExtractor(allow=r'Sections/.*'), follow=True),
        Rule(LinkExtractor(allow=r'title/tt\d+'), callback='parse_item', follow=True),
        # Rule(),
        # Rule(),
    )

    headers = header_list.get_header()

    custom_settings = {
        # do not needs login project
        'COOKIES_ENABLED': False,
        'ITEM_PIPELINES':{
            'BaseTemp.pipelines.ImdbMongoPipeline': 300,
        },
        # do not needs login project
        'DOWNLOADER_MIDDLEWARES':{
            'BaseTemp.middlewares.UserAgentMiddleware': 200,
        },
        'MONGO_DB':'imdb',
        'JOBDIR':'info/imdbcrawl.cn/001',

    }

    def parse_item(self, response):

        movie_item = BasetempItem()
        movie_item['crawl_time'] = datetime.now().strftime('%Y-%m-%d')
        movie_item['title'] = response.xpath('//div[@class="fk-3"]/div/h3/text()').extract()[0].strip()
        movie_item['time'] = self.get_time(response)
        movie_item['area'] = self.get_area(response)
        movie_item['mongo_collection'] = 'movie1'  # 选择mongo表

        yield movie_item

    def get_time(self,response):

        if re.search('<i>上映时间：</i><a.*?>(\d+)</a>',response.text):
            time = re.search('<i>上映时间：</i><a.*?>(\d+)</a>',response.text).group(1).strip()
        else:
            time = ''
        return time

    def get_area(self,response):

        if re.search('<i>国家：</i><a.*?>(.*?)</a>',response.text):
            area = re.search('<i>国家：</i><a.*?>(.*?)</a>',response.text).group(1).strip()
        else:
            area = ''
        return area
