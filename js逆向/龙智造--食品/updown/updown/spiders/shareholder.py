"""爬取企业基础信息"""
import time

import scrapy
import pandas as pd
import json
from jsonpath import jsonpath
from updown.items import Shareholder


class MyspiderSpider(scrapy.Spider):
    name = "share"
    allowed_domains = ["dingtalk.com"]
    # start_urls = ["http://dingtalk.com/"]
    # 起始url
    one_url = 'https://holmes.taobao.com/web/detail/companyDetailCard'
    # 参数信息
    p = {
        "dataModuleId": 484,
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

    def start_requests(self):
        df = pd.read_excel('总.xlsx')
        i = 0
        for i, j in df.iterrows():
            print(str(int(j['id'])))
            # self.p["params"][0]['value'] = str(int(j['id']))
            self.p["params"][0]['value'] = 1180716000049727118
            items = Shareholder()
            items['oid'] = '123'
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
                    break
            except:
                print('完毕')
            break

    # 获取股东信息
    def parse_one(self, response):
        items = response.meta['items']
        data = response.json()
        print(data)
        break_lows = jsonpath(data, '$..data.rows[0:]')
        if break_lows:
            for j in break_lows:
                print(j)
                items['name'] = j[0]
                items['ratio'] = j[3]
                items['money'] = j[2]
                items['date'] = j[4]
                print(items)
                yield items

        else:
            items['name'] = '-'
            items['ratio'] = '-'
            items['money'] = '-'
            items['date'] = '-'
            self.sign = False
            yield items


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute('scrapy crawl share --nolog'.split())
