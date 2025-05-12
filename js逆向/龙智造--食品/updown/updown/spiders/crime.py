"""爬取企业基础信息"""
import time

import scrapy
import pandas as pd
import json
from jsonpath import jsonpath
from updown.items import Crime
import requests


class MyspiderSpider(scrapy.Spider):
    name = "crime"
    allowed_domains = ["dingtalk.com"]
    # start_urls = ["http://dingtalk.com/"]
    # 起始url
    one_url = 'https://holmes.taobao.com/web/detail/companyDetailCardBatch'
    # 参数信息
    p = {
        "dataModuleId": 509,
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
        df = pd.read_excel('企业基础信息.xlsx')
        i = 0
        ips = requests.get(
            url='http://api.66daili.cn/API/GetSecretProxy/?orderid=l85l2OO4923Ol972824&num=20&token=66daili&format=text&line_separator=win&protocol=http&region=domestic')
        for ip in ips.text.split('\r\n'):
            ipPool.append('http://' + ip)
        for i, j in df.iterrows():
            print(str(int(j['ids'])))
            self.p["params"][0]['value'] = str(int(j['id']))
            # self.p["params"][0]['value'] = 1180716000049727118
            items = Crime()
            items['oid'] = j['统一社会信用代码']
            try:
                yield scrapy.Request(url=self.one_url, method='post', callback=self.parse_one,
                                         meta={'items': items},
                                         body=json.dumps(self.p), dont_filter=True)
                time.sleep(0.5)
            except:
                print('完毕')

    # 获取融资信息
    def parse_one(self, response):
        items = response.meta['items']
        data = response.json()
        print(data)
        break_lows = jsonpath(data, '$..data.rows[0:]')
        if break_lows:
            for j in break_lows:
                items['date_to'] = j[1]
                items['reason_to'] = j[3]
                items['decison_to'] = j[2]
                items['dete_out'] = '-'
                items['reason_out'] = '-'
                items['decison_out'] = '-'
                yield items

        else:
            items['date_to'] = '-'
            items['reason_to'] = '-'
            items['decison_to'] = '-'
            items['dete_out'] = '-'
            items['reason_out'] = '-'
            items['decison_out'] = '-'
            self.sign = False
            yield items

if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute('scrapy crawl crime --nolog'.split())
