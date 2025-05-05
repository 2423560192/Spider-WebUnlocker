import os
import time

from jsonpath_ng import parse

from utils.crypt import encrypt, decrypt
import get_detail_source
import detail_source_download


def get_resp_data(id):
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

    j_data = {"subject": "en", "tid": id,
              "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTE2Mjk2LCJpYXQiOjE3NDMwODk0MjIuMTYwMDg2NiwidGltZW91dCI6MjU5MjAwMCwidHlwZSI6MX0.TAJ1VEgtyEWIjri0yxVUXfeQVtqNObSQZ-WYGspB5lY"}

    json_data = {
        'data': encrypt(j_data),
    }

    response = requests.post('https://api.smallschoolbag.com/a12/universal/resource/get_set_list/', headers=headers,
                             json=json_data)

    return response.json()['data']


def get_parse_data(data):
    # 创建一个新的结构来存储按 name 和 list 提取的结果
    result = []

    # 使用 jsonpath 提取每个 name 和它对应的 list
    jsonpath_expr = parse('$.list[*]')  # 匹配顶层 list 里的每个对象
    matches = jsonpath_expr.find(data)

    for match in matches:
        item = match.value
        # 提取 name 和对应的嵌套 list
        extracted_item = {
            "name": item["name"],
            "list": item["list"]
        }
        result.append(extracted_item)

    # 格式化输出

    return result


def get_data(new_path, id):
    data = get_resp_data(id)
    # 解密
    data = decrypt(data)
    # 解析数据
    res = get_parse_data(data)
    # 抓取每一个板块的资源
    for source in res:
        # 资源名
        print(source)
        source_name = source['name']
        path = os.path.join(new_path, f'下载资源/{source_name}')
        # 保存
        if not os.path.exists(path):
            os.makedirs(path)

        # 获取书id
        try:
            book_id = source['list'][0]['id']
            # 获取单元
            uni_ids, names = get_detail_source.get_data(book_id)
            # 获取具体的
            for uni_id, name in zip(uni_ids, names):
                # 保存
                uni_path = os.path.join(path, name)
                if not os.path.exists(uni_path):
                    os.makedirs(uni_path)
                detail_source_download.get_data(uni_path, uni_id)
                time.sleep(0.5)



        except Exception as e:
            print(e)

        time.sleep(1)
