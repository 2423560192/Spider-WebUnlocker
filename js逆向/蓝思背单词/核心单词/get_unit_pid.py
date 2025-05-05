"""
获取一本书下面的单元名和id
免责声明：
本代码仅供学习和参考之用，不得用于任何商业用途或非法目的。使用者应自行承担因使用本代码所产生的一切后果和风险，包括但不限于数据丢失、系统损坏或法律责任。作者不对代码的完整性、准确性或适用性作出任何明示或暗示的保证。使用本代码前，请确保遵守相关法律法规和目标网站的使用条款。
"""
import json

import requests
from jsonpath_ng import parse

from utils.decrypt_js import jiemi


def get_resp_data(book_id):
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
        'lgid': '1',
        'appCookie': 'version_3.9.12 build_18 pro_0 lan_zh_CN oid_oZAMb5BVTr4cL4uDe4m3dnJow2_k package_com.miniapp.lsbdc platform_windows ver_1 model_microsoft t2_1742981443 t_1742981058 md5_7d uid_0 di_0 wh_414x716',
    }

    response = requests.post('https://dudu.diiiapp.com/app/word/groups', headers=headers, data=data)
    return response.json()


def get_parse_data(data):
    # 定义 JSONPath 表达式
    book_title_expr = parse('$.entry.group_name')
    unit_title_expr = parse('$.list[*].title')
    lgid_expr = parse('$.list[*].lgid')

    # 提取数据
    book_title = book_title_expr.find(data)[0].value  # 总书名
    unit_titles = [match.value for match in unit_title_expr.find(data)]  # 单元标题
    lgids = [match.value for match in lgid_expr.find(data)]  # lgid

    # 打印结果
    print("总书名:", book_title)
    print("\n单元信息:")
    for unit_title, lgid in zip(unit_titles, lgids):
        print(f"单元标题: {unit_title}, lgid: {lgid}")

    # 可选：将结果保存为结构化数据
    results = {
        "title": book_title,
        "unit": [{"title": title, "lgid": lgid} for title, lgid in zip(unit_titles, lgids)]
    }

    # 转换为 JSON 格式并打印
    # print("\n结构化 JSON 结果:")
    # print(json.dumps(results, ensure_ascii=False, indent=2))
    return results
