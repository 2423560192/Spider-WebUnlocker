import requests
import json
from jsonpath import jsonpath


def get_data(name):
    url = f"https://api.zjzw.cn/web/api/?uri=apigkcx/api/gkv3/whole/lists&request_type=1&province_id=50&keyword={name}&signsafe=66250014be8cae2b35e2f2c50812ca69"

    payload = json.dumps({
        "signsafe": "66250014be8cae2b35e2f2c50812ca69"
    })
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://www.gaokao.cn',
        'referer': 'https://www.gaokao.cn/',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    resp = response.json()
    print(resp)
    try:
        data = jsonpath(resp, '$..school_id')[0]
    except:
        data = '-'
    print(data)

    img_url = f'https://static-data.gaokao.cn/upload/logo/{data}.jpg'
    save_img(img_url, name)


def save_img(img_url, name):
    sql = 'update datainfo set picurl = %s where outline = %s'
    cursor.execute(sql, (img_url, name))
    conn.commit()


# 链接数据库
import pymysql

if __name__ == '__main__':
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='5201314',
        database='java-test',
        charset='utf8'
    )
    cursor = conn.cursor()  # 获取
    sql = 'select outline from datainfo'
    cursor.execute(sql)
    names = cursor.fetchall()
    for i in names[142:]:
        get_data(i[0])
        # break
