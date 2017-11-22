# -*- conding:utf-8 -*-
import time
import pymongo

client = pymongo.MongoClient('localhost',27017)

imdb = client['imdb']
movie = imdb['movie1']

#监控
while True:
    # for i, item in enumerate(sheet_line.find()):
    #     print(i)
    print('已抓取%s条数据'%movie.find().count())
    time .sleep(1)