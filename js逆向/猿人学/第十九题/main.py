import base64
import math
import random
import re
import time

import httpx
import pywasm
import requests

from CoreUtils.ua import get_random_ua
from CoreUtils.Encrypt import md5_encrypt
import execjs


def get_m(tt):
    m = execjs.compile(open('loader.js', 'r', encoding='utf-8').read()).call('btoa', tt)
    print(m)
    return m


def get_resp(page):
    ua = get_random_ua()  # 假设你有这个函数
    tt = str(int(time.time()) * 1000)

    cookies = {
        'sessionid': '10zwpnj1ljclbht04s41inzgtnpntrzt',
        'Hm_lvt_c99546cf032aaa5a679230de9a95c7db': '1746860209,1746876536,1746956778,1747015815',
        'HMACCOUNT': 'D8E43A19B6731930',
        'qpfccr': 'true',
        'no-alert3': 'true',
        'Hm_lvt_9bcbda9cbf86757998a2339a0437208e': '1746860215,1746876543,1746956781,1747015847',
        'Hm_lpvt_9bcbda9cbf86757998a2339a0437208e': '1747015847',
        'Hm_lpvt_c99546cf032aaa5a679230de9a95c7db': '1747015883',
    }

    headers = {
        "pragma": "no-cache",
        "cache-control": "no-cache",
        "sec-ch-ua-platform": "\"Windows\"",
        "x-requested-with": "XMLHttpRequest",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "sec-ch-ua": "\"Chromium\";v=\"136\", \"Google Chrome\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://match.yuanrenxue.cn/match/19",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9"
    }

    params = {
        'page': page,
    }

    # 使用 HTTP/2 请求
    with httpx.Client(http2=True, cookies=cookies, headers=headers) as client:
        response = client.get('https://match.yuanrenxue.cn/api/match/19', params=params)
        print("使用协议:", response.http_version)
        print(response.json())
        return response.json()
    # response = requests.get('https://match.yuanrenxue.cn/api/match/16', headers=headers, cookies=cookies, params=params)
    # #
    # print(response.json())


def parse_data(data):
    nums = data['data']
    res = []
    for i in nums:
        res.append(i['value'])
    return res


if __name__ == '__main__':
    res = []
    session = requests.Session()
    for i in range(1, 6):
        data = get_resp(str(i))
        nums = parse_data(data)
        res.extend(nums)

    print(sum(res))
