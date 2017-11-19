# -*- coding: utf-8 -*-
import re
import time
import datetime
from PIL import Image
import json
from urllib import parse
try:
    from urllib import parse
except:
    pass

import scrapy
from ArticleSpider.items import ZhihuQItem,ZhihuAItem

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com']
    start_answer_url = 'http://www.zhihu.com/api/v4/questions/{0}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit={1}&offset={2}&sort_by=default'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Host': 'www.zhihu.com',
        'Referer':'https://www.zhihu.com'

    }

    def get_url(self,response):
        #get page url
        all_url = response.xpath('//a/@href').extract()
        all_url = [parse.urljoin(response.url, url) for url in all_url]
        all_url = filter(lambda x: True if x.startswith('https') else False, all_url)
        for url in all_url:
            match_obj = re.match('(.*zhihu.com/question/(\d+))(/|$).*', url)
            if match_obj:
                request_url = match_obj.group(1)
                question_id = match_obj.group(2)
                yield scrapy.Request(request_url, headers=self.header, meta={'question_id': question_id},
                                     callback=self.parse_question)
            else:
                yield scrapy.Request(url, headers=self.header, callback=self.parse)

    def parse(self, response):

        all_url = response.xpath('//a/@href').extract()
        all_url = [parse.urljoin(response.url, url) for url in all_url]
        all_url = filter(lambda x: True if x.startswith('https') else False, all_url)
        for url in all_url:
            match_obj = re.match('(.*zhihu.com/question/(\d+))(/|$).*', url)
            if match_obj:
                request_url = match_obj.group(1)
                question_id = match_obj.group(2)
                yield scrapy.Request(request_url, headers=self.header, meta={'question_id': question_id},callback=self.parse_question)
            else:
                yield scrapy.Request(url, headers=self.header, callback=self.parse)

    def parse_question(self,response):
        #zhihu question
        if 'QuestionHeader-title' in response.text:
            #zhihu new question
            q_item = ZhihuQItem()
            question_id = int(response.meta.get('question_id'))
            q_item['zhihu_id'] =  question_id
            q_item['topic'] = response.xpath('//a[@class="TopicLink"]/div[@class="Popover"]/div/text()').extract()[0]
            q_item['url'] = response.url
            q_item['title'] = response.xpath('//h1/text()').extract()[0]
            q_item['content'] = response.xpath('//div[@class = "QuestionHeader-detail"]//span/text()').extract()[0]
            # q_item['create_time'] = response.xpath('').extract()[0]
            # q_item['update_time'] = response.xpath('').extract()[0]
            answer_num_temp = response.xpath('//h4/span/text()').extract()[0].strip()
            q_item['answer_num'] = int(re.match('(\d+).*',answer_num_temp).group(1))
            q_item['comments_num'] = response.xpath('//div[@class="QuestionHeader-Comment"]/button/text()').extract()[0]
            q_item['watch_num'] = int(response.xpath('//div[@class="NumberBoard-value"]/text()').extract()[0])
            q_item['click_num'] = int(response.xpath('//div[@class="NumberBoard-value"]/text()').extract()[1])
            # q_item['crawl_time'] = response.xpath('').extract()[0]
            # zhihu_id = scrapy.Field()
            # topic = scrapy.Field()
            # url = scrapy.Field()
            # title = scrapy.Field()
            # content = scrapy.Field()
            # create_time = scrapy.Field()
            # update_time = scrapy.Field()
            # answer_num = scrapy.Field()
            # comments_num = scrapy.Field()
            # watch_num = scrapy.Field()
            # click_num = scrapy.Field()
            # crawl_time = scrapy.Field()
            yield scrapy.Request(self.start_answer_url.format(question_id,20,0),headers=self.header,callback=self.parse_answer)
            yield q_item
            # self.get_url(response)
        else:
            #zhihu old question
            pass

    def parse_answer(self,response):
        ans_json = json.loads(response.text)
        is_end = ans_json['paging']['is_end']
        totals_ans = ans_json['paging']['totals']
        next_url = ans_json['paging']['next']
        for answer in ans_json['data']:
            a_item = ZhihuAItem()
            a_item['zhihu_id'] = answer['id']
            a_item['url'] = answer['url']
            a_item['question_id'] = answer['question']['id']
            a_item['author_id'] = answer['author']['id'] if id in answer['author'] else None
            a_item['content'] = answer['content'] if 'content' in answer else None
            a_item['praise_num'] = answer['voteup_count']
            a_item['comments_num'] = answer['comment_count']
            a_item['create_time'] = answer['created_time']
            a_item['update_time'] = answer['updated_time']
            a_item['crawl_time'] = datetime.datetime.now()

            yield a_item


        if not is_end:
            yield scrapy.Request(next_url, headers=self.header,callback=self.parse_answer)

    def start_requests(self):
        return [scrapy.Request('https://www.zhihu.com/#signin', headers=self.header, callback=self.get_login_info)]

    def get_login_info(self,response):

        response_text = response.text
        re_obj = '.*name="_xsrf" value="(.*?)"'
        match_obj = re.match(re_obj, response_text, re.DOTALL)
        xsrf = ''
        if match_obj:
            xsrf = match_obj.group(1)

        t = str(int(time.time() * 1000))
        captcha_url = 'https://www.zhihu.com/captcha.gif?r={0}&type=login'.format(t)

        post_data = {
                    'xsrf': xsrf,
                    'password': '123123',
                    'phone_num': '15251769161',
                }
        yield scrapy.Request(captcha_url,headers=self.header,meta={'post_data':post_data},callback=self.login)

    def login(self,response):
        #login
        with open('captcha.jpg', 'wb') as f:
            f.write(response.body)
        try:
            im = Image.open('captcha.jpg')
            im.show()
            im.close()
        except:
            pass

        captcha = input('captch\n')
        post_data =response.meta.get('post_data',{})
        post_data['captcha'] = captcha
        return [scrapy.FormRequest(
            url='https://www.zhihu.com/login/phone_num',
            formdata=post_data,
            headers=self.header,
            callback=self.check_login
        )]

    def check_login(self,response):
        #chack login
        text_json = json.loads(response.text)
        if 'msg' in text_json and text_json['msg'] == '登录成功':
            for url in self.start_urls:
                yield scrapy.Request(url,dont_filter=True,headers=self.header)