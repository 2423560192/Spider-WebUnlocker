import os
import time
from urllib.parse import urljoin
import pandas as pd
from jsonpath import jsonpath
from db import DB
from concurrent.futures import ThreadPoolExecutor
import requests
from 普通爬虫.防消易平台.kuaidaili import get_ip


def get_img(creditCode, url):
    img_url = urljoin('https://xf.jintongxinxi.com/', url)  # 使用 urljoin 来构建完整的图片 URL
    try:
        response = requests.get(img_url, stream=True)
        response.raise_for_status()  # 确保请求成功
        with open(f'images-待整改/{creditCode}.jpg', 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(creditCode, '图片保存完毕!')
    except requests.exceptions.RequestException as e:
        print(creditCode, f"下载图片失败，错误信息：{e}")


def get_detail(id, url):
    get_img(id, url)


def worker(id, url):
    get_detail(id, url)  # 获取公司详情


if __name__ == '__main__':
    # 初始化数据库
    db = DB()
    conn, cursor = db.connect()
    # 查询数据库表
    insert_query = '''
              SELECT * FROM subsidy_info4;
            '''
    cursor.execute(insert_query)
    tbs = cursor.fetchall()

    lst = []
    for i in tbs:
        if i[3] != '':
            lst.append([i[1], i[3]])

    print(len(lst))

    res = []
    for i in os.listdir('images-待整改'):
        res.append(i.split('.')[0])

    print(len(res))
    # 使用线程池管理并发任务
    with ThreadPoolExecutor(max_workers=100) as executor:
        # 提交任务到线程池

        for id, url in lst:
            if id in res:
                continue
            executor.submit(worker, id, url)
            time.sleep(0.01)  # 每秒 100 次任务，控制提交速率
