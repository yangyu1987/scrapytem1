# -*- conding:utf-8 -*-
import time

from weibo.common import Mogo_helper

mogo = Mogo_helper('weibo_info')


#监控
while True:
    # for i, item in enumerate(sheet_line.find()):
    #     print(i)
    print('已抓取%s条数据'%mogo.data_count('post'))
    time .sleep(1)
