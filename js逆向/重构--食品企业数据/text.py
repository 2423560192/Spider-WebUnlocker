"""
2023-5-30
"""
import ast
import json
import random
import time

import pymysql as pymysql
import requests
from jsonpath import jsonpath
import pandas as pd
from openpyxl import workbook
import urllib3

urllib3.disable_warnings()

import json

# 提取数据
df = pd.read_excel('上游.xlsx')
lst = []
for index, rows in df.iterrows():
    dic = dict()
    dic['id'] = rows['id']
    lst.append(dic)

sign = True


class Spider:
    def __init__(self):
        # 保存数据
        self.pc_USE_AGENT = [
            'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3451.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:57.0) Gecko/20100101 Firefox/57.0',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2999.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.70 Safari/537.36',
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.4; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.1.4322; MS-RTC LM 8; InfoPath.2; Tablet PC 2.0)',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36 OPR/55.0.2994.61',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.814.0 Safari/535.1',
            'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/418.9.1 (KHTML, like Gecko) Safari/419.3',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0; Touch; MASMJS)',
            'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1041.0 Safari/535.21',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3451.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:57.0) Gecko/20100101 Firefox/57.0',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2999.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.70 Safari/537.36',
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.4; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.1.4322; MS-RTC LM 8; InfoPath.2; Tablet PC 2.0)',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36 OPR/55.0.2994.61',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.814.0 Safari/535.1',
            'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/418.9.1 (KHTML, like Gecko) Safari/419.3',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0; Touch; MASMJS)',
            'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1041.0 Safari/535.21',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4093.3 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko; compatible; Swurl) Chrome/77.0.3865.120 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4086.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:75.0) Gecko/20100101 Firefox/75.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/91.0.146 Chrome/85.0.4183.146 Safari/537.36',
            'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 VivoBrowser/8.4.72.0 Chrome/62.0.3202.84',
            'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:83.0) Gecko/20100101 Firefox/83.0',
            'Mozilla/5.0 (X11; CrOS x86_64 13505.63.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 OPR/72.0.3815.400',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
        ]
        self.h = {
            'content-type': 'application/json',
            'cookie': 'cna=jaAYHY/bRwcCAd0HRUZG18NJ; _m_h5_tk=565627bfcfa8f287b0ae1b14a1795c82_1693041914347; _m_h5_tk_enc=c40d429f0955786436310f516e590be5; x5sec=7b22617365727665723b32223a223935623738306539323333636466383863326439663838303732623330363039434f542b707163474550506e772f66372f2f2f2f2f77456f674151777a3962367951524141773d3d222c22733b32223a2233353636616236366537363566383465227d',
            'origin': 'https://www.dingtalk.com',
            'referer': 'https://www.dingtalk.com/',
            'user-agent': random.choice(self.pc_USE_AGENT),
        }

        # 行政处罚
        self.url4 = 'https://holmes.taobao.com/web/detail/companyDetailCard'
        # 参数信息
        self.p4 = {
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
        self.p1 = {
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

    def base_data(self, dic):
        # 爬取融资历程
        self.p4["params"][0]['value'] = dic['id']
        i = 1
        while True:
            if sign:
                self.p4['pageNo'] = i
                self.parse_rongzi_data(self.url4, self.p4, dic['id'])
                i += 1
                time.sleep(3)

            else:
                break

    # 爬取融资数据
    def parse_rongzi_data(self, url, p, id):
        global sign

        try:
            html_data = requests.post(url=url, headers=self.h, data=json.dumps(p))
            time.sleep(0.5)
            if html_data.status_code == 200:
                data = html_data.json()
                print(data)

                break_lows = jsonpath(data, '$..data.rows[0:]')
                if break_lows:
                    for j in break_lows:
                        items = {}
                        items['ocid'] = id
                        items['stock_name'] = j[0]
                        items['stock_type'] = j[1]
                        items['should_capi'] = j[2]
                        items['stock_percent'] = j[3]
                        items['should_capi_time'] = j[4]
                        items['ent_cnt'] = j[5]

                        for k in items.keys():
                            if items[k] == '':
                                items[k] = '-'
                        self.save_data(items)


                else:
                    items = {}
                    items['ocid'] = id
                    items['stock_name'] = '-'
                    items['stock_type'] = '-'
                    items['should_capi'] = '-'
                    items['stock_percent'] = '-'
                    items['should_capi_time'] = '-'
                    items['ent_cnt'] = '-'
                    sign = False
                    self.save_data(items)
        except Exception as e:
            print(e)
            self.parse_rongzi_data(url, p, id)

    def save_data(self, item):
        global cursor, db
        info = [
            int(item['ocid']),
            item['stock_name'],
            item['stock_type'],
            item['should_capi'],
            item['stock_percent'],
            item['should_capi_time'],
            item['ent_cnt'],
        ]

        print(info)

        try:
            sql = 'insert into dd_company_stock_info(ocid,stock_name,stock_type,should_capi,stock_percent,should_capi_time,ent_cnt) values ("%s","%s","%s","%s","%s","%s","%s")'
            cursor.execute(sql, info)
            db.commit()
        except Exception as e:
            print(e)
            self.save_data(item)

    def main(self):
        global sign
        # 打开表格，获取里面的信息
        for k in lst:
            sign = True
            print('当前id: ', k['id'])
            k['id'] = int(k['id'])
            self.base_data(k)


if __name__ == '__main__':
    # dd_company_stock_info  (股东信息)
    db = pymysql.connect(
        user='root',
        password='root',
        database='my-db',
        host='127.0.0.1',
        port=3306,
    )
    cursor = db.cursor()

    spider = Spider()
    spider.main()
