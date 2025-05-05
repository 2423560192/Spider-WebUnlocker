import os

import execjs
import pandas as pd

import requests
from jsonpath_ng import parse

from utils.crypt import decrypt, encrypt


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

    p_data = encrypt({
        'tid': id,
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTE2Mjk2LCJpYXQiOjE3NDMwODk0MjIuMTYwMDg2NiwidGltZW91dCI6MjU5MjAwMCwidHlwZSI6MX0.TAJ1VEgtyEWIjri0yxVUXfeQVtqNObSQZ-WYGspB5lY'
    })

    json_data = {
        'data': p_data
    }


    response = requests.post('https://api.smallschoolbag.com/a12/english/word/list/unit/list/', headers=headers,
                             json=json_data)

    data = response.json()['data']
    return data


def get_parse_data(path, data):
    # 提取所有单元
    unit_expr = parse('$.list[*]')
    units = [match.value for match in unit_expr.find(data)]

    # 创建输出目录（可选）
    output_dir = path

    # 定义所有Windows非法字符
    invalid_chars = '<>:"/\\|?*'

    for unit in units:
        # 只选择需要的字段
        selected_fields = ['word', 'chinese', 'phonetic']
        word_list_filtered = [
            {key: word[key] for key in selected_fields if key in word}
            for word in unit['word_list']
        ]

        # 转换为DataFrame
        df = pd.DataFrame(word_list_filtered)

        # 设置友好列名
        column_mapping = {
            'word': 'Word',
            'chinese': 'Chinese',
            'phonetic': 'Phonetic',
        }
        df.columns = [column_mapping[col] for col in df.columns]

        # 设置独立的Excel文件名
        # 将单元名称中的所有非法字符替换为下划线
        safe_name = unit['name']
        for char in invalid_chars:
            safe_name = safe_name.replace(char, '_')
        excel_file = f"{output_dir}/{safe_name}.xlsx"

        # 保存到单独的Excel文件
        with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Words', index=False)

            # 动态调整列宽
            worksheet = writer.sheets['Words']
            for i, col in enumerate(df.columns):
                max_length = max(df[col].astype(str).map(len).max(), len(col)) + 2
                worksheet.set_column(i, i, min(max_length, 50))  # 最大宽度限制为50

        print(f"已保存单元 '{unit['name']}' 到 {excel_file}")


def get_data(path  , id):
    data = get_resp_data(id)
    data = decrypt(data)
    get_parse_data(path , data)



