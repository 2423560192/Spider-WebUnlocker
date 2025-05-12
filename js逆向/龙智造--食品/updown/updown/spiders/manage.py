"""爬取企业基础信息"""
import time

import scrapy
import pandas as pd
import json
from jsonpath import jsonpath
from updown.items import Manage


class MyspiderSpider(scrapy.Spider):
    name = "manage"
    allowed_domains = ["dingtalk.com"]
    # start_urls = ["http://dingtalk.com/"]
    # 起始url
    one_url = 'https://holmes.taobao.com/web/detail/companyDetailCard'
    # 参数信息
    p = {
        "dataModuleId": 520,
        "params": [
            {
                "key": "onecomp_id",
                "value": "None"
            }
        ],
        "type": "web",
        "pageNo": 1,
        "pageSize": 10
    }
    # 标志
    sign = True

    def start_requests(self):
        df = pd.read_excel('总.xlsx')
        i = 0
        for i, j in df.iterrows():
            print(str(int(j['id'])))
            # self.p["params"][0]['value'] = str(int(j['id']))
            self.p["params"][0]['value'] = 1180716000049727118
            items = Manage()
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
                    # time.sleep(2)
            except:
                print('完毕')
            break

    # 获取融资信息
    def parse_one(self, response):
        items = response.meta['items']
        data = response.json()
        abnormal_run = jsonpath(data, '$..data.rows[0:]')
        print(abnormal_run)
        if abnormal_run:
            for j in abnormal_run:
                items['date_to'] = j[1]
                items['reason_to'] = j[2]
                items['decison_to'] = j[5]
                items['dete_out'] = j[3]
                items['reason_out'] = j[4]
                items['decison_out'] = j[5]
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

    cmdline.execute('scrapy crawl manage --nolog'.split())
