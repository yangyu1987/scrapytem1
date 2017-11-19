#-*- coding:utf-8 -*-
import hashlib
import json
from datetime import datetime

import requests

from weibo.common import *

headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    }

ck = 'SINAGLOBAL=8921766109525.262.1491589733363; _s_tentry=cuiqingcai.com; Apache=7116304911733.029.1509961091600; ULV=1509961092417:19:1:1:7116304911733.029.1509961091600:1508547125886; login_sid_t=489d856c936895538d74617ada4ef0ec; cross_origin_proto=SSL; wvr=6; SCF=AsQR6i4BRxLD8_mqVTPrQ8xEH-0sid22myGpYHOykLJRbGL1Dt0ywJdDC6zvwUy1zW5h9AfPsCaJkPIIaq5B-OU.; SUHB=0OM0fxkOSDD5MV; ALF=1512740417; SUB=_2A253B3kQDeThGeNP6lcV9ijNyzuIHXVUCAdYrDV8PUJbkNBeLRnDkW09G8sf8yttzu6SU6MjFhEPgFFV1Q..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Whp8H91FrFCL3XUZjgYB7Zn5JpX5oz75NHD95QfeK2fShqceK5NWs4Dqcj_i--Xi-zRiKn7i--NiK.Xi-zNi--Ri-8si-zXi--NiK.Xi-zfi--fiK.fiKnc; UOR=bbs.win10go.com,widget.weibo.com,zihaolucky.github.io'
cookies = dict(i.strip().split('=') for i in ck.strip().split(';'))
mogo = Mogo_helper('weibo_info')#建立链接 选择数据库


def start_url(link):
    #查询db中是否存在传入的链接
    link_md5 = hashlib.md5(link.encode('utf-8')).hexdigest()
    account = mogo.db['account']

    if account.find({'url_md5':link_md5}).count() == 1:
        print('此微博帐号已爬，去db取数据并发起请求')
        get_weibo_info_from_db(link)#存在，去db取数据发起请求
    else:
        print('此微博第一次爬取，直接发起请求')
        get_weibo_info(link)#不存在，直接发起请求


def get_weibo_info(link):
    # 获取指定微博的基本信息
    page_link = link + '?is_all=1'
    link_md5 = hashlib.md5(link.encode('utf-8')).hexdigest()
    res = requests.get(page_link, headers=headers, cookies=cookies)

    counter = script_html_counter(res.text).xpath('//div[@class="PCD_counter"]')  # 重新装载selector对象
    person_info = script_html_person_info(res.text).xpath('//div[@class="PCD_person_info"]')

    timestamp = datetime.now().strftime('%Y-%m-%d')
    account_id = re.match(r".*CONFIG\['oid'\]='(\d+)'", res.text, re.DOTALL).group(1)
    account_name = re.match(r".*CONFIG\['onick'\]='(.*?)'", res.text, re.DOTALL).group(1)
    following = counter.xpath('div//td[@class="S_line1"][1]/strong/text()').extract()[0]
    follwers = counter.xpath('div//td[@class="S_line1"][2]/strong/text()').extract()[0]
    post_count = counter.xpath('div//td[@class="S_line1"][3]/strong/text()').extract()[0]
    #网页结构不统一 做判断
    account_note_temp = person_info.xpath('div//p[@class="info"]/span/text()')
    if account_note_temp:
        account_note = account_note_temp.extract()[0]
    else:
        account_note = ''
    # 网页结构不统一 做判断
    account_info_temp = person_info.xpath('div//ul/li[3]/span[@class="item_text W_fl"]/text()')
    if account_info_temp:
        account_info = replace_rtn(account_info_temp.extract()[0])
    else:
        account_info = replace_rtn(person_info.xpath('div//ul/li[2]/span[@class="item_text W_fl"]/text()').extract()[0])

    page_id = re.match(r".*CONFIG\['page_id'\]='(\d+)'", res.text, re.DOTALL).group(1)
    account_en_name = link.split('/')[-1]

    account = {
        'url_md5':link_md5,
        'timestamp': timestamp,
        'account_id': account_id,
        'account_name': account_name,
        'account_url': link,
        'following': following,
        'follwers': follwers,
        'post_count': post_count,
        'account_note': account_note,
        'account_info': account_info,
        'page_id':page_id,
        'account_en_name':account_en_name
    }
    # save_account_info(account)#保存帐号信息
    print('正在抓取%s的帐号信息'%account_name)
    mogo.save_data('account',account)#保存帐号信息到account表
    # 构建ajax_url
    ajax_url_list = ajax_url(page_id,account_en_name)
    # 发起请求
    try:
        get_ajax_post(account_id,account_name,*ajax_url_list)
    except:
        pass

