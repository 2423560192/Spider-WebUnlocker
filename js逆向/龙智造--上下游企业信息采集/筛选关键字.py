import ast
import random
import time
import threading

import requests
from jsonpath import jsonpath
import json
from openpyxl import workbook
import pandas as pd

h = {
    'authority': 'holmes.taobao.com',
    'accept': 'application/json, text/plain',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://www.dingtalk.com',
    'referer': 'https://www.dingtalk.com/',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36',
    # 'Cookie': 'arms_uid=34de0031-5b6f-4567-8a77-b3dd28bc4a41; cna=hFmlHOLVInoCAX1SeRZobwyo; xlly_s=1; account=oauth_k1%3AwnXaaW3blywVOjX0%2F7Po29q2pl7cUdUJ7D3WdtMvC40gk6g%2FK8J9LsBmy59fbsWoi6eImp7ELVr7Z4Y8%2Btd64mu3ahSLWDPpBm%2FGyPnaDfg%3D; deviceid=dad47dd1bf0342e8a5aa558cad972baf; pub_uid=1Tn4R6fToK22KVSaGmegHQ%3D%3D; isg=BImJ5jNBCUBfk_W5UMRE8PbqmLXj1n0IlYmPtCv-TXCvcqmEcyIx2HKjsNZEKhVA; l=fBIgMkbnN1suSeEKBOfwPurza77txIRAguPzaNbMi9fP935H5ihdW1aTkuLMCnGVFsOBR3l39SNMBeYBqQd-nxv9pEcBudMmnmOk-Wf..; tfstk=c4GOBJNeIHxiSLt0T5phursA66LlZPBT0trfMfUOQtTyEo1AizcowZSkurqzXeC..'
}
res = []
import json


# 保存数据
ws = workbook.Workbook()
wb = ws.active
demain_info = []

# 读取表格信息
def reads_excel():
    data = pd.read_excel(io='爬虫实习生1组任务.xlsx')
    # print(data)
    for i,j in data.iterrows():
        dic = {}
        dic['key'] = j['关键词']
        dic['category'] = j['行业大类']
        dic['category_small'] = j['行业小类']
        dic['place'] = j['地域']
        dic['status'] = j['上下游']
        demain_info.append(dic)

def get_data(url, p,place,kind,category):
    html_data = requests.post(url, headers=h, data=json.dumps(p))
    time.sleep(0.3)
    if html_data.status_code == 200:
        data = html_data.json()
        print(data)
        values = jsonpath(data, '$..data.data[0:10]..ocid')
        # 保存
        for v in values:
            wb.append([v,place,kind,category])
            ws.save('上下游企业-接口id-上游.xlsx')


def main():
    global p
    reads_excel()
    url = 'https://holmes.taobao.com/web/corp/customer/searchWithSummary'
    for demain in demain_info[0:3]:
        print(demain)
        lst_places = demain['place'].split('、')
        for pl in lst_places:
            if '省' in pl:
                p = {
                    "pageNo": 1,
                    "pageSize": 10,
                    "keyword": demain['key'],
                    "orderByType": 5,
                    "region": {
                        "province": pl,
                        "city": None,
                        "area": None
                    },
                    "bizCategory": {
                        "bigCategory": demain['category'],
                        "smallCategory": demain['category_small'],
                    }
                }
            elif '市' in pl:
                p = {
                    "pageNo": 1,
                    "pageSize": 10,
                    "keyword": demain['key'],
                    "orderByType": 5,
                    "region": {
                        "province": pl,
                        "city": pl,
                        "area": None
                    },
                    "bizCategory": {
                        "bigCategory": demain['category'],
                        "smallCategory": demain['category_small']
                    }
                }
            try:
                i = 1
                while True:
                    p['pageNo'] = i
                    get_data(url, p,pl,demain['status'],demain['category_small'])
                    i += 1
            except:
                print('已爬取完毕!')


if __name__ == '__main__':
    # t1 = threading.Thread(target=main,args=)
    main()
