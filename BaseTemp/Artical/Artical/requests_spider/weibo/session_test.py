#-*- coding:utf-8 -*-

import requests
import re
import time
import datetime
import http.cookiejar as cookielib

#session 保持长链接访问
s = requests.Session()
s.cookies = cookielib.LWPCookieJar(filename='cookies.txt')
headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    }

def weibo_login(user, passwd):
    #登录微博，获取cookie
    s.get('https://passport.weibo.cn/signin/login', headers=headers)
    post_data = {
        'username': user,
        'password': passwd,
        'savestate': '1',
        'ec': '0',
        'entry': 'mweibo',
        'mainpageflag': '1',
    }
    post_url = 'https://passport.weibo.cn/sso/login'
    response_text = s.post(url=post_url, headers=headers, data=post_data)
    res = s.get('https://weibo.cn/eauthermaleavene',headers=headers)
    print(res.text)


def get_weibo_post(link,page_num):
    #获取指定微博的全部信息
    #page_num要爬取的页面总数， link微博主页链接
    pass

def get_weibo_info(link):
    # 获取指定微博的基本信息
    pass


if __name__ == '__main__':
    pass