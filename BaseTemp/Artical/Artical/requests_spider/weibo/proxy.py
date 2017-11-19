# -*- coding:utf-8 -*-

import random

import requests
from scrapy.selector import Selector

from header_list import get_header
from weibo.common import Mogo_helper

#获取代理

# proxys = {
#     # 'http':'http://115.200.160.220:80',
#     'https':'https://116.231.35.5:8118'
# }
mogo = Mogo_helper('proxies')
def crawl_ip():
    #西刺代理
    for i in range(1,6):
        #抓取前5页
        headers = get_header()
        url = 'http://www.xicidaili.com/nn/{0}'.format(i)
        response = requests.get(url,headers=headers)
        res = Selector(text=response.text)
        all_trs = res.xpath('//tr[position()>1]')

        for tr in all_trs:
            ip = tr.xpath('td[2]/text()').extract()[0]
            port = tr.xpath('td[3]/text()').extract()[0]
            is_http = tr.xpath('td[6]/text()').extract()[0]

            if is_http == 'HTTP':
                ip = 'http://{0}:{1}'.format(ip,port)
                proxies = {
                    'http':ip,
                    'rd':random.random()
                }
                if mogo.db['ip'].find({'http':ip}).count() == 0:
                    mogo.save_data('ip',proxies)
                    print(mogo.data_count('ip'))

    # r = requests.get('http://ip.chinaz.com/',proxies=proxys)
    # print(r.text)
    # http://ip.chinaz.com/

class Get_ip(object):
    #从数据库中取ip 并完成验证 不符合要求的就删除
    def __init__(self):
        self.headers = get_header()

    def get_random_ip(self):
        # rd = random.random()
        # ip = mogo.db['ip'].find_one({'rd':{'$lte':rd}})
        # if ip == '':
        #     ip = mogo.db['ip'].find_one({'rd': {'$gte': rd}})
        # print(ip)

        ip =random.choice([i for i in mogo.db['ip'].find()])
        proxies = {
            'http':ip['http'],
        }
        if self.check_ip(proxies):
            return proxies
        else:
            return self.get_random_ip()


    def check_ip(self,proxies):
        #检查ip是否可用
        try:
            res = requests.get('http://www.imdb.cn'
                               '',proxies = proxies,headers = self.headers)
            res.encoding('utf-8')
            print(res.text)
        except Exception as e:
            print('IP已经失效，删除')
            self.del_ip(proxies)
            return False
        else:
            code = res.status_code
            if code >= 200 and code < 300:
                print('有效IP')
                return True
            else:
                print('IP已经失效，删除')
                self.del_ip(proxies)
                return False

    def del_ip(self,ip):
        #删除失效的IP
        mogo.db['ip'].remove(ip)



# def check_ips():
#     #检查ip是否可用
#     proxies = {'http': 'http://115.200.160.220:80'}
#     proxies1 = {
#         'http': 'http://115.200.160.220:80',
#
#     }
#     headers = get_header()
#     url = 'http://www.baidu.com'
#     r = requests.get(url,headers=headers,proxies=proxies)
#     print(r.status_code)



if __name__ == '__main__':
    # check_ips()
    proxy = Get_ip()
    print(proxy.get_random_ip())
    # proxy.check_ip({"http" : "http://116.24.80.215:8088"})
    # # print(random.random())
    # crawl_ip()