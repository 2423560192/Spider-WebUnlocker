import requests
from jsonpath_ng import parse

from utils.crypt import encrypt, decrypt


def get_resp_data():
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
        'referer': 'https://servicewechat.com/wxbea389fff6410981/15/page-frame.html',
        'accept-language': 'zh-CN,zh;q=0.9',
    }

    p_data = {'subject': 'en', 'level': '高中',
              'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTE2Mjk2LCJpYXQiOjE3NDMwODk0MjIuMTYwMDg2NiwidGltZW91dCI6MjU5MjAwMCwidHlwZSI6MX0.TAJ1VEgtyEWIjri0yxVUXfeQVtqNObSQZ-WYGspB5lY'}

    p_data = encrypt(p_data)
    json_data = {
        'data': p_data,
    }

    response = requests.post('https://api.smallschoolbag.com/v2/a12/publishing/list/', headers=headers, json=json_data)

    return response.json()['data']


def get_parse_data(data):
    # 提取所有版本信息
    book_expr = parse('$.list[*]')
    books = [match.value for match in book_expr.find(data)]
    # 只保留需要的字段
    selected_fields = ['id', 'publishing']
    result = [
        {field: book[field] for field in selected_fields}
        for book in books
    ]
    return result


def get_data():
    data = get_resp_data()
    data = decrypt(data)
    result = get_parse_data(data)
    return result
