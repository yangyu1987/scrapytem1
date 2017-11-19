# -*- coding:utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractor import LinkExtractor
from header_list import get_header
from Artical.items import ImdbMovieItem

class ImdbSpider(CrawlSpider):
    name = 'imdb'
    allowed_domains = ['']
    start_urls = ['http://www.imdb.cn/NowPlaying/']

    rules = (
        Rule(LinkExtractor(r''),follow=True),
        Rule()
    )