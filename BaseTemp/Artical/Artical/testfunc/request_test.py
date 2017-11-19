#! -*- coding:utf-8 -*-
import time
from datetime import datetime
import requests
import re
# headers = {
# 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
# }
# ck ='_T_WM=eeb5d45975518d05a5e2713daecd50f5; SCF=AsQR6i4BRxLD8_mqVTPrQ8xEH-0sid22myGpYHOykLJRtScnbXp2VahEmBbyNaBX4ZbVtBXPU-fTYfi5-GBitsg.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWQPLQNUQqHss7CvCAesHdB5JpX5KzhUgL.Fo-XSK.Nehq4SKz2dJLoIEBLxKBLBonL1-eLxKBLB.2LB-eLxK-LBo5L12qLxK-LB--L1h-t; WEIBOCN_WM=3349; H5_wentry=H5; backURL=http%3A%2F%2Fm.weibo.cn%2F; SUB=_2A253B3kQDeThGeNP6lcV9ijNyzuIHXVUCAdYrDV6PUJbkdBeLWzMkW0cysc6VpQ57OFZzLFeoZ-J9JXBxA..; SUHB=03oVv0-Gj1sGHa; SSOLoginState=1510148416'
# cookies = dict(i.strip().split('=') for i in ck.strip().split(';'))
# res = requests.get('https://weibo.cn/eauthermaleavene',cookies=cookies,headers=headers)
# print(res.text)

print(int(time.time()*1000))
print(datetime.now().second)
# 1510249138857
# 1510253095.7848446

from header_list import get_header

headers = get_header()

r = requests.get('https://www.toutiao.com/',headers=headers)

print(r.status_code)
# print(r.content.decode('utf-8'))
# print(r.text)
t = r.text


