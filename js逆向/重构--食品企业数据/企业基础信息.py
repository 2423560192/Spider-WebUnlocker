import random
import time

import pandas as pd
import json

import pymysql as pymysql
from jsonpath import jsonpath
import requests
from openpyxl import workbook
import threading
requests.packages.urllib3.disable_warnings()

pc_USE_AGENT = [
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

h = {
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
    'user-agent': random.choice(pc_USE_AGENT),
    'Connection': 'close'
}

one_url = 'http://holmes.taobao.com/web/detail/companyDetailCardBatch'
two_url = 'http://holmes.taobao.com/web/corpquery/company/category3'
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
num = 0


def get_ip():
    ips = requests.get(
        url='http://api.66daili.cn/API/GetSecretProxy/?orderid=l85l2OO4923Ol972824&num=20&token=66daili&format=text&line_separator=win&protocol=http&region=domestic').text
    ips = ips.split('\r\n')
    print(ips)
    return ips


def start():
    df = pd.read_excel('总.xlsx')
    # ips = get_ip()
    for i, j in df.iterrows():
        print(str(int(j['id'])))
        items = {}
        p1["params"][0]['value'] = str(int(j['id']))
        # p1["params"][0]['value'] = 1190959000046852568
        p2['ocid'] = str(int(j['id']))
        # p2['ocid'] = 1190959000046852568
        items['city'] = '重庆市'
        items['prevence'] = '-'
        items['area'] = j['区域']
        items['state'] = '在营'
        items['category'] = '上游'
        items['now_id'] = str(int(j['id']))
        parse_one(two_url, p2, items)

# 获取企业信息1
def parse_one(url, p, items):
    # try:
    #     ips.remove('')
    # except:
    #     pass
    # ip = random.choice(ips)
    # proxy = {
    #     'http': f'http://{ip}',
    #     'https': f'https://{ip}',
    # }
    # print(proxy)
    try:
        response = requests.post(url, headers=h, data=json.dumps(p), timeout=10, verify=False)
        time.sleep(1)
        if response.status_code == 200:
            data = response.json()
            print(data)
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
            parse_two(one_url, p1, items)
        else:
            print("该ip无效")
    except Exception as e:
        print(e)
        parse_one(url, p, items)


# 基础信息2
def parse_two(url, p, items):
    # try:
    #     ips.remove('')
    # except:
    #     pass
    # ip = random.choice(ips)
    # proxy = {
    #     'http': f'http://{ip}',
    #     'https': f'https://{ip}',
    # }
    # print(proxy)
    try:
        response = requests.post(url=url, headers=h, data=json.dumps(p), timeout=10, verify=False)
        time.sleep(1)
        if response.status_code == 200:
            # time.sleep(1)
            data = response.json()
            print(data)
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
            lst = [
                'city', 'prevence', 'area', 'state', 'category', 'now_id'
                , 'phone', 'email', 'name', 'reg_money', 'entBrief',
                'big_category', 'small_category', 'addr',
                'oid', 'num', 'business'
            ]
            for i in lst:
                if i not in items.keys():
                    items[i] = '-'
            save_data(items)
        else:
            # print(ip + "无效")
            pass
    except:
        parse_two(url, p, items)


def save_data(item):
    info = [item['city'], item['prevence'], item['area'], item['state'], item['category'], item['now_id']
        , item['phone'], item['email'], item['name'], item['reg_money'], item['entBrief'],
            item['big_category'], item['small_category'], item['addr'],
            item['oid'], item['num'], item['business']]
    print(info)
    try:
        sql = 'insert into 企业基础信息(市级, 省级,区级,状态,分类,ids, 电话,邮箱,企业名称,注册金额,企业简介,行业大类,行业小类,地址, 统一社会信用代码,从业人数,经营范围) values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'
        cursor.execute(sql, info)
        db.commit()
    except Exception as e:
        print(1)




if __name__ == '__main__':
    # db = pymysql.connect(
    #     user='root',
    #     password='root',
    #     database='panco',
    #     host='127.0.0.1',
    #     port=3306,
    # )
    # cursor = db.cursor()
    # try:
    #     sql = 'create table 企业基础信息(id int not null auto_increment primary key ,市级 varchar(255),省级 varchar(255),区级 varchar(255),状态 varchar(255),分类 varchar(255),ids varchar(255),电话 varchar(255),邮箱 varchar(255),企业名称 varchar(255),注册金额 varchar(255),企业简介 varchar(255),行业大类 varchar(255),行业小类 varchar(255),地址 varchar(255),统一社会信用代码 varchar(255),从业人数 varchar(255),经营范围 varchar(255))'
    #     cursor.execute(sql)
    # except Exception as e:
    #     print('表已存在!', e)
    start()
