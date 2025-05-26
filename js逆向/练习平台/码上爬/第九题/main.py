import base64
import binascii
import json
import time

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from CoreUtils.ua import get_random_ua

import urllib.parse
from CoreUtils.Encrypt import md5_encrypt, sha256, words_to_bytes , generate_hmac_sha1


def get_m(tt):
    r = '9527' + tt
    m = generate_hmac_sha1(r , 'xxxooo')
    print("m:" , m)
    return m





def get_resp(page):
    ua = get_random_ua()
    tt = str(int(time.time() * 1000))
    cookies = {
        'sessionid': 'xlu3qj58yo5zkjm328fr831ps08oid66',
        'v': 'QXdlbTQyS0RMQjFDVUtjS0U5TTIzeTZSbHJEVUROdnVOZUJmWXRuMEl4YTlTQ211NGR4clBrV3c3N0RxMTc0NjQ1OTM4MzAyNA==',
        'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183': '1746426452,1746454341,1746497340,1746503823',
        'HMACCOUNT': '74E03469813A9187',
        'Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183': tt,
    }

    m = get_m(tt)

    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://www.mashangpa.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.mashangpa.com/problem-detail/9/',
        'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': ua,
        'x-requested-with': 'XMLHttpRequest',
        # 'cookie': 'sessionid=xlu3qj58yo5zkjm328fr831ps08oid66; v=QXdlbTQyS0RMQjFDVUtjS0U5TTIzeTZSbHJEVUROdnVOZUJmWXRuMEl4YTlTQ211NGR4clBrV3c3N0RxMTc0NjQ1OTM4MzAyNA==; Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183=1745931531,1746426452,1746454341,1746497340; HMACCOUNT=74E03469813A9187; Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183=1746497359',
    }

    t = base64.b64encode(tt.encode()).decode()

    json_data = {
        'page': page,
        'm': m,
        'tt': t,
    }
    print(json_data)

    response = requests.post('https://www.mashangpa.com/api/problem-detail/9/data/', cookies=cookies, headers=headers,
                             json=json_data)

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
