# -*- coding: utf-8 -*-
import scrapy
import re


class BoleSpider(scrapy.Spider):
    name = 'bole'
    allowed_domains = ['www.readnovel.com']
    start_urls = ['https://www.readnovel.com/all?pageSize=10&pageNum=1']

    header = {
        'user-agent:':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    }

    # def parse(self, response):
    #     res = response.xpath('//div[@class="post floated-thumb"]')
    #     # print(len(res))
    #     for items in res:
    #         in_url = items.xpath('div[@class="post-meta"]//span[@class="read-more"]/a/@href').extract()
    #         yield scrapy.Request(url = in_url,headers=self.header,callback=self.parse_item)
    #
    #     next_page = response.xpath('//a[@class="next page-numbers"]/@href').extract()[0]
    #     yield scrapy.Request(url = next_page,callback=self.parse)
    #
    # def parse_item(self,response):
    #     pass

    def parse(self, response):
        all_url = response.xpath('//div[@class="book-info"]/h3/a/@href').extract()
        for book_url in all_url:
            yield scrapy.Request(url = response.urljoin(book_url),headers=self.header,callback=self.parse_book)
        print(int(response.url.split('=')[-1])+1)
        response.url.split('=')[-1] = int(response.url.split('=')[-1])+1
        next_page_str = response.url.split('=')
        next_page_str[-1] = str(int(next_page_str[-1])+1)
        next_page = '='.join(next_page_str)
        # next_page = response.xpath('').extract()[0]
        yield scrapy.Request(url = next_page,callback=self.parse)

    def parse_book(self,response):
        pass