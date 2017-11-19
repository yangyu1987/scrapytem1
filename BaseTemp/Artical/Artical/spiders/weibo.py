# -*- coding: utf-8 -*-
import scrapy
import re
import json
from datetime import datetime
from Artical.items import  WeiboInfoItem,WeiboPostItem
from Artical.utils.url_lists import URL_LIST
import time

class WeiboSpider(scrapy.Spider):
    #微波爬虫，登录版本
    name = 'weibo'
    allowed_domains = ['weibo.cn']
    start_urls = URL_LIST

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    }

    def start_requests(self):
        #登录必须带上登录页的请求
        login_url = 'https://passport.weibo.cn/signin/login'
        return [scrapy.Request(url=login_url,headers=self.headers,callback=self.login)]

    def login(self,reponse):
        #处理登录，此处的response来自login——url页面
        username = '493749813@qq.com'
        password = ''

        post_data = {
            'username': username,
            'password': password,
            'savestate': '1',
            'ec': '0',
            'entry': 'mweibo',
            'mainpageflag': '1',
        }

        return [scrapy.FormRequest(
            url = 'https://passport.weibo.cn/sso/login',
            formdata = post_data,
            headers = self.headers,
            callback = self.check_login,
        )]

    def check_login(self, response):
        #检查是否登录成功
        json_text = json.loads(response.text)
        if json_text['data']['uid']:
            #print('登录成功')
            #带上cookie 发起请求，爬取网页(回到调用start_urls)
            for url in self.start_urls:
                yield scrapy.Request(url=url,dont_filter=True,headers=self.headers)
        else:
            print('登录失败')

    def parse(self, response):
        #1,获取帐号信息
        #2,获取具体博文
        timestamp = datetime.now().strftime("%Y-%m-%d")
        industry = ''
        account_id = response.xpath('//div[@class="ut"]/a[2]/@href').extract()[0].split('/')[1]
        account_name = response.xpath('//div[@class="ut"]/span[@class="ctt"][1]/text()').extract()[0]
        account_url = response.url.replace('.cn','.com')
        following = response.xpath('//div[@class="tip2"]/a[1]/text()').extract()[0].replace(']','[').split('[')[-2]
        follwers = response.xpath('//div[@class="tip2"]/a[2]/text()').extract()[0].replace(']','[').split('[')[-2]
        post_count = response.xpath('//div[@class="tip2"]/span[@class="tc"]').extract()[0].replace(']','[').split('[')[-2]
        account_note = response.xpath('//span[@class="ctt"][2]/text()').extract()[0]
        account_info = response.xpath('//span[@class="ctt"][3]/text()').extract()[0]

        # item_info = WeiboInfoItem()
        # item_info['timestamp'] = timestamp
        # item_info['industry'] = industry
        # item_info['account_id'] = account_id
        # item_info['account_name'] = account_name
        # item_info['account_url'] = account_url
        # item_info['following'] = following
        # item_info['follwers'] = follwers
        # item_info['post_count'] = post_count
        # item_info['account_note'] = account_note
        # item_info['account_info'] = account_info
        #
        # yield item_info
        post_list_url = response.url + '?page=1'
        data_user = {'account_id': account_id,'account_name':account_name}
        # 发起20页的微博内容请求
        for i in range(1, 20):
            post_list_url = response.url + '?page={0}'.format(i)
            yield scrapy.Request(url=post_list_url, callback=self.parse_post_link, meta=data_user)
            # time.sleep(1)

    def parse_post_link(self ,response):
        #获取微博列表页上能抓取的，微博详细信息和微波
        try:
            posts = response.xpath('//div[@class="c"][position()<11]')
            for post in posts:
                timestamp = datetime.now().strftime("%Y-%m-%d")
                account_id = response.meta.get('account_id')
                account_name = response.meta.get('account_name')
                post_id = post.xpath('@id').extract()[0].split('_')[1]
                post_date = ''.join(post.xpath('div/span[@class="ct"]/text()').extract()[0].split(' ')[:-1]).replace(' 来自微博','')
                post_image = post.xpath('div/a/img[@class="ib"]/@src').extract()[0]
                lb = post.xpath('div[2]').extract()[0]
                like = re.match(r'.*赞.*?(\d+).*',lb).group(1)
                comment = re.match(r'.*论.*?(\d+).*', lb).group(1)
                forward = re.match(r'.*转发.*?(\d+).*', lb).group(1)

                data_post = {
                    'timestamp':timestamp,
                    'account_id':account_id,
                    'account_name':account_name,
                    'post_id':post_id,
                    'post_date':post_date,
                    'post_image':post_image,
                    'like':like,
                    'comment':comment,
                    'forward':forward
                }

                comment_url = 'https://weibo.cn/comment/'+post_id

                yield scrapy.Request(url = comment_url,callback=self.parse_post,meta=data_post)

        except Exception as e:
            print(e)


    def parse_post(self, response):
        #跳到详情页获取全文内容
        post_content = response.xpath('//div[@id="M_"]/div/span[@class="ctt"]').extract()[0]
        re_h = re.compile('</?\w+[^>]*>')
        post_content = re_h.sub('', post_content)
        re_h1 = re.compile('^:')
        post_content = re_h1.sub('', post_content)
        item_post = WeiboPostItem()
        item_post['timestamp'] = response.meta.get('timestamp')
        item_post['account_id'] = response.meta.get('account_id')
        item_post['account_name'] = response.meta.get('account_name')
        item_post['post_id'] = response.meta.get('post_id')
        item_post['post_date'] = response.meta.get('post_date')
        item_post['post_content'] = post_content
        item_post['post_image'] = response.meta.get('post_image')
        item_post['post_url'] = 'https://weibo.com/'+item_post['account_id']+'/'+item_post['post_id']
        item_post['like'] = response.meta.get('like')
        item_post['comment'] = response.meta.get('comment')
        item_post['forward'] = response.meta.get('forward')

        yield item_post
        # 获取具体post信息
        # timestamp = scrapy.Field()
        # account_id = scrapy.Field()
        # post_id = scrapy.Field()
        # post_date = scrapy.Field()
        # post_content = scrapy.Field()
        # post_image = scrapy.Field()
        # post_url = scrapy.Field()
        # like = scrapy.Field()
        # comment = scrapy.Field()
        # forward = scrapy.Field()
