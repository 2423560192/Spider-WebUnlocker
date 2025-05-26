import base64
import binascii
import json
import time

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from CoreUtils.ua import get_random_ua

import urllib.parse
from CoreUtils.Encrypt import md5_encrypt, sha256, words_to_bytes


def get_s(tt):
    return md5_encrypt("sssssbbbbb" + tt)


def xxxxoooo(cipher_text_base64: str):
    key = {
        "words": [
            2021161080,
            2021161080,
            1869573999,
            1869573999
        ],
        "sigBytes": 16
    }

    iv = {
        "words": [
            808530483,
            875902519,
            943276354,
            1128547654
        ],
        "sigBytes": 16
    }
    key = words_to_bytes(key['words'], key['sigBytes'])
    iv = words_to_bytes(iv['words'], iv['sigBytes'])

    cipher_bytes = bytes.fromhex(cipher_text_base64)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(cipher_bytes)
    try:
        return unpad(decrypted, AES.block_size).decode('utf-8')
    except ValueError as e:
        raise ValueError("解密失败，可能是 key/iv 不正确或数据被破坏") from e


def get_resp(page):
    ua = get_random_ua()
    tt = str(int(time.time() * 1000))
    cookies = {
        'sessionid': 'xlu3qj58yo5zkjm328fr831ps08oid66',
        'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183': '1745931531,1746426452',
        'HMACCOUNT': '74E03469813A9187',
        'Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183': tt,
    }
    m = md5_encrypt(f'xialuo{tt}')

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'm': m,
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.mashangpa.com/problem-detail/7/',
        'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'ts': tt,
        'user-agent': ua,
        'x-requested-with': 'XMLHttpRequest',
        # 'cookie': 'sessionid=xlu3qj58yo5zkjm328fr831ps08oid66; Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183=1745931531,1746426452; HMACCOUNT=74E03469813A9187; Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183=1746431159',
    }

    x = sha256(m + 'xxoo')
    print('x1:', x)

    params = {
        'page': page,
        'x': x,
    }

    response = requests.get('https://www.mashangpa.com/api/problem-detail/7/data/', params=params, cookies=cookies,
                            headers=headers)

    data = response.json()
    print(data)
    return data


def parse_data(data):
    nums = data['r']

    print(nums)
    res = json.loads(xxxxoooo(nums))['current_array']
    print(res)

    return res


if __name__ == '__main__':
    res_sum = []
    for i in range(1, 21):
        resp = get_resp(str(i))
        nums = parse_data(resp)
        res_sum.extend(nums)
    print(sum(res_sum))
