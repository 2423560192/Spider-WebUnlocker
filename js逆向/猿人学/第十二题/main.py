import base64
import time

import requests

from CoreUtils.ua import get_random_ua
from CoreUtils.Encrypt import md5_encrypt
import execjs


def get_m(page):
    m = base64.b64encode(('yuanrenxue' + page).encode()).decode()
    print(m)
    return m

def get_resp(page):
    ua = get_random_ua()
    tt = str(int(time.time()) * 1000)
    # tt = '1746814244000'

    cookies = {
        'sessionid': '9v4dut5gjjvapw0ox3ls3mp5rt5p3yov',
        'Hm_lvt_434c501fe98c1a8ec74b813751d4e3e3': '1745473253,1745670989,1745930833,1746704613',
        'Hm_lvt_c99546cf032aaa5a679230de9a95c7db': '1746770541,1746776721,1746846259,1746860209',
        'HMACCOUNT': '74E03469813A9187',
        'Hm_lvt_9bcbda9cbf86757998a2339a0437208e': '1746770631,1746776739,1746846273,1746860215',
        'Hm_lpvt_9bcbda9cbf86757998a2339a0437208e': '1746860215',
        'qpfccr': 'true',
        'no-alert3': 'true',
        'Hm_lpvt_c99546cf032aaa5a679230de9a95c7db': '1746860224',
    }

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'referer': 'https://match.yuanrenxue.cn/match/12',
        'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        # 'cookie': 'sessionid=9v4dut5gjjvapw0ox3ls3mp5rt5p3yov; Hm_lvt_434c501fe98c1a8ec74b813751d4e3e3=1745473253,1745670989,1745930833,1746704613; Hm_lvt_c99546cf032aaa5a679230de9a95c7db=1746770541,1746776721,1746846259,1746860209; HMACCOUNT=74E03469813A9187; Hm_lvt_9bcbda9cbf86757998a2339a0437208e=1746770631,1746776739,1746846273,1746860215; Hm_lpvt_9bcbda9cbf86757998a2339a0437208e=1746860215; qpfccr=true; no-alert3=true; Hm_lpvt_c99546cf032aaa5a679230de9a95c7db=1746860224',
    }
    m = get_m(page)
    params = {
        'page': page,
        'm': m,
    }

    response = requests.get('https://match.yuanrenxue.cn/api/match/12', params=params, cookies=cookies, headers=headers)
    print(response.text)

    print(response.json())

    return response.json()


def parse_data(data):
    nums = data['data']
    res = []
    for i in nums:
        res.append(i['value'])
    return res



if __name__ == '__main__':
    res = []
    session = requests.Session()
    for i in range(1, 6):
        data = get_resp(str(i))
        nums = parse_data(data)
        res.extend(nums)

    print(sum(res))
