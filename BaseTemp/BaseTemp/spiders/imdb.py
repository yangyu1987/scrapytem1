# -*- coding: utf-8 -*-
import scrapy
from BaseTemp.items import BasetempItem
from datetime import datetime
import re
from BaseTemp.utils import header_list


class ImdbSpider(scrapy.Spider):
    name = 'imdb'
    allowed_domains = ['www.imdb.cn']
    start_urls = ['http://www.imdb.cn/nowplaying/1']

    custom_settings = {
        'COOKIES_ENABLED': False,
        'ITEM_PIPELINES':{
            'BaseTemp.pipelines.ImdbMongoPipeline': 300,
        },
        'MONGO_DB':'imdb',
        # 'MONGO_COLLECTION':'movie',
        'JOBDIR': 'info/imdb.com/001',
        # 'LOG_FILE':'imdb_log.txt',
    }

    headers = header_list.get_header()

    def parse(self, response):
        # 获取下一页 并抽取详情链接
        for page in range(1,2):
            movie_url = response.xpath('//div[@class="ss-3 clear"]/a/@href').extract()
            for url in movie_url:
                yield scrapy.Request(url=response.urljoin(url),headers=self.headers,callback=self.parse_movie)

            next_page = 'http://www.imdb.cn/nowplaying/{0}'.format(page)
            yield scrapy.Request(url=next_page,headers=self.headers,callback=self.parse)


    def parse_movie(self,response):
        # 解析电影页面
        movie_item = BasetempItem()
        movie_item['crawl_time'] = datetime.now().strftime('%Y-%m-%d')
        movie_item['title'] = response.xpath('//div[@class="fk-3"]/div/h3/text()').extract()[0].strip()
        movie_item['time'] = self.get_time(response)
        movie_item['area'] = self.get_area(response)
        movie_item['mongo_collection'] = 'movie'#选择mongo表

        yield movie_item


    def get_time(self,response):

        if re.search('<i>上映时间：</i><a.*?>(\d+)</a>',response.text):
            time = re.search('<i>上映时间：</i><a.*?>(\d+)</a>',response.text).group(1).strip()
        else:
            time = ''
        return time

    def get_area(self,response):

        if re.search('<i>国家：</i><a.*?>(.*?)</a>',response.text):
            area = re.search('<i>上映时间：</i><a.*?>(\d+)</a>',response.text).group(1).strip()
        else:
            area = ''
        return area
