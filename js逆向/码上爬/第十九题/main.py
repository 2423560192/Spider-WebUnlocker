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

from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad
import base64

from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad
import base64


# DES3.iv() 返回的值
def DES3_iv():
    """
    返回 '20250507' 作为默认 IV（8 字节）。
    """
    return '20250507'.encode('utf-8')  # 将字符串转为字节数组（8 字节）


def parse_utf8(input_str=None):
    """
    模拟 CryptoJS.enc.Utf8.parse(a) 功能
    如果没有提供输入字符串，则使用 DES3.iv() 返回的默认 IV。

    参数:
        input_str: 输入的字符串（可选）

    返回:
        字节数组：UTF-8 编码的字节数组，或者默认的 8 字节 IV（'20250507'）
    """
    # 如果提供了 input_str，则使用 UTF-8 编码转换为字节数组
    if input_str:
        return input_str.encode('utf-8')
    # 如果没有提供 input_str，则返回默认的 8 字节 IV（'20250507'）
    else:
        return DES3_iv()  # 默认的 IV 是 '20250507'


def decrypt(b, c, a=None):
    """
    完全模拟 CryptoJS 的 decrypt 函数

    参数:
        b: 加密后的密文（Base64 编码的字符串）
        c: 密钥（UTF-8 字符串）
        a: IV（可选，默认为 None，使用默认的 IV）

    返回:
        解密后的明文（字符串）
    """
    if c:  # 如果提供了密钥
        # 将密钥从 UTF-8 字符串转换为字节
        key = c.encode('utf-8')

        # 使用 parse_utf8 模拟 CryptoJS.enc.Utf8.parse(a || DES3.iv())
        iv = parse_utf8(a)  # 如果提供了 a，使用它，否则使用默认 IV

        # 将密文（Base64）解码为字节
        ciphertext = base64.b64decode(b)

        # 创建 DES3 cipher 对象
        cipher = DES3.new(key, DES3.MODE_CBC, iv)

        # 解密并去除填充
        decrypted = cipher.decrypt(ciphertext)
        plaintext = unpad(decrypted, DES3.block_size).decode('utf-8')

        return plaintext
    return ""  # 如果没有提供密钥，返回空字符串


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
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.mashangpa.com/problem-detail/19/',
        'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': ua,
        # 'cookie': 'sessionid=xlu3qj58yo5zkjm328fr831ps08oid66; v=QXhITTA5RWtFcVA0NG5FdXk3eFlrZVNqSUJhdWZvVVVMX01wQlBPbkRKYjNoejlJTzg2VndMOUNPZGVBMTc0NjU3NzY0MjAxMA==; _nano_fp=XpmYn5d8nqmJXpEbnC_uphO7sVYXWszj8oBunmms; Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183=1746529458,1746535829,1746577481,1746582669; HMACCOUNT=74E03469813A9187; Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183=1746582689',
    }

    params = {
        'page': page,
    }

    response = requests.get('https://www.mashangpa.com/api/problem-detail/19/data/', params=params, cookies=cookies,
                            headers=headers)

    data = response.json()
    print(data)
    return data


def parse_data(data):
    nums = data['r']
    k = data['k']
    print(k)

    res = json.loads(decrypt(nums, k))
    print("res:::", res)


    return res['current_array']


if __name__ == '__main__':
    res_sum = []
    for i in range(1, 21):
        resp = get_resp(str(i))
        nums = parse_data(resp)
        res_sum.extend(nums)
    print(sum(res_sum))
