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


def get_h5(page, tt):
    result = subprocess.run(
        ["node", "loader.js", page, str(tt)],
        capture_output=True,
        text=True
    )
    print(result.stdout.strip())
    return result.stdout.strip()


def get_resp(page):
    ua = get_random_ua()
    tt = str(int(time.time()) * 1000)
    tt = int(time.time()) * 1000

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://www.mashangpa.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.mashangpa.com/problem-detail/16/",
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
        "Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183": "1746623315"
    }

    url = "https://www.mashangpa.com/api/problem-detail/16/data/"

    h5 = get_h5(page, tt)

    data = {
        "page": int(page),
        "t": tt,
        "h5": h5
    }

    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, cookies=cookies, data=data)

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
