#! -*- coding:utf-8 -*-
from weibo.common import *


def content_re(content):
    #除去微博正文html标签和开头的：号
    content_temp = re.compile('</?\w+[^>]*>').sub('', content)
    content = re.compile('^:').sub('', content_temp)
    content = content.replace(' ', '').replace(r'\n', '')
    return content


with open('sina.html','r') as f:
    sina = f.read()
    # print(sina)

s = 'dsadsauiedhns212183你啊号\n\t'
print(s)