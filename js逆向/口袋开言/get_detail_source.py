from jsonpath import jsonpath

from utils.crypt import encrypt, decrypt


def get_resp_data(book_id):
    import requests

    headers = {
        'Host': 'api.smallschoolbag.com',
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTE2Mjk2LCJpYXQiOjE3NDMwODk0MjIuMTYwMDg2NiwidGltZW91dCI6MjU5MjAwMCwidHlwZSI6MX0.TAJ1VEgtyEWIjri0yxVUXfeQVtqNObSQZ-WYGspB5lY',
        'xweb_xhr': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c33)XWEB/11581',
        'app': '100000',
        'phone_system_type': 'applets',
        'Content-type': 'application/json;charset=UTF-8',
        'accept': '*/*',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://servicewechat.com/wxbea389fff6410981/16/page-frame.html',
        'accept-language': 'zh-CN,zh;q=0.9',
    }
    j_data = {"sid": book_id,
              "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTE2Mjk2LCJpYXQiOjE3NDMwODk0MjIuMTYwMDg2NiwidGltZW91dCI6MjU5MjAwMCwidHlwZSI6MX0.TAJ1VEgtyEWIjri0yxVUXfeQVtqNObSQZ-WYGspB5lY"}

    json_data = {
        'data': encrypt(j_data),
    }

    response = requests.post(
        'https://api.smallschoolbag.com/a12/universal/resource/get_catalog_list/',
        headers=headers,
        json=json_data,
    )
    return response.json()['data']


def get_parse_data(data):
    # 解析 id
    ids = jsonpath(data, '$.list[*].id')
    # 解析 name
    names = jsonpath(data, '$.list[*].name')
    return ids, names


def get_data(book_id):
    data = get_resp_data(book_id)
    # 解密
    data = decrypt(data)
    # 解析数据
    ids, names = get_parse_data(data)
    return ids, names
