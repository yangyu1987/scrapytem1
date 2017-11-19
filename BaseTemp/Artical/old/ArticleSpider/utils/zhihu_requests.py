#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 8/11/17 11:52 PM
# @Author  : Yang

import time

import requests

try:
    import cookielib
except:
    import http.cookiejar as cookielib

import re
from PIL import Image

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies.txt')

header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Host':'www.zhihu.com'

}

def get_xsrf():
    #get_xrsf
    response = session.get('https://www.zhihu.com',headers = header)
    re_obj = '.*name="_xsrf" value="(.*?)"'
    match_obj = re.match(re_obj,response.text,re.DOTALL)
    xsrf = match_obj.group(1)
    return xsrf

def login(account, password):
    #login zhihu
    ac_obj = re.match('^1\d{10}',account)
    if ac_obj:
        post_url = 'https://www.zhihu.com/login/phone_num'
        xsrf = get_xsrf()
        captcha = get_captcha()
        post_data = {
            'xsrf':xsrf,
            'password':password,
            'phone_num':account,
            'captcha':captcha
        }
        response = session.post(post_url,post_data,headers=header)
        session.cookies.save()
        # print('phone login url'+str(post_data))
    else:
        print('email login url')

def get_captcha():
    #get captcha
    t = str(int(time.time()*1000))
    captcha_url = 'https://www.zhihu.com/captcha.gif?r={0}&type=login'.format(t)
    captcha_temp = session.get(captcha_url,headers = header)
    with open('captcha.jpg','wb') as f:
        f.write(captcha_temp.content)
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        pass

    captcha = input('captch\n')
    return captcha

def check_login():
    #check lgoin
    response = session.get('',headers = header,)

login('15251769161',123123)
# print(get_captcha())
