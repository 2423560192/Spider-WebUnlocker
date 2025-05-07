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


def get_p(tt):
    def J(b, f, p):
        return b ^ (f >> (p % 8))

    def B(b, f, p):
        return b ^ (f << (p % 8))

    def Y(b, f):
        return (b + f - f) ^ f

    def compute_p(N):
        W = 0
        for ch in N:
            O = ord(ch)
            for y in range(20):
                if y % 3 == 0:
                    W = B(W, O, y)
                elif y % 3 == 1:
                    W = J(W, O, y)
                elif y % 3 == 2:
                    W = Y(W, O)
        return W


    input_string = 'dasdasdarqwdasdasqwdasda' + tt

    p = compute_p(input_string)

    return str(hex(p)[2:])


def get_m(tt):
    p = get_p(tt)
    print('p:::' , p)
    t = p + tt + '\x00'
    print(t)
    # t = '154b1746617534226' + '\x00'
    m = base64.b64encode(t.encode()).decode()
    print('m:::', m)
    return m


def get_resp(page):
    ua = get_random_ua()
    tt = str(int(time.time()) * 1000)

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://www.mashangpa.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.mashangpa.com/problem-detail/14/",
        "sec-ch-ua": "\"Chromium\";v=\"136\", \"Google Chrome\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": ua,
        "x-requested-with": "XMLHttpRequest"
    }
    cookies = {
        "sessionid": "xlu3qj58yo5zkjm328fr831ps08oid66",
        "v": "QXhITTA5RWtFcVA0NG5FdXk3eFlrZVNqSUJhdWZvVVVMX01wQlBPbkRKYjNoejlJTzg2VndMOUNPZGVBMTc0NjU3NzY0MjAxMA==",
        "_nano_fp": "XpmYn5d8nqmJXpEbnC_uphO7sVYXWszj8oBunmms",
        "Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183": "1746535829,1746577481,1746582669,1746616149",
        "HMACCOUNT": "74E03469813A9187",
        "Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183": "1746616871"
    }
    url = "https://www.mashangpa.com/api/problem-detail/14/data/"

    m = str(get_m(tt))
    print(m, type(m))
    params = {
        "m": m
    }

    data = {
        "page": page
    }
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, cookies=cookies, params=params, data=data)

    data = response.json()
    print(data)
    print(response.url)
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
