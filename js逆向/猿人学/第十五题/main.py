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


def get_m():
    t1 = int(time.time() // 2)
    t2 = t1 - random.randint(1, 50)

    # print(tt)

    # 设置日志级别（可选，调试使用）
    pywasm.log.lvl = 0

    # 初始化 Runtime 实例
    runtime = pywasm.core.Runtime()

    # 加载并实例化 WebAssembly 模块
    m = runtime.instance_from_file('main.wasm')

    # 调用 WebAssembly 模块中的函数 'encrypt'，传入参数 [100, 30]
    r = runtime.invocate(m, 'encode', [t1, t2])

    res = r[0]
    # 打印结果
    print("结果：", res)  # 输出应该是计算的结果
    m = f"{res}|{t1}|{t2}"
    return m


def get_resp(page):
    ua = get_random_ua()  # 假设你有这个函数
    tt = str(int(time.time()) * 1000)

    cookies = {
        'sessionid': '10zwpnj1ljclbht04s41inzgtnpntrzt',
        'Hm_lvt_c99546cf032aaa5a679230de9a95c7db': '1746770541,1746776721,1746846259,1746860209',
        'qpfccr': 'true',
        'no-alert3': 'true',
        'tk': '8683284781106509632',
        'Hm_lvt_9bcbda9cbf86757998a2339a0437208e': '1746770631,1746776739,1746846273,1746860215',
        'Hm_lpvt_9bcbda9cbf86757998a2339a0437208e': '1746865984',
        'Hm_lpvt_c99546cf032aaa5a679230de9a95c7db': '1746866000',
    }

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'referer': 'https://match.yuanrenxue.cn/match/15',
        'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        # 'cookie': 'sessionid=10zwpnj1ljclbht04s41inzgtnpntrzt; Hm_lvt_c99546cf032aaa5a679230de9a95c7db=1746770541,1746776721,1746846259,1746860209; qpfccr=true; no-alert3=true; tk=8683284781106509632; Hm_lvt_9bcbda9cbf86757998a2339a0437208e=1746770631,1746776739,1746846273,1746860215; yuanrenxue_cookie=1746865017|eTaV5AJKegKnKYfGQkZBz0IkEQ1Al6yot92jsrkkRDN5Z1Ffyuym4y2EChtU4GXz5KCxO8pTHSHIQHgbHlpjEUZr05GUF8FdiA80; Hm_lpvt_9bcbda9cbf86757998a2339a0437208e=1746865984; Hm_lpvt_c99546cf032aaa5a679230de9a95c7db=1746866000',
    }

    m = get_m()

    params = {
        'm': m,
        'page': page,
    }

    response = requests.get('https://match.yuanrenxue.cn/api/match/15', params=params, cookies=cookies, headers=headers)

    print(response.json())

    return response.json()


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
