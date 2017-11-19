# -*- coding: utf-8 -*-
import json
from datetime import datetime

import scrapy
from scrapy.selector import Selector

from weibo.common import *


class SinaSpider(scrapy.Spider):
    name = 'sina'
    # allowed_domains = ['weibo.com']
    start_urls = ['https://weibo.com/eauthermaleavene?is_all=1']

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    }

    def parse(self, response):

        counter = script_html_counter(response.text).xpath('//div[@class="PCD_counter"]')#重新装载selector对象
        person_info = script_html_person_info(response.text).xpath('//div[@class="PCD_person_info"]')

        timestamp = datetime.now().strftime('%Y-%m-%d')
        account_id = re.match(r".*CONFIG\['oid'\]='(\d+)'", response.text, re.DOTALL).group(1)
        account_name = re.match(r".*CONFIG\['onick'\]='(.*?)'", response.text, re.DOTALL).group(1)
        following = counter.xpath('div//td[@class="S_line1"][1]/strong[@class="W_f14"]/text()').extract()[0]
        follwers = counter.xpath('div//td[@class="S_line1"][2]/strong[@class="W_f14"]/text()').extract()[0]
        post_count = counter.xpath('div//td[@class="S_line1"][3]/strong[@class="W_f14"]/text()').extract()[0]
        account_note = person_info.xpath('div//p[@class="info"]/span/text()').extract()[0]
        account_info = replace_rtn(person_info.xpath('div//ul/li[3]/span[@class="item_text W_fl"]/text()').extract()[0])

        account = {
            'timestamp': timestamp,
            'account_id': account_id,
            'account_name': account_name,
            'account_url': response.url,
            'following': following,
            'follwers': follwers,
            'post_count': post_count,
            'account_note': account_note,
            'account_info': account_info
        }


        # 传递帐号信息
        data_user = {'account_id': account_id, 'account_name': account_name}
        page_id = re.match(r".*CONFIG\['page_id'\]='(\d+)'", response.text, re.DOTALL).group(1)
        time_param = time.time()*1000
        # ajax 请求
        ajax_url = 'https://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100606&is_all=1&id={0}&script_uri=/annasuicosmetics&page=1&__rnd=1510249138857'
        # yield scrapy.Request(url=ajax_url, callback=self.parse_post_ajax, meta=data_user)

        # https://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100606&is_all=1&id=1006061832363790&script_uri=/annasuicosmetics&page=1&__rnd=1510249138857

        # 普通请求，发起3页的微博内容请求
        # for i in range(1, 3):
        #     post_list_url = response.url + '&page={0}'.format(i)
        #     yield scrapy.Request(url=post_list_url, callback=self.parse_post, meta=data_user)
            # time.sleep(1)



    def parse_post(self, response):
        # 不用ajax请求可以抓取前15条
        res = script_html(response.text)#重新装载selector对象
        all_post = res.xpath('//div[contains(@class,"WB_cardwrap WB_feed_type")]')

        for weibo_post in all_post:
            timestamp = datetime.now().strftime('%Y-%m-%d')
            post_date = \
                weibo_post.xpath('div/div[@class="WB_detail"]/div[@class="WB_from S_txt2"]/a[1]/@title').extract()[0]
            post_id_temp = \
                weibo_post.xpath('div/div[@class="WB_detail"]/div[@class="WB_from S_txt2"]/a[1]/@href').extract()[0]
            post_id = re.match(r'^/\d+/(.*)\?from', post_id_temp).group(1)
            post_content = del_html_tag(
                weibo_post.xpath('div/div[@class="WB_detail"]/div[@class="WB_text W_f14"]').extract()[0])
            if '展开全文' in post_content:
                post_content = ''
            else:
                print(post_content)
            post_image = weibo_post.xpath('div/div[@class="WB_detail"]/div//img/@src').extract()[0]
            post_url_temp = \
                weibo_post.xpath('div/div[@class="WB_detail"]/div[@class="WB_from S_txt2"]/a[1]/@href').extract()[0]
            post_url = 'https:weibo.com' + re.match(r'(/\d+/.*?)\?', post_url_temp).group(1)
            like_temp = weibo_post.xpath('div[@class="WB_feed_handle"]//li[4]//em[2]/text()').extract()[0]
            like = '0' if "赞" in like_temp else like_temp
            comment_temp = weibo_post.xpath('div[@class="WB_feed_handle"]//li[3]//em[2]/text()').extract()[0]
            comment = '0' if "评论" in comment_temp else comment_temp
            forward_temp = weibo_post.xpath('div[@class="WB_feed_handle"]//li[2]//em[2]/text()').extract()[0]
            forward = '0' if "转发" in forward_temp else forward_temp

            data_post = {
                'timestamp': timestamp,
                # 'account_id': account_id,
                # 'account_name': account_name,
                'post_id': post_id,
                'post_date': post_date,
                'post_content': post_content,
                'post_image': post_image,
                'like': like,
                'comment': comment,
                'forward': forward
            }

            print(data_post)

    def parse_post_ajax(self,response):
        #ajax抓取解析
        htm = json.loads(response.text)
        res = Selector(text=htm['data'])
        all_post = res.xpath('//div[contains(@class,"WB_cardwrap WB_feed_type")]')
        # print(len(all_post))
        for weibo_post in all_post:
            #开始解析
            timestamp = datetime.now().strftime('%Y-%m-%d')
            account_id = response.meta.get('account_id')
            account_name = response.meta.get('account_name')
            post_date = weibo_post.xpath('div/div[@class="WB_detail"]/div[@class="WB_from S_txt2"]/a[1]/@title').extract()[0]
            post_id_temp = weibo_post.xpath('div/div[@class="WB_detail"]/div[@class="WB_from S_txt2"]/a[1]/@href').extract()[0]
            post_id = re.match(r'^/\d+/(.*)\?from', post_id_temp).group(1)
            post_content = del_html_tag(weibo_post.xpath('div/div[@class="WB_detail"]/div[@class="WB_text W_f14"]').extract()[0])
            # if '展开全文' in post_content:
            #     post_content = ''
            # else:
            #     print(post_content)
            post_url_temp = weibo_post.xpath('div/div[@class="WB_detail"]/div[@class="WB_from S_txt2"]/a[1]/@href').extract()[0]
            post_url = 'https:weibo.com' + re.match(r'(/\d+/.*?)\?', post_url_temp).group(1)
            like_temp = weibo_post.xpath('div[@class="WB_feed_handle"]//li[4]//em[2]/text()').extract()[0]
            like = '0' if "赞" in like_temp else like_temp
            comment_temp = weibo_post.xpath('div[@class="WB_feed_handle"]//li[3]//em[2]/text()').extract()[0]
            comment = '0' if "评论" in comment_temp else comment_temp
            forward_temp = weibo_post.xpath('div[@class="WB_feed_handle"]//li[2]//em[2]/text()').extract()[0]
            forward = '0' if "转发" in forward_temp else forward_temp
            try:
                post_image = weibo_post.xpath('div/div[@class="WB_detail"]/div//img/@src').extract()[0]
            except:
                post_image = '无图'

            data_post = {
                'timestamp': timestamp,
                'account_id': account_id,
                'account_name': account_name,
                'post_id': post_id,
                'post_date': post_date,
                'post_content': post_content,
                'post_image': post_image,
                'like': like,
                'comment': comment,
                'forward': forward
            }

            print(data_post)

