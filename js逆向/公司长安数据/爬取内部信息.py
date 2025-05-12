import json
import time

import requests
from openpyxl import workbook
from jsonpath import jsonpath
from lxml import etree
import execjs
import re

lst = []

with open('niumo.txt', encoding='utf-8') as f:
    line = f.readlines()
    cookie = line[0].strip()
    for i in line[1:]:
        lst.append(i.strip())

headers = {
    'Cookie': cookie,
    'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
    'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Referer': 'http://dms.changan.com.cn/jc/claim/dealerClaimMng/ClaimBillMaintainMain/infoAddForward.do?infoId=',
    # 'Accept-Language': 'zh-cn',
    # 'Accept-Encoding': 'gzip, deflate',
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 10.0; WOW64; Trident/4.0; .NET4.0C; .NET4.0E; Tablet PC 2.0; Core/1.94.202.400 QQBrowser/11.9.5355.400)',
    'Host': 'dms.changan.com.cn',
    # 'Content-Length': '27',
    'Connection': 'Keep-Alive',
    'Pragma': 'no-cache',

}


def get_two_data(id, dic):
    url = f'http://dms.changan.com.cn/jc/claim/dealerClaimMng/ClaimBillMaintainMain/freeMaintainHistory.do?VIN={id}'
    resp = requests.get(url, headers=headers)
    # print(resp.text)
    lxml = etree.HTML(resp.text)
    tr = lxml.xpath('//tr')[3:-2]
    with open('ceshi.js', 'r', encoding='utf-8') as f:
        js = f.read()
    for i in tr[-1:]:
        lst = i.xpath('.//td//text()')
        print(lst)
        a = 0
        for j in lst:
            b = j.strip()
            print(a,b)
            if 'writeItemValue' in b:
                # print(b)
                js_ = execjs.compile(js)
                now_id = re.findall(r'writeItemValue\((.*?)\)', str(b))[0]
                # print(now_id)
                lst[a] = js_.call('writeItemValue', now_id)
            a += 1
        dic['经销商代码'] = lst[1].strip()
        dic['经销商名称'] = lst[2].strip()
        dic['工单号码'] = lst[3].strip()
        dic['日期'] = lst[4].strip()
        dic['单据类型'] = lst[6].strip()
        dic['工单状态'] = lst[9].strip()
        dic['预授权状态'] = lst[7].strip()
        dic['行驶里程'] = lst[14].strip()
        dic['保养次数'] = lst[15].strip()
        dic['变更记录'] = lst[17].strip()
        dic['废弃记录'] = lst[20].strip()
        print(dic)
        save_data(dic)
        time.sleep(1)


def save_data(dic):
    info = list(dic.values())
    wb.append(info)
    ws.save('数据.xlsx')


def get_data():
    url = 'http://dms.changan.com.cn/jc-report/report/reportmng/DynamicReportMng/doQuery.json?curPage=1'
    for i in lst:
        print('当前正在爬取', i)
        data = {
            'reportId': '2011051117955846',
            'userId': '4000024920',
            'dealerId': '2014120905542000',
            'VV': i,
            'orderCol': '',
            'order': '',
        }
        dic = {}
        resp = requests.post(url, data=data, headers=headers)
        print(resp.text)
        print(resp.json()['ps']['records'])
        reps_data = resp.json()['ps']['records']
        # print(reps_data)
        for j in reps_data:
            dic = {}
            dic['VIN'] = j['A1']
            dic['车系'] = j['A2']
            dic['车型代码'] = j['A3']
            dic['车型组代码'] = j['A15']
            dic['车型组名称'] = j['A16']
            dic['生产时间'] = j['A4']
            dic['购车时间'] = j['A5']
            dic['车牌号'] = j['A14']
            dic['客户姓名'] = j['A8']
            dic['客户电话'] = j['A9']
            dic['客户地址'] = j['A10']
            dic['大区'] = j['A11']
            dic['省份'] = j['A12']
            dic['销售经销商'] = j['A13']
            dic['开票对象'] = j['A161']
            dic['车辆用途'] = j['A162']
            dic['实销录入时间'] = j['A163']
            dic['产地'] = j['A17']
            dic['交车日期'] = j['A165']
            dic['三包政策'] = j['A164']
            # get_two_data(i, dic)
            save_data(dic)

        time.sleep(1)


if __name__ == '__main__':
    ws = workbook.Workbook()
    wb = ws.active
    wb.append(['VIN', '车系', '车型代码', '车型组代码', '车型组名称', '生产时间', '购车时间',
               '车牌号', '客户姓名', '客户电话', '客户地址', '大区', '省份', '销售经销商', '开票对象', '车辆用途',
               '实销录入时间', '产地', '交车日期', '三包政策', '经销商代码', '经销商名称', '工单号码', '日期',
               '单据类型', '工单状态', '预授权状态', '行驶里程',
               '保养次数', '变更记录', '废弃记录'])
    ws.save('数据.xlsx')
    get_data()
