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

import subprocess
from functools import partial

subprocess.Popen = partial(subprocess.Popen, encoding="UTF-8")

import execjs
import os


def get_m(tt):
    m = execjs.compile(open('webpac.js', 'r', encoding='utf-8').read()).call('get_m', tt)
    print('m:::', m)
    return m


def get_resp(page):
    ua = get_random_ua()
    tt = str(int(time.time() * 1000))

    cookies = {
        'sessionid': 'xlu3qj58yo5zkjm328fr831ps08oid66',
        'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183': '1746516380,1746529458,1746535829,1746577481',
        'HMACCOUNT': '74E03469813A9187',
        'v': 'QXhITTA5RWtFcVA0NG5FdXk3eFlrZVNqSUJhdWZvVVVMX01wQlBPbkRKYjNoejlJTzg2VndMOUNPZGVBMTc0NjU3NzY0MjAxMA==',
        'Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183': tt,
        '_nano_fp': 'XpmYn5d8nqmJXpEbnC_uphO7sVYXWszj8oBunmms',
    }

    m = get_m(tt)

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'client-version': '1.0.0',
        'm': m,
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.mashangpa.com/problem-detail/18/',
        'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'timestamp': tt,
        'user-agent': ua,
        'x-requested-with': 'XMLHttpRequest',
        # 'cookie': 'sessionid=xlu3qj58yo5zkjm328fr831ps08oid66; Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183=1746516380,1746529458,1746535829,1746577481; HMACCOUNT=74E03469813A9187; v=QXhITTA5RWtFcVA0NG5FdXk3eFlrZVNqSUJhdWZvVVVMX01wQlBPbkRKYjNoejlJTzg2VndMOUNPZGVBMTc0NjU3NzY0MjAxMA==; Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183=1746577782; _nano_fp=XpmYn5d8nqmJXpEbnC_uphO7sVYXWszj8oBunmms',
    }

    params = {
        'page': page,
    }

    response = requests.get('https://www.mashangpa.com/api/problem-detail/18/data/', params=params, cookies=cookies,
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
