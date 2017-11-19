#-*- coding:utf-8 -*-

import requests
import re
import time
import json
from datetime import datetime
from url_lists import URL_LIST
from scrapy.selector import Selector

headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    }

ck = 'SINAGLOBAL=8921766109525.262.1491589733363; _s_tentry=cuiqingcai.com; Apache=7116304911733.029.1509961091600; ULV=1509961092417:19:1:1:7116304911733.029.1509961091600:1508547125886; login_sid_t=489d856c936895538d74617ada4ef0ec; cross_origin_proto=SSL; wvr=6; SCF=AsQR6i4BRxLD8_mqVTPrQ8xEH-0sid22myGpYHOykLJRbGL1Dt0ywJdDC6zvwUy1zW5h9AfPsCaJkPIIaq5B-OU.; SUHB=0OM0fxkOSDD5MV; ALF=1512740417; SUB=_2A253B3kQDeThGeNP6lcV9ijNyzuIHXVUCAdYrDV8PUJbkNBeLRnDkW09G8sf8yttzu6SU6MjFhEPgFFV1Q..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Whp8H91FrFCL3XUZjgYB7Zn5JpX5oz75NHD95QfeK2fShqceK5NWs4Dqcj_i--Xi-zRiKn7i--NiK.Xi-zNi--Ri-8si-zXi--NiK.Xi-zfi--fiK.fiKnc; UOR=bbs.win10go.com,widget.weibo.com,zihaolucky.github.io'
cookies = dict(i.strip().split('=') for i in ck.strip().split(';'))


def get_weibo_post(link,page_num=1):
    #获取指定微博的全部信息
    #page_num要爬取的页面总数， link微博主页链接

    #帐号基础信息
    res_info = requests.get(link, headers=headers, cookies=cookies)
    response_info = Selector(text=res_info.text)
    try:
        account_id = judge_null(response_info.xpath('//div[@class="ut"]/a[2]/@href').extract()[0].split('/')[1])
        account_name = judge_null(response_info.xpath('//div[@class="ut"]/span[@class="ctt"][1]/text()').extract()[0])
        # 开始循环抓取
        for i in range(1, page_num + 1):
            page_link = link + '?page={0}'.format(i)
            res = requests.get(link, headers=headers, cookies=cookies)
            response = Selector(text=res.text)  # 创建Selector对象
            get_all_post(response, account_id, account_name)  # 抓取当前页面的全部post
            time.sleep(5)  # 设置延时

    except Exception as e:
        print(e)



def get_all_post(response,account_id,account_name):
    #抓取当前页面的全部post
    posts = response.xpath('//div[@class="c"][position()<11]')
    for post in posts:
        timestamp = datetime.now().strftime("%Y-%m-%d")
        account_id = account_id
        account_name = account_name
        post_id = post.xpath('@id').extract()[0].split('_')[1]
        post_date = ''.join(post.xpath('div/span[@class="ct"]/text()').extract()[0].split(' ')[:-1]).replace(
            ' 来自微博', '')
        post_image = post.xpath('div/a/img[@class="ib"]/@src').extract()[0]
        lb = post.xpath('div[2]').extract()[0]
        like = re.match(r'.*赞.*?(\d+).*', lb).group(1)
        comment = re.match(r'.*论.*?(\d+).*', lb).group(1)
        forward = re.match(r'.*转发.*?(\d+).*', lb).group(1)
        comment_url = 'https://weibo.cn/comment/' + post_id

        try:
            if get_content(comment_url):
                post_content = get_content(comment_url)
            else:
                post_content = post.xpath('div/span[@class="ctt"]').extract()[0]
                post_content = content_re(post_content)
        except Exception as e:
            print(e)

        data_post = {
            'timestamp': timestamp,
            'account_id': account_id,
            'account_name': account_name,
            'post_id': post_id,
            'post_date': post_date,
            'post_content':post_content,
            'post_image': post_image,
            'like': like,
            'comment': comment,
            'forward': forward
        }
        print(data_post['account_name']+data_post['post_content'])
        #保存
        save_post_info(data_post)


def get_weibo_info(link):
    # 获取指定微博的基本信息
    res = requests.get(link, headers=headers, cookies=cookies)
    response = Selector(text=res.text)

    timestamp = datetime.now().strftime("%Y-%m-%d")
    account_id = response.xpath('//div[@class="ut"]/a[2]/@href').extract()[0].split('/')[1]
    account_name = response.xpath('//div[@class="ut"]/span[@class="ctt"][1]/text()').extract()[0]
    account_url = link.replace('.cn', '.com')
    following = response.xpath('//div[@class="tip2"]/a[1]/text()').extract()[0].replace(']', '[').split('[')[-2]
    follwers = response.xpath('//div[@class="tip2"]/a[2]/text()').extract()[0].replace(']', '[').split('[')[-2]
    post_count = response.xpath('//div[@class="tip2"]/span[@class="tc"]').extract()[0].replace(']', '[').split('[')[-2]
    account_note = response.xpath('//span[@class="ctt"][2]/text()').extract()[0]
    account_info = response.xpath('//span[@class="ctt"][3]/text()').extract()[0]

    #保存文件
    data = {
        'timestamp':timestamp,
        'account_id': account_id,
        'account_name': account_name,
        'account_url': account_url,
        'following': following,
        'follwers': follwers,
        'post_count': post_count,
        'account_note': account_note,
        'account_info': account_info
    }
    print(data['account_name'])
    save_account_info(data)


def save_account_info(data):
    #保存帐号信息
    text = json.dumps(data, ensure_ascii=False) + '\n'
    fileName = 'account_info'
    with open('weibo/weibo_info/' + fileName + '.json', 'ab+') as f:
        f.write(text.encode('utf-8'))


def save_post_info(data):
    #保存发布信息
    text = json.dumps(data, ensure_ascii=False) + '\n'
    fileName = 'account_info'
    with open('weibo/weibo_info/' + fileName + '.json', 'ab+') as f:
        f.write(text.encode('utf-8'))


def save_post_info(data):
    #保存具体博文信息
    text = json.dumps(data, ensure_ascii=False) + '\n'
    fileName = 'Post:' + data.get('account_name')
    with open('weibo/weibo_post/' + fileName + '.json', 'ab+') as f:
        f.write(text.encode('utf-8'))


def judge_null(x):
    #防止
    x = x if x else None
    return x


def content_re(post_content):
    #除去微博正文html标签和开头的：号
    post_content_temp = re.compile('</?\w+[^>]*>').sub('', post_content)
    post_content = re.compile('^:').sub('', post_content_temp)

    return post_content


def get_content(link_content):
    #获取微博正文
    res = requests.get(link_content, headers=headers, cookies=cookies)
    response = Selector(text=res.text)  # 创建Selector对象
    post_content = response.xpath('//div[@id="M_"]/div/span[@class="ctt"]').extract()[0]
    return content_re(post_content)


if __name__ == '__main__':
    # get_weibo_post('https://weibo.cn/eauthermaleavene')
    for url in URL_LIST:
        get_weibo_info(url)
        time.sleep(1)
    # get_weibo_post('https://weibo.cn/eauthermaleavene', 1)