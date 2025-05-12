"""爬取企业基础信息"""
import time

import scrapy
import pandas as pd
import json
from jsonpath import jsonpath
from updown.items import Rongzi
import requests


class MyspiderSpider(scrapy.Spider):
    name = "rongzi"
    allowed_domains = ["dingtalk.com"]
    # start_urls = ["http://dingtalk.com/"]
    # 起始url
    one_url = 'https://holmes.taobao.com/web/detail/companyDetailCardBatch'
    # 参数信息
    p = {
        "dataModuleIds": [
            503,
            502,
            472,
            471
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
    def start_requests(self,):
        df = pd.read_excel('企业基础信息.xlsx')
        k = 0
        ips = requests.get(
            url='http://api.66daili.cn/API/GetSecretProxy/?orderid=l85l2OO4923Ol972824&num=20&token=66daili&format=text&line_separator=win&protocol=http&region=domestic')
        for i, j in df.iterrows():
            print(str(int(j['ids'])))
            self.p["params"][0]['value'] = str(int(j['ids']))
            # self.p["params"][0]['value'] = 1180716000049727118
            items = Rongzi()
            items['oid'] = j['统一社会信用代码']
            yield scrapy.Request(url=self.one_url, method='post', callback=self.parse_one, meta={'items': items},
                                 body=json.dumps(self.p), dont_filter=True)
            # break
    # 获取融资信息
    def parse_one(self, response):
        items = response.meta['items']
        data = response.json()
        print(data)
        rongzi_history = jsonpath(data, '$..data.0..rows[0:]')
        if rongzi_history:
            for detail in rongzi_history:
                items['rongzi_round'] = detail[2]  # 融资轮次
                items['rongzi_money'] = detail[3]  # 融资金额
                items['investor'] = detail[5]   # 投资方
                items['date'] = detail[1]   # 发布日期
                yield items
        else:
            items['rongzi_round'] = '-'  # 融资轮次
            items['rongzi_money'] = '-'  # 融资金额
            items['investor'] = '-'  # 投资方
            items['date'] = '-'  # 发布日期
            yield items

if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute('scrapy crawl rongzi --nolog'.split())
