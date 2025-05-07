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



def get_hexin_v():

    ctx = execjs.compile(open('main.js', 'r', encoding='utf-8').read())
    res = ctx.call('get_D')
    print('get_hexin_v:::', res)
    return res


def get_resp(page):
    ua = get_random_ua()
    tt = str(int(time.time() * 1000))

    v = get_hexin_v()


    cookies = {
        'sessionid': 'xlu3qj58yo5zkjm328fr831ps08oid66',
        'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183': '1746503823,1746516380,1746529458,1746535829',
        'HMACCOUNT': '74E03469813A9187',
        'Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183': tt,
        'v': v,
    }





    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'hexin-v': v,
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.mashangpa.com/problem-detail/15/',
        'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': ua,
        # 'cookie': 'sessionid=xlu3qj58yo5zkjm328fr831ps08oid66; Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183=1746503823,1746516380,1746529458,1746535829; HMACCOUNT=74E03469813A9187; Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183=1746546492; v=QXc3UGRXNXM1ZnB6ZzE1SFI0Q1BtSF9pWC1fVmo5TWs1RldHYXpoV2Z2SE5YYUJSb0I4aW1iVGoxbmtMMTc0NjU0NjUwMzgxMQ==',
    }

    params = {
        'page': page,
    }

    response = requests.get('https://www.mashangpa.com/api/problem-detail/15/data/', params=params, cookies=cookies,
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
