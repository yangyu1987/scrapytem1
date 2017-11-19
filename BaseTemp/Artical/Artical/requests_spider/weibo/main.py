#-*- coding:utf-8 -*-
import time
from multiprocessing import Pool
import setting

from spider_new import start_url
from url_lists import START_URL_LIST

# def main_spider(link):
#     #装载urllist进行爬取，单进程
#     for url in link:
#         try:
#             get_weibo_info(url)
#             print('开始爬取' + url)
#             time.sleep(10)
#         except:
#             pass
#     print('爬取任务结束')

#多进程


if __name__ == '__main__':
    # main_spider(URL_LIST)
    pool = Pool()
    while True:
        pool.map(start_url,START_URL_LIST)
        print('爬虫休眠中')
        time.sleep(50)