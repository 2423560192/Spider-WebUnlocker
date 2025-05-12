"""爬取企业基础信息"""
import time

import scrapy
import pandas as pd
import json
from jsonpath import jsonpath
from updown.items import Judge


class MyspiderSpider(scrapy.Spider):
    name = "judge"
    allowed_domains = ["dingtalk.com"]
    # start_urls = ["http://dingtalk.com/"]
    # 起始url
    one_url = 'https://holmes.taobao.com/web/detail/companyDetailCard'
    # 参数信息
    p = {
        "dataModuleId": 456,
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
    sign = True
    num = False

    def start_requests(self):
        df = pd.read_excel('上游.xlsx')
        p = 0
        for i, j in df.iterrows():
            self.sign = True
            self.num = False
            print(str(int(j['id'])))
            self.p["params"][0]['value'] = str(int(j['id']))
            items = Judge()
            items['oid'] = j['id']
            try:
                k = 1
                while True:
                    if self.sign != True:
                        break
                    self.p['pageNo'] = k
                    yield scrapy.Request(url=self.one_url, method='post', callback=self.parse_one,
                                         meta={'items': items},
                                         body=json.dumps(self.p), dont_filter=True)
                    k += 1
            except:
                print('完毕')


    # 获取融资信息
    def parse_one(self, response):
        items = response.meta['items']
        data = response.json()
        print(data)
        break_lows = jsonpath(data, '$..data.rows[0:]')
        if break_lows:
            self.num = True
            for j in break_lows:
                items['name'] = j[2]
                items['reason'] = j[3]
                items['id'] = j[5]
                items['date'] = j[7]
                items['num'] = j[4]
                yield items
                # print(items)

        else:
            items['name'] = '-'
            items['reason'] = '-'
            items['id'] = '-'
            items['date'] = '-'
            items['num'] = '-'
            self.sign = False
            if self.num == False:
                self.num = True
                yield items

if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute('scrapy crawl judge --nolog'.split())
