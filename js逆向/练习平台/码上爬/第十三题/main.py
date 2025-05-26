import base64
import binascii
import datetime
import hashlib
import json
import random
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

from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad
import base64

from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad



def get_r():
    r = execjs.compile(open('loader.js', 'r', encoding='utf-8').read()).call('get_r')
    print("r:::" ,r)
    return r


def uu_s():
    # 定义十六进制字符集
    hex_chars = "0123456789abcdef"

    # 生成32个随机字符
    arr = [random.choice(hex_chars) for _ in range(32)]

    # 将字符数组连接成一个字符串
    return ''.join(arr)


def get_s(page , tt):
    # 生成 uu 值，类似于 JavaScript 中的 _0x1e5c29()
    uu = uu_s()
    # 构造 {"page":"1"} 格式的 JSON 字符串，去掉中间空格
    page_string = json.dumps({"page": page}, separators=(",", ":"))


    # 拼接 r 字符串
    r = page_string + uu + str(tt)

    # 打印调试信息
    print("Timestamp:", tt)
    print('page_s' , len(page_string))
    print('uu' , len(uu))
    print("Length of r:", len(r))
    print("rr:", r)

    # 返回 MD5 和时间戳
    md5_hash = hashlib.md5(r.encode('utf-8')).hexdigest()
    return md5_hash , uu


# def get_hexin_v():
#
#     ctx = execjs.compile(open('v.js', 'r', encoding='utf-8').read())
#     res = ctx.call('get_D')
#     print('get_hexin_v:::', res)
#     return res

def get_resp(page):
    ua = get_random_ua()
    tt = str(int(time.time()) * 1000)

    # r = get_r()
    s,r = get_s(page , tt)
    print('r:::' , r)
    print('s:::' , s)
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://www.mashangpa.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "r": r,
        "referer": "https://www.mashangpa.com/problem-detail/13/",
        "s": s,
        "sec-ch-ua": "\"Chromium\";v=\"136\", \"Google Chrome\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "t": tt,
        "user-agent": ua,
        "x-requested-with": "XMLHttpRequest"
    }
    cookies = {
        'sessionid': 'xlu3qj58yo5zkjm328fr831ps08oid66',
        'v': 'QXhITTA5RWtFcVA0NG5FdXk3eFlrZVNqSUJhdWZvVVVMX01wQlBPbkRKYjNoejlJTzg2VndMOUNPZGVBMTc0NjU3NzY0MjAxMA==',
        '_nano_fp': 'XpmYn5d8nqmJXpEbnC_uphO7sVYXWszj8oBunmms',
        'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183': '1746529458,1746535829,1746577481,1746582669',
        'HMACCOUNT': '74E03469813A9187',
        'Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183': '1746607725',
    }

    url = "https://www.mashangpa.com/api/problem-detail/13/data/"
    data = {
        "page": page
    }

    print(headers)
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, cookies=cookies, data=data)

    data = response.json()
    print(data)
    return data


def parse_data(data):
    nums = data
    print(nums)
    return nums['current_array']


if __name__ == '__main__':
    res_sum = []
    for i in range(1, 21):
        resp = get_resp(str(i))
        nums = parse_data(resp)
        res_sum.extend(nums)
    print(sum(res_sum))