import time
from urllib.parse import urljoin
import pandas as pd
from jsonpath import jsonpath
from db import DB
from concurrent.futures import ThreadPoolExecutor
import requests
from 普通爬虫.防消易平台.kuaidaili import get_ip


def get_img(creditCode, url, ip):
    img_url = urljoin('https://xf.jintongxinxi.com/', url)  # 使用 urljoin 来构建完整的图片 URL
    try:
        response = requests.get(img_url, proxies=ip, stream=True)
        response.raise_for_status()  # 确保请求成功
        with open(f'images/{creditCode}.jpg', 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(creditCode, '图片保存完毕!')
    except requests.exceptions.RequestException as e:
        print(f"下载图片失败，错误信息：{e}")


def get_detail(id, db):
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
        'creditcode': id,
    }

    retries = 3  # 设置重试次数
    for attempt in range(retries):
        try:
            response = requests.get(
                'https://xf.jintongxinxi.com/apiv1/Company/GetCompanyDetail',
                params=params,
                headers=headers,
                # proxies=ip,  # 使用代理 IP
                verify=False  # 可根据需要设置为 True
            )

            response.raise_for_status()  # 如果响应代码不是200, 会抛出异常
            data = response.json()

            companyName = jsonpath(data, '$..data..rows..companyName')[0]
            creditCode = jsonpath(data, '$..data..rows..creditCode')[0]
            businessLicenseImage = jsonpath(data, '$..data..rows..businessLicenseImage')[0]
            companyTypeName = jsonpath(data, '$..data..rows..companyTypeName')[0]
            dutyPerson = jsonpath(data, '$..data..rows..dutyPerson')[0]
            phone = jsonpath(data, '$..data..rows..phone')[0]
            addressInfo = jsonpath(data, '$..data..rows..addressInfo')[0]
            businessScope = jsonpath(data, '$..data..rows..businessScope')[0]

            # 构建字典
            data_dict = {
                "companyName": companyName,
                "creditCode": creditCode,
                "businessLicenseImage": businessLicenseImage,
                "companyTypeName": companyTypeName,
                "dutyPerson": dutyPerson,
                "phone": phone,
                "addressInfo": addressInfo,
                "businessScope": businessScope
            }
            print(data_dict)
            db.insert(data_dict)
            break  # 请求成功，跳出重试循环

        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"请求失败，尝试第 {attempt + 1} 次重新获取数据，错误信息：{e}")
            if attempt < retries - 1:
                # 如果请求失败且重试次数未用完，则获取新的 IP 重新尝试
                ip = get_ip()
                time.sleep(2)  # 可以根据需要增加延迟
            else:
                print("重试次数已用完，请检查问题")


def worker(id, db):
    # ip = get_ip()  # 获取代理 IP
    db.connect()
    get_detail(id, db)  # 获取公司详情
    db.close()


if __name__ == '__main__':
    # 初始化数据库
    db = DB()
    conn, cursor = db.connect()
    db.create_table()
    # 查询数据库表
    tbs = db.search()
    db.close()

    lst = []
    for i in tbs:
        lst.append(i[0])
    # 打开表
    df = pd.read_excel('信息.xlsx')
    ids = df['ID']
    # 使用线程池管理并发任务
    with ThreadPoolExecutor(max_workers=100) as executor:
        # 提交任务到线程池
        for i in ids:
            # print(f"正在处理 ID: {i}")
            if i in lst:
                continue
            executor.submit(worker, i, db)
            time.sleep(0.01)  # 每秒 100 次任务，控制提交速率
