import pandas as pd
import requests
from jsonpath_ng import parse

from utils.crypt import encrypt, decrypt


def get_resp_data(id):
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

    p_data = encrypt({"tid": id,
                      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTE2Mjk2LCJpYXQiOjE3NDMwODk0MjIuMTYwMDg2NiwidGltZW91dCI6MjU5MjAwMCwidHlwZSI6MX0.TAJ1VEgtyEWIjri0yxVUXfeQVtqNObSQZ-WYGspB5lY"}
                     )

    json_data = {
        'data': p_data
    }

    response = requests.post('https://api.smallschoolbag.com/a12/book/catalog/', headers=headers,
                             json=json_data)

    data = response.json()['data']
    return data


# 使用 JSONPath 解析数据
def extract_json_data(json_data):
    # 定义要提取的字段和对应的 JSONPath 表达式
    fields = {
        "id": "$.list[*].id",
        "name": "$.list[*].name",
        "page": "$.list[*].page",
        "cover": "$.list[*].cover"
    }

    # 存储提取结果
    extracted_data = {}

    # 遍历字段并提取数据
    for field, path in fields.items():
        jsonpath_expr = parse(path)
        extracted_data[field] = [match.value for match in jsonpath_expr.find(json_data)]

    return extracted_data


def save_data(data, path):
    # 将数据转换为适合 Excel 的格式
    # 因为 "total" 是一个单独的值，而其他字段是列表，我们需要调整结构
    rows = []
    for i in range(len(data["id"])):
        row = {
            "ID": data["id"][i],
            "Name": data["name"][i],
            "Page": data["page"][i],
            "Cover": data["cover"][i]
        }
        rows.append(row)
    # 使用 pandas 创建 DataFrame
    df = pd.DataFrame(rows)

    # 保存到 Excel 文件
    output_file = path + "/lesson_data.xlsx"
    df.to_excel(output_file, index=False)
    print(f"数据已保存到 {output_file}")


def get_data(id, path):
    data = get_resp_data(id)
    data = decrypt(data)
    print(data)
    # 解析数据
    parse_data = extract_json_data(data)

    save_data(parse_data, path)
