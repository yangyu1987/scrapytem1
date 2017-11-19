# -*- conding:utf-8 -*-

import time

from weibo.common import Mogo_helper

mogo = Mogo_helper('sina','info')


#监控
while True:
    # for i, item in enumerate(sheet_line.find()):
    #     print(i)
    print(mogo.data_count())
    time .sleep(1)
