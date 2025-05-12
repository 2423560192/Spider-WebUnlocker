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
df = pd.read_excel('竞争.xlsx')
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
            'authority': 'holmes.taobao.com',
            'accept': 'application/json, text/plain',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/json',
            'cookie': 'cna=hFmlHOLVInoCAX1SeRZobwyo; lgc=tb256721506; tracknick=tb256721506; t=05bd17d0eb125168fa7cd87059cbdca7; sgcookie=E1007p2fECijRNxbp9O1DDOfsVHbal%2Fub49b3ZDuVHI3DQ61%2FoIwVYXeerXVqhMNNPvdhctN6yFttJrZLJpae9NpkrMhbO%2FTw3gna3a9zIaL3GE%3D; uc3=lg2=WqG3DMC9VAQiUQ%3D%3D&id2=UUphzOV5nsYb%2Bf81eg%3D%3D&vt3=F8dCsf5%2BvGtOJIa4DWc%3D&nk2=F5RHpC2cIoejhjw%3D; uc4=nk4=0%40FY4MthPoY97ivHUhM%2Bj5AzTZCUJOEg%3D%3D&id4=0%40U2grF862PT9uTiwTjVJofx70LDnGzgKh; _cc_=UIHiLt3xSw%3D%3D; isg=BPX1oyCn_Rdxkxl_qTQ1aVKzBHGvcqmEDfqucXca6my7ThRAP8LlVNaHmBL4DsE8; XSRF-TOKEN=f96fdcd9-f64f-4909-b25d-20dcc5f8eb3f',
            'origin': 'https://www.dingtalk.com',
            'referer': 'https://www.dingtalk.com/',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': random.choice(self.pc_USE_AGENT),
        }

        # 行政处罚
        self.url4 = 'http://holmes.taobao.com/web/detail/companyDetailCardBatch'
        self.p4 = {
            "dataModuleIds": [
                520,
                463,
                464,
                466,
                467,
                511,
                510,
                514,
                509,
                515,
                697,
                469,
                465
            ],
            "type": "web",
            "pageNo": 1,
            "pageSize": 10,
            "params": [
                {
                    "key": "onecomp_id",
                    "value": "1180716010221044173"
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
            else:
                break

    # 爬取融资数据
    def parse_rongzi_data(self, url, p, id):
        try:
            global sign
            # 隧道域名:端口号
            tunnel = "p800.kdltps.com:15818"

            # 用户名密码方式
            username = "t18982054986441"
            password = "tqr9zm78"
            proxy = {
                "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel},
                "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel}
            }
            html_data = requests.post(url=url, headers=self.h, data=json.dumps(p),proxies=proxy)
            if html_data.status_code == 200:
                data = html_data.json()
                print(data)
                break_lows = jsonpath(data, '$..data.1.rows[0:]')
                if break_lows:
                    for j in break_lows:
                        items = {}
                        items['oid'] = id
                        items['num'] = j[1]
                        items['kind'] = j[2]
                        items['decison_to'] = j[3]
                        items['date'] = j[4]
                        self.save_data(items)


                else:
                    items = {}
                    items['oid'] = id
                    items['num'] = '-'
                    items['kind'] = '-'
                    items['decison_to'] = '-'
                    items['date'] = '-'
                    sign = False
                    self.save_data(items)
        except:
            self.parse_rongzi_data(url,p,id)

    def save_data(self, item):
        global cursor, db
        info = [item['oid'], item['num'], item['kind'], item['decison_to'], item['date']]
        print(info)
        sql = 'insert into 企业行政信息(企业统一社会信用代码,决定文书号,行政处罚种类,决定机关,决定日期) values ("%s","%s","%s","%s","%s")'
        cursor.execute(sql, info)
        db.commit()

    def main(self):
        global sign
        # 打开表格，获取里面的信息
        for k in lst:
            sign = True
            print('当前id: ', k['id'])
            k['id'] = int(k['id'])
            self.base_data(k)


if __name__ == '__main__':
    # ips = requests.get(
    #     url='http://api.66daili.cn/API/GetSecretProxy/?orderid=l85l2OO4923Ol972824&num=20&token=66daili&format=text&line_separator=win&protocol=http&region=domestic').text
    # ips = ips.split('\r\n')
    db = pymysql.connect(
        user='root',
        password='root',
        database='panco',
        host='127.0.0.1',
        port=3306,
    )
    cursor = db.cursor()
    # 创建数据库表
    try:
        sql = 'create table 企业行政信息(id int not null auto_increment primary key,企业统一社会信用代码 varchar(255) ,决定文书号 varchar(255),行政处罚种类 varchar(255),决定机关 varchar(255),决定日期 varchar(255))'
        cursor.execute(sql)
    except Exception as e:
        print('表已存在!', e)
    spider = Spider()
    spider.main()