def get_weibo_info_from_db(link):
    # 已经爬过的帐号，从数据库中取字段构建ajax请求
    #a05a1b63723187f91d551ba0657a5fd3
    link_md5 = hashlib.md5(link.encode('utf-8')).hexdigest()
    account = mogo.db['account']
    for acc in account.find({'url_md5':link_md5}):
        # 构建ajax_url
        page_id = acc['page_id']
        account_en_name = acc['account_en_name']
        account_id = acc['account_id']
        account_name = acc['account_name']

        ajax_url_list = ajax_url(page_id,account_en_name)
        # 发起请求
        try:
            get_ajax_post(account_id,account_name,*ajax_url_list)
        except:
            pass


def get_ajax_post(account_id,account_name,*args):
    #抓取博文信息
    for ajax_page in args:
        # 向ajax页面发起请求
        response = requests.get(ajax_page, headers=headers, cookies=cookies)
        htm = json.loads(response.text)
        res = Selector(text=htm['data'])
        all_post = res.xpath('//div[contains(@class,"WB_cardwrap WB_feed_type")]')

        for weibo_post in all_post:
            # 开始解析页面
            timestamp = datetime.now().strftime('%Y-%m-%d')
            account_id = account_id
            account_name = account_name
            post_date = \
            weibo_post.xpath('div/div[@class="WB_detail"]/div[@class="WB_from S_txt2"]/a[1]/@title').extract()[0]
            post_id_temp = \
            weibo_post.xpath('div/div[@class="WB_detail"]/div[@class="WB_from S_txt2"]/a[1]/@href').extract()[0]
            post_id = re.match(r'^/\d+/(.*)\?from', post_id_temp).group(1)
            post_url_temp = \
            weibo_post.xpath('div/div[@class="WB_detail"]/div[@class="WB_from S_txt2"]/a[1]/@href').extract()[0]
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

            post_content = del_html_tag(weibo_post.xpath('div//div[@class="WB_text W_f14"]').extract()[0])
            if '展开全文' in post_content:
                mid_temp = weibo_post.xpath('div//div[@class="WB_text W_f14"]/a/@action-data').extract()[0]
                mid = re.match('.*?(\d+).*', mid_temp).group(1)
                try:
                    post_content = get_long_text(mid)
                except:
                    pass

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

            # 保存数据
            # save_post_info(data_post)
            if mogo.db['post'].find({'post_id':post_id}).count() == 1:
                print('本页已无新内容，停止本页抓取')
                print(ajax_page)
                # break
                return #结束抓取
            else:
                mogo.save_data('post',data_post)#保存到post表
                print('正在抓取%s的微博PostId:%s' % (account_name, post_id))

        time.sleep(5)


def get_long_text(mid):
    # ajax 请求获取完整博文
    # https://weibo.com/p/aj/mblog/getlongtext?mid=4141702983781428&__rnd=1510264357278
    time_param = int(time.time() * 1000)
    url = 'https://weibo.com/p/aj/mblog/getlongtext?mid={0}&__rnd={1}'.format(mid,time_param)
    response = requests.get(url, headers=headers, cookies=cookies)
    htm = json.loads(response.text)
    long_text = del_html_tag(htm['data']['html'])

    return long_text


def ajax_url(page_id,account_en_name):
    # 构建ajax请求地址
    ajax_url_list = []
    time_param = int(time.time() * 1000)

    for i in range(1, 4):
        for j in [0, 1]:
            alink = 'https://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100606&is_all=1&id={0}&script_uri=/{1}&pagebar={2}&page={3}&pre_page={4}&__rnd={5}' \
                .format(page_id, account_en_name, j, i, i, time_param)
            ajax_url_list.append(alink)

    for i in range(3):
        first_page = 'https://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100606&is_all=1&id={0}&script_uri=/{1}&page={2}&__rnd={3}' \
            .format(page_id, account_en_name, i + 1, time_param)
        ajax_url_list.insert(i * 3, first_page)

    return ajax_url_list


def save_account_info(data):
    #保存帐号信息
    text = json.dumps(data, ensure_ascii=False) + '\n'
    fileName = 'account_info'
    with open('weibo/weibo_info/' + fileName + '.json', 'ab+') as f:
        f.write(text.encode('utf-8'))
        print('保存成功')


def save_post_info(data):
    #保存具体博文信息
    text = json.dumps(data, ensure_ascii=False) + '\n'
    fileName = data.get('account_name')+ '.json'
    with open('weibo/post_info/' + fileName, 'ab+') as f:
        f.write(text.encode('utf-8'))
        print('保存成功')


if __name__ == '__main__':
    start_url('https://www.weibo.com/AlfredDunhill')
    # ajax_url_mogo('1111','yang')

