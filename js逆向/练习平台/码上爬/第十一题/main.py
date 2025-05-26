import base64
import binascii
import json
import time

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from CoreUtils.ua import get_random_ua
import pywasm

import math

import urllib.parse
from CoreUtils.Encrypt import md5_encrypt, sha256, words_to_bytes, generate_hmac_sha1

import execjs


def get_m(page):
    # 获取当前时间戳（秒）
    current_time = int(time.time())

    # 模拟 Math.floor 和 int（parseInt）
    tt = int(math.floor(current_time))

    print(tt)

    # 设置日志级别（可选，调试使用）
    pywasm.log.lvl = 0

    # 初始化 Runtime 实例
    runtime = pywasm.core.Runtime()

    # 加载并实例化 WebAssembly 模块
    m = runtime.instance_from_file('encrypt.wasm')

    # 调用 WebAssembly 模块中的函数 'encrypt'，传入参数 [100, 30]
    r = runtime.invocate(m, 'encrypt', [int(page), tt])

    res = r[0]
    # 打印结果
    print("结果：" , res , r)  # 输出应该是计算的结果
    return res , tt


def get_resp(page):
    ua = get_random_ua()
    tt = str(int(time.time() * 1000))
    cookies = {
        'sessionid': 'xlu3qj58yo5zkjm328fr831ps08oid66',
        'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183': '1746503823,1746516380,1746529458,1746535829',
        'HMACCOUNT': '74E03469813A9187',
        'Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183': '1746546492',
        'v': 'QXc3UGRXNXM1ZnB6ZzE1SFI0Q1BtSF9pWC1fVmo5TWs1RldHYXpoV2Z2SE5YYUJSb0I4aW1iVGoxbmtMMTc0NjU0NjUwMzgxMQ==',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.mashangpa.com/problem-detail/11/',
        'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': ua,
        # 'cookie': 'sessionid=xlu3qj58yo5zkjm328fr831ps08oid66; v=QXdlbTQyS0RMQjFDVUtjS0U5TTIzeTZSbHJEVUROdnVOZUJmWXRuMEl4YTlTQ211NGR4clBrV3c3N0RxMTc0NjQ1OTM4MzAyNA==; Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183=1746503823,1746516380,1746529458,1746535829; HMACCOUNT=74E03469813A9187; Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183=1746539804',
    }

    m , tt = get_m(page)

    print("m:" , m)

    params = {
        'page': page,
        'm': m,
        '_ts': tt,
    }

    response = requests.get('https://www.mashangpa.com/api/problem-detail/11/data/', params=params, cookies=cookies,
                            headers=headers)

    data = response.json()
    print(data)
    return data


def parse_data(data):
    nums = data['current_array']

    print(nums)

    return nums


if __name__ == '__main__':
    res_sum = []
    for i in range(1, 21):
        resp = get_resp(str(i))
        nums = parse_data(resp)
        res_sum.extend(nums)
    print(sum(res_sum))
