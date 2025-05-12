"""爬取企业基础信息"""
import time

import scrapy
import pandas as pd
import json
from jsonpath import jsonpath
from updown.items import Administration


class MyspiderSpider(scrapy.Spider):
    name = "administration"
    allowed_domains = ["dingtalk.com"]
    # start_urls = ["http://dingtalk.com/"]
    # 起始url
    one_url = 'https://holmes.taobao.com/web/detail/companyDetailCard'
    # 参数信息
    p = {
        "dataModuleId": 463,
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
            items = Administration()
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
            except:
                print('完毕')
            break

    # 获取融资信息
    def parse_one(self, response):
        items = response.meta['items']
        data = response.json()
        print(data)
        break_lows = jsonpath(data, '$..data.rows[0:]')
        if break_lows:
            for j in break_lows:
                items['num'] = j[1]
                items['kind'] = j[2]
                items['decison_to'] = j[3]
                items['date'] = j[4]
                yield items

        else:
            items['num'] = '-'
            items['kind'] = '-'
            items['decison_to'] = '-'
            items['date'] = '-'
            self.sign = False
            yield items

if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute('scrapy crawl administration --nolog'.split())
