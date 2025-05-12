import time

import requests

from jsonpath import jsonpath


def save_data(data):
    for i in data:
        wb.append(i)
    ws.save('待整改.xlsx')


def get_data():
    import requests

    headers = {
        'Host': 'xf.jintongxinxi.com',
        'xweb_xhr': '1',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiIxMjA5NDciLCJzaWQiOiIxMjA5NDdfMTAwMl8xNTUwOTYwODEyODk0NDY0MDVfMTYwMjEzMjI2MDczNjIxNTA5IiwianRpIjoiIiwiaXNzIjoiNjY2NjY2NjYiLCJzdWIiOiIiLCJhdWQiOiIiLCJuYmYiOjE3MzQ5NTYxNDAsImV4cCI6MTczNTQ3NDg0MH0.d-K-p3XcQD75Y9G80u7AR_B1ZjhkACu2ctnwsCQNAGg',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c11)XWEB/11581',
        'Content-type': 'application/json;charset=UTF-8',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://servicewechat.com/wx49d7d6daf888d0e3/79/page-frame.html',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    params = {
        'pageIndex': '1',
        'pageSize': '1600',
        'risktype': '1001',
        'checkstatus': '1002,1003,1004',
        'industry': '',
        'keyword': '',
    }

    response = requests.get('https://xf.jintongxinxi.com/apiv1/Risk/GetSelfRiskInfoList', params=params,
                            headers=headers)

    # print(response.json())
    data = response.json()
    creditCode = jsonpath(data, '$..rows..creditCode')
    companyName = jsonpath(data, '$..rows..companyName')
    dutyPerson = jsonpath(data, '$..rows..dutyPerson')
    phone = jsonpath(data, '$..rows..phone')
    address = jsonpath(data, '$..rows..address')

    print(len(creditCode))
    print(len(companyName))
    print(len(dutyPerson))
    print(len(phone))
    print(len(address))
    lst = []
    for code, name, person, ph, add in zip(creditCode, companyName, dutyPerson, phone, address):
        lst.append([code, name, person, ph, add])
    save_data(lst)


if __name__ == '__main__':
    from openpyxl import Workbook

    ws = Workbook()
    wb = ws.active
    wb.append(['ID', '公司名', '管理人', '电话', '地址位置'])
    ws.save('待整改.xlsx')
    get_data()