#! -*- coding:utf-8 -*-

import json,xlwt


def readExcel(file):
     with open(file,'r',encoding='utf8') as fr:
         data = fr.readlines() # 用json中的load方法，将json串转换成字典
     return data


def writeM():
     a = readExcel('Post:dunhill.json')
     title = ["timestamp","account_id","post_id","post_date","post_content","post_url","like_num","comment","forward"]
     book = xlwt.Workbook() # 创建一个excel对象
     sheet = book.add_sheet('Sheet1',cell_overwrite_ok=True) # 添加一个sheet页
     for i in range(len(title)): # 循环列
         sheet.write(0,i,title[i]) # 将title数组中的字段写入到0行i列中

     cont_len = []
     for i,line in enumerate(a):
         sheet.write(i+1, 0, eval(line)['timestamp'])  # 将title数组中的字段写入到0行i列中
         sheet.write(i+1, 1, eval(line)['account_id'])
         sheet.write(i+1, 2, eval(line)['post_id'])
         sheet.write(i+1, 3, eval(line)['post_date'])
         sheet.write(i+1, 4, eval(line)['post_content'])
         cont_len.append(int(len(eval(line)['post_content'])))
         # sheet.write(i+1, 5, eval(line)['post_url'])
         sheet.write(i+1, 6, eval(line)['like'])
         sheet.write(i+1, 7, eval(line)['comment'])
         sheet.write(i+1, 8, eval(line)['forward'])
     sheet.col(3).width = 200* 30
     sheet.col(4).width = max(cont_len) * 100
     # first_col = sheet.col(0)
     # sec_col = sheet.col(1)
     #
     # first_col.width = 256 * 50
     # tall_style = xlwt.easyxf('font:height 1080;')  # 36pt,类型小初的字号
     # first_row = sheet.row(0)
     # first_row.set_style(tall_style)
     book.save('Post:dunhill.xls')
     # for line in eval(a[0]):
     #     sheet.write(1, i, title[i])
     # for line in eval(a[0]): #　循环字典
     #     print('line:',line)
     #     sheet.write(int(line),0,line) #　将line写入到第int(line)行，第0列中
     #     # summ = a[line][1] + a[line][2] + a[line][3] # 成绩总分
     #     # sheet.write(int(line),5,summ) # 总分
     #     # sheet.write(int(line),6,summ/3) # 平均分
     #     for i in range(len(a[line])):
     #         sheet.write(int(line),i+1,a[line][i])
     #

if __name__ == '__main__':
     writeM()