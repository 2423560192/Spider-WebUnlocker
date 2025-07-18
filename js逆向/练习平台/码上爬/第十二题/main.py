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

from urllib.parse import urlparse, parse_qs
from CoreUtils.Encrypt import md5_encrypt, sha256, words_to_bytes, generate_hmac_sha1

import subprocess
from functools import partial

subprocess.Popen = partial(subprocess.Popen, encoding="UTF-8")

import execjs
import os

from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad
import base64

from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad



def get_m(page):
    result = subprocess.run(
        ["node", "loader.js" , page],
        capture_output=True,
        text=True
    )
    url = result.stdout.strip()
    # 解析 URL
    parsed_url = urlparse(url)
    # 解析查询参数
    params = parse_qs(parsed_url.query)

    # 提取 m 和 t
    m = params.get('m', [None])[0]
    t = params.get('t', [None])[0]
    return m , t


def get_resp(page):
    ua = get_random_ua()
    tt = str(int(time.time() * 1000))

    cookies = {
        'sessionid': 'xlu3qj58yo5zkjm328fr831ps08oid66',
        'v': 'QXhITTA5RWtFcVA0NG5FdXk3eFlrZVNqSUJhdWZvVVVMX01wQlBPbkRKYjNoejlJTzg2VndMOUNPZGVBMTc0NjU3NzY0MjAxMA==',
        '_nano_fp': 'XpmYn5d8nqmJXpEbnC_uphO7sVYXWszj8oBunmms',
        'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183': '1746529458,1746535829,1746577481,1746582669',
        'HMACCOUNT': '74E03469813A9187',
        'Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183': tt,
    }

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.mashangpa.com/problem-detail/12/',
        'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': ua,
        'x-requested-with': 'XMLHttpRequest',
        # 'cookie': 'sessionid=xlu3qj58yo5zkjm328fr831ps08oid66; v=QXhITTA5RWtFcVA0NG5FdXk3eFlrZVNqSUJhdWZvVVVMX01wQlBPbkRKYjNoejlJTzg2VndMOUNPZGVBMTc0NjU3NzY0MjAxMA==; _nano_fp=XpmYn5d8nqmJXpEbnC_uphO7sVYXWszj8oBunmms; Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183=1746529458,1746535829,1746577481,1746582669; HMACCOUNT=74E03469813A9187; Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183=1746584761',
    }

    m , t = get_m(page)
    print(m , t)

    params = {
        'page': page,
        'm': m,
        't': t,
    }

    response = requests.get('https://www.mashangpa.com/api/problem-detail/12/data/', params=params, cookies=cookies,
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