import pandas as pd
import requests

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

    p_data = {
        "tid": id,
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTE2Mjk2LCJpYXQiOjE3NDMwODk0MjIuMTYwMDg2NiwidGltZW91dCI6MjU5MjAwMCwidHlwZSI6MX0.TAJ1VEgtyEWIjri0yxVUXfeQVtqNObSQZ-WYGspB5lY"
    }
    p_data = encrypt(p_data)
    json_data = {
        'data': p_data
    }

    response = requests.post('https://api.smallschoolbag.com/a12/book/xml_json/', headers=headers, json=json_data)

    return response.json()['data']


def save_data(data, new_path):
    # 定义一个空列表，用于存储提取的数据
    extracted_data = []

    # 提取书籍的基本信息
    book_info = {
        'book_name': data['name'],
        'publishing': data['publishing'],
    }

    # 遍历每一页
    for page in data['pages']:
        page_info = {
            'page_id': page['id'],
            'page_number': page['page_number'],
            'image_path': page['image_path']
        }

        # 合并书籍信息和页面信息
        combined_info = {**book_info, **page_info}

        # 如果页面有语句信息，遍历每一条语句
        if page['statements']:
            for statement in page['statements']:
                statement_info = {
                    'sound_path': statement['sound_path'],
                    'english_text': statement['english_text'],
                    'chinese_text': statement['chinese_text'],
                    'axis_x': statement['axis_x'],
                    'axis_y': statement['axis_y'],
                    'axis_width': statement['axis_width'],
                    'axis_height': statement['axis_height']
                }
                # 合并页面信息和语句信息
                final_info = {**combined_info, **statement_info}
                extracted_data.append(final_info)
        else:
            # 如果页面没有语句信息，直接添加页面信息
            extracted_data.append(combined_info)

    # 创建 DataFrame
    df = pd.DataFrame(extracted_data)

    # 将 DataFrame 保存到 Excel 文件
    df.to_excel(f'{new_path}/图文标注.xlsx', index=False)

    print(f"数据已成功保存到 {new_path}/'图文标注.xlsx' 文件中。")


def get_data(id, new_path):
    data = get_resp_data(id)
    # 解密
    data = decrypt(data)
    # 保存数据
    save_data(data, new_path)
