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

import execjs




def get_m(input_str, key):
    output = []
    key_len = len(key)

    for i, ch in enumerate(input_str):
        key_char = key[i % key_len]
        xor_val = (ord(ch) + ord(key_char)) % 256
        output.append(format(xor_val, '02x'))

    return ''.join(output)



def get_s(tt):
    input_string = f'xoxoxoxo{tt}'

    res = execjs.compile(open('loader.js' , 'r' , encoding='utf-8').read()).call('OOOoO' , input_string)
    return res




def get_resp(page):
    ua = get_random_ua()
    tt = str(int(time.time() * 1000))

    s = get_s(tt)
    print("s" ,  s)
    cookies = {
        "sessionid": "xlu3qj58yo5zkjm328fr831ps08oid66",
        "Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183": "1745931531,1746426452,1746454341",
        "HMACCOUNT": "74E03469813A9187",
        "Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183": tt,
        "s": s,
    }

    m = get_m('oooooo' + tt + page, 'oooooo')
    print(m)

    t = base64.b64encode(tt.encode()).decode()

    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "m": m,
        "origin": "https://www.mashangpa.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.mashangpa.com/problem-detail/8/",
        "sec-ch-ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "t": t,
        "user-agent": ua,
        "x-requested-with": "XMLHttpRequest",
        # 'cookie': 'sessionid=xlu3qj58yo5zkjm328fr831ps08oid66; Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183=1745931531,1746426452,1746454341; HMACCOUNT=74E03469813A9187; Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183=1746454344; s=51b351b351b351b370b0d090d0f0d030f0f0519050',
    }

    json_data = {
        "page": page,
    }

    response = requests.post(
        "https://www.mashangpa.com/api/problem-detail/8/data/",
        cookies=cookies,
        headers=headers,
        json=json_data,
    )

    data = response.json()
    print(data)
    return data


def parse_data(data):
    nums = data["current_array"]

    print(nums)

    return nums


if __name__ == "__main__":
    res_sum = []
    for i in range(1, 21):
        resp = get_resp(str(i))
        nums = parse_data(resp)
        res_sum.extend(nums)
    print(sum(res_sum))
