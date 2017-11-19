#-*- coding:utf-8 -*-
import requests

proxy1 = {

    'http':'http://183.152.173.247:808'
}
from header_list import get_header

headers = get_header()
res = requests.get('https://www.douban.com/',headers = headers,proxies = proxy1)
print(res.cookies)
# res.encoding('utf-8')