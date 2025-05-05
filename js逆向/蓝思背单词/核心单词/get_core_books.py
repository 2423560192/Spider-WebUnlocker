import os

import pandas as pd
from jsonpath_ng import parse

from utils.decrypt_js import jiemi
import jsonpath_ng

def get_resp_data():
    import requests

    headers = {
        'Host': 'dudu.diiiapp.com',
        'xweb_xhr': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c33)XWEB/11581',
        'content-type': 'application/x-www-form-urlencoded',
        'accept': '*/*',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://servicewechat.com/wx8095a0e00e139ded/22/page-frame.html',
        'accept-language': 'zh-CN,zh;q=0.9',
    }

    data = {
        'appCookie': 'version_3.9.12 build_18 pro_0 lan_zh_CN oid_oZAMb5BVTr4cL4uDe4m3dnJow2_k package_com.miniapp.lsbdc platform_windows ver_1 model_microsoft t2_1742981113 t_1742981058 md5_7d uid_0 di_0 wh_414x716',
    }

    response = requests.post('https://dudu.diiiapp.com/app/word/groups', headers=headers, data=data)
    return response.json()

def get_parse_data(data):
    # 提取id
    jsonpath_expr = parse("$.list[*].lgid")

    # 提取 lgid
    lgid_list = [match.value for match in jsonpath_expr.find(data)]

    print(lgid_list)  # 输出: [112, 1, 161, 3123, 5903, 5904, 6030, 0]
    return lgid_list
def get_data():
    res_data = get_resp_data()
    # 解密
    data = jiemi(res_data)
    print(data)

    res = get_parse_data(data)
    print(res)
    # 将 ID 列表保存到 Excel 文件（仅初次运行时需要）
    excel_file = "book_ids.xlsx"

    if not os.path.exists(excel_file):
        df = pd.DataFrame(res, columns=["Book_ID"])
        df["Processed"] = False  # 添加一列标记是否已处理，初始值为 False
        df.to_excel(excel_file, index=False)
        print(f"书本 ID 已保存到 {excel_file}")
    else:
        print(f"{excel_file} 已存在，将从中读取数据")

get_data()
