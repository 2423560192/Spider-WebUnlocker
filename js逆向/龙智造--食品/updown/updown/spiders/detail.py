"""爬取企业基础信息"""
import time

import scrapy
import pandas as pd
import json
from jsonpath import jsonpath
from updown.items import Baseinfo
import requests


class MyspiderSpider(scrapy.Spider):
    name = "detail"
    allowed_domains = ["dingtalk.com"]
    # start_urls = ["http://dingtalk.com/"]
    # 起始url
    one_url = 'https://holmes.taobao.com/web/detail/companyDetailCardBatch'
    two_url = 'https://holmes.taobao.com/web/corpquery/company/category3'
    # 参数信息
    p1 = {
        "dataModuleIds": [
            482,
            483,
            484,
            486,
            453,
            485
        ],
        "type": "web",
        "pageNo": 1,
        "pageSize": 10,
        "params": [
            {
                "key": "onecomp_id",
                "value": None
            }
        ]
    }
    p2 = {
        'ocid': None
    }

    def start_requests(self):
        global ips
        ips = requests.get(
            url='http://api.66daili.cn/API/GetSecretProxy/?orderid=l85l2OO4923Ol972824&num=20&token=66daili&format=text&line_separator=win&protocol=http&region=domestic')
        for ip in ips.text.split('\r\n'):
            ipPool.append('http://' + ip)
        df = pd.read_excel('总.xlsx')
        i = 0
        items = Baseinfo()
        for i, j in df.iterrows():
            print(str(int(j['id'])))
            self.p1["params"][0]['value'] = str(int(j['id']))
            # self.p1["params"][0]['value'] = 1190959000046852568
            self.p2['ocid'] = str(int(j['id']))
            # self.p2['ocid'] = 1190959000046852568
            items = Baseinfo()
            items['city'] = '重庆市'
            items['prevence'] = '-'
            items['area'] = j['区域']
            items['state'] = '在营'
            items['category'] = '上游'
            items['now_id'] = str(int(j['id']))
            num = 0
            yield scrapy.Request(url=self.two_url, method='post', callback=self.parse_one, meta={'items': items,'num': num},
                                 body=json.dumps(self.p2), dont_filter=True)



            i += 1
            if i == 20:
                break

    # 获取企业信息1
    def parse_one(self, response):
        data = response.json()
        print(data)
        items = response.meta['items']
        name = jsonpath(data, '$..data..companyName')[0]  # 企业名称
        phone = jsonpath(data, '$..data..phoneList')  # 手机号
        email = jsonpath(data, '$..data..emailList')  # 邮箱
        reg_money = jsonpath(data, '$..data..registerCapital')[0]  # 注册金额
        entBrief = jsonpath(data, '$..data..entBrief')[0]  # 企业简介
        big_category = jsonpath(data, '$..data..industryOne')[0]  # 行业大类
        small_category = jsonpath(data, '$..data..industryTwo')[0]  # 行业小类
        addr = jsonpath(data, '$..data..address')[0]  # 行业小类
        if str(phone) != '[None]':
            items['phone'] = ','.join(phone[0])
        if str(email) != '[[]]':
            items['email'] = ','.join(email)
        if name:
            items['name'] = name
        if reg_money:
            items['reg_money'] = reg_money
        if entBrief:
            items['entBrief'] = entBrief
        if big_category:
            items['big_category'] = big_category
        if small_category:
            items['small_category'] = small_category
        if addr:
            items['addr'] = addr
        # print(name, phone, email, reg_money, entBrief, big_category, small_category, addr)
        yield scrapy.Request(url=self.one_url, method='post', callback=self.parse_two, meta={'items': items},
                             body=json.dumps(self.p1), dont_filter=True)



    # 基础信息2
    def parse_two(self, response):
        data = response.json()
        # no_da = str(data)
        print(data)
        items = response.meta['items']
        info_key = jsonpath(data, '$..data.[0].fields..title')  # 基本信息表头字段
        detail_info = jsonpath(data, '$..data[0]..rows.0[1:19]')  # 法定代表人单独
        i = 1
        for k, v in zip(info_key[1:], detail_info):
            if i in [5, 12, 18]:
                if k == '统一社会信用代码':
                    items['oid'] = v
                elif k == '人员规模':
                    items['num'] = v
                elif k == '经营范围':
                    items['business'] = v
            i += 1
        lst = []
        for k in list(Baseinfo.fields.keys()):
            if k not in items.keys():
                items[k] = '-'
        yield items



if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute('scrapy crawl detail --nolog'.split())
