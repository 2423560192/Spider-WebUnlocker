"""
小程序：蓝思背单词
获取一本书下面的所有单元单词
免责声明：
本代码仅供学习和参考之用，不得用于任何商业用途或非法目的。使用者应自行承担因使用本代码所产生的一切后果和风险，包括但不限于数据丢失、系统损坏或法律责任。作者不对代码的完整性、准确性或适用性作出任何明示或暗示的保证。使用本代码前，请确保遵守相关法律法规和目标网站的使用条款。
"""
import json

import execjs
import pandas as pd
import requests
from jsonpath_ng import parse

from utils.decrypt_js import jiemi


def get_resp_data(lgid):
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1 wechatdevtools/1.06.2412050 MicroMessenger/8.0.5 Language/zh_CN webview/',
        'content-type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://servicewechat.com/wx9ca23b910f46dcde/devtools/page-frame.html',
    }

    data = f'lgid={lgid}&type=learn&appCookie=version_8.0.5%20build_18%20pro_0%20lan_zh_CN%20oid_%20package_com.miniapp.lsbdc%20platform_devtools%20ver_1%20model_iPhone-12%2F13%20(Pro)%20t2_1742814109%20t_1742813790%20md5_7d%20uid_0%20di_0%20wh_390x753'

    response = requests.post('https://dudu.diiiapp.com/app/word/words', headers=headers, data=data)

    data = response.json()
    return data


def get_data(title, uni_title, lgid):
    data = get_resp_data(lgid)
    # 解密
    data = jiemi(data)
    # 解析
    parse_data(title, uni_title, data)


def parse_data(title, uni_title, data):
    # 定义 JSONPath 表达式
    word_expr = parse('$.list[*].word')
    meaning_expr = parse('$.list[*].meaning')

    # 提取数据
    words = [match.value for match in word_expr.find(data)]
    meanings = [match.value for match in meaning_expr.find(data)]

    # 分离词性和意思
    results = []
    for word, meaning in zip(words, meanings):
        # 提取词性（假设词性是 meaning 中第一个以点号分隔的部分）
        parts = meaning.split('. ', 1)
        pos = parts[0]  # 词性
        definition = parts[1] if len(parts) > 1 else ""  # 意思（如果有）
        results.append({
            "单词": word,
            "意思": definition,
            "词性": pos
        })

    # 将结果转换为 DataFrame 并保存到 Excel
    df = pd.DataFrame(results)
    df.to_excel(f"{title}/{uni_title}.xlsx", index=False, engine='openpyxl')

    print(f"数据已保存到 {title}/{uni_title}.xlsx 文件中！")

    # 打印结果以便查看
    for result in results:
        print(result)
