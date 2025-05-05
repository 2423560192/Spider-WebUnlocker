"""
免责声明：
本代码仅供学习和参考之用，不得用于任何商业用途或非法目的。使用者应自行承担因使用本代码所产生的一切后果和风险，包括但不限于数据丢失、系统损坏或法律责任。作者不对代码的完整性、准确性或适用性作出任何明示或暗示的保证。使用本代码前，请确保遵守相关法律法规和目标网站的使用条款。
"""
import json
import os

import pandas as pd
import requests
from jsonpath_ng import parse

from utils.decrypt_js import jiemi


def get_resp_data():
    headers = {
        'authority': 'dudu.diiiapp.com',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1 wechatdevtools/1.06.2412050 MicroMessenger/8.0.5 Language/zh_CN webview/',
        'content-type': 'application/json',
        'accept': '*/*',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://servicewechat.com/wx9ca23b910f46dcde/devtools/page-frame.html',
    }

    response = requests.get(
        'https://dudu.diiiapp.com/app/word/books?appCookie=version_8.0.5%20build_18%20pro_0%20lan_zh_CN%20oid_%20package_com.miniapp.lsbdc%20platform_devtools%20ver_1%20model_iPhone-12%2F13%20(Pro)%20t2_1742892203%20t_1742892118%20md5_7d%20uid_0%20di_0%20wh_390x753',
        headers=headers,
    )

    data = response.json()
    return data


def get_parse_data(json_data):
    # 提取所有版本的 title
    version_title_expr = parse('$[*].title')
    version_titles = [match.value for match in version_title_expr.find(json_data)]

    # 提取每个版本下的 book_id, version 和 title
    books_expr = parse('$[*].menu[*].[book_id]')
    books_data = [match.value for match in books_expr.find(json_data)]

    return books_data


def get_data():
    data = get_resp_data()

    data = jiemi(data)

    # 解析数据
    res = get_parse_data(data)

    return res


if __name__ == '__main__':
    res = get_data()
    # 将 ID 列表保存到 Excel 文件（仅初次运行时需要）
    excel_file = "../核心单词/book_ids.xlsx"
    if not os.path.exists(excel_file):
        df = pd.DataFrame(res, columns=["Book_ID"])
        df["Processed"] = False  # 添加一列标记是否已处理，初始值为 False
        df.to_excel(excel_file, index=False)
        print(f"书本 ID 已保存到 {excel_file}")
    else:
        print(f"{excel_file} 已存在，将从中读取数据")
