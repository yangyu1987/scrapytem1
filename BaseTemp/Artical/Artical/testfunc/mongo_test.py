# -*- conding:utf-8 -*-

import pymongo

client = pymongo.MongoClient('localhost',27017)
weibo = client['weibo_info']#建立数据库 选择
url = weibo['url']#建一个表 选择
#
# weibo_infos = client['weibo_info']  # 建立数据库 选择
# posts = weibo_infos['post']  # 建一个表 选择

# mogo = Mogo_helper('sina','info')
#
# with open ('sina.html','r') as f:
#     lines = f.readlines()
#     for index,line in enumerate(lines):
#         print("发起请求")
#         data = {
#             'index':index,
#             'line':line,
#             'words':len(line)
#         }
#         mogo.save_data(data)



#监控
# while True:
#     # for i, item in enumerate(sheet_line.find()):
#     #     print(i)
#     print(posts.find().count())
#     time .sleep(1)
