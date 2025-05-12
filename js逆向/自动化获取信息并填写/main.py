"""
内网填写表格信息
"""
import time

import requests
from openpyxl import workbook
from jsonpath import jsonpath


def get_data(i):
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'ws_connectionid': 'null',
        'Authorization': 'bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1lIjoiMDE2NTA4Mzk0OTQ2NjIwNTcwNjgwIiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9yb2xlIjoie1wiVWlkXCI6XCIwMTY1MDgzOTQ5NDY2MjA1NzA2ODBcIixcIkFjY291bnRcIjpcIjE1NTg5NjEwOTc3XCIsXCJOYW1lXCI6XCLkur_kuLDlvanljbBcIixcIlJvbGVcIjpcIjMyLDI3LDI2LDI1LDI0LDIzLDIwLDE0LDEzLDEyXCIsXCJEZXB0XCI6XCIxODEzNzYwNzlcIixcIlRvdVhpYW5nXCI6bnVsbCxcIlBcIjowLFwiWWVXdVl1YW5cIjowLFwiR0dTVGl0bGVcIjpudWxsLFwiR0dTSW1nXCI6bnVsbCxcIlNGR0dTXCI6MH0iLCJuYmYiOjE3MzIwMDA5MTYsImV4cCI6MTczMjA1ODUxNiwiaXNzIjoiVG9uZ1lpbi5DT00iLCJhdWQiOiJFUlAifQ.DpQviz-D0DbLup8Pd2qgbMbpyvRZu4htDi-xZ1eMUxg',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
        'DNT': '1',
        'Origin': 'http://erp.ytyfcy.com',
        'Content-Type': 'application/json;charset=UTF-8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': 'http://erp.ytyfcy.com/',
    }

    params = {
        '__bianhao__': 'crmkehu',
        'current': str(i),
        'size': '30',
    }

    json_data = {
        '__bianhao__': 'crmkehu',
    }

    response = requests.post(
        'http://erp.ytyfcy.com/api/crmkehu/getsCrmKeHu',
        params=params,
        headers=headers,
        json=json_data,
        verify=False,
    )
    return response.json()


def init_excel():
    ws = workbook.Workbook()
    wb = ws.active
    wb.append(['客户外部名称', '内部名称', '联系人', '手机号', '其他电话', 'qq', '联系地址',
               '默认发货地区'])
    ws.save('crm_kehu.xlsx')
    return ws, wb


def save_data(lst):
    wb.append(lst)
    ws.save('crm_kehu.xlsx')


def parse_data(data):
    data_lst = jsonpath(data, '$..data.records')[0]
    print(data_lst)
    for i in data_lst:
        kehumingcheng = i['kehumingcheng']
        kehujiancheng = i['kehujiancheng']
        lianxiren = i['lianxiren']
        shoujihao = i['shoujihao']
        qitadianhua = i['qitadianhua']
        qq = i['qq']
        lianxidizhi = i['lianxidizhi']
        moren_addr = ''
        if i['shengfen']:
            moren_addr += i['shengfen'] + '/'
        if i['dishi']:
            moren_addr += i['dishi'] + '/'
        if i['xianqu']:
            moren_addr += i['xianqu']

        lst = [kehumingcheng, kehujiancheng, lianxiren,
               shoujihao, qitadianhua, qq, lianxidizhi, moren_addr]
        save_data(lst)


if __name__ == '__main__':
    # 初始化表格
    ws, wb = init_excel()
    for i in range(1, 244):
        print(i)
        data = get_data(i)
        # 解析数据
        parse_data(data)
        time.sleep(1)
