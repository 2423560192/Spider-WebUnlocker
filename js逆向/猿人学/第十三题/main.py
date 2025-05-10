import base64
import re
import time

import requests

from CoreUtils.ua import get_random_ua
from CoreUtils.Encrypt import md5_encrypt
import execjs


def get_m(page):
    m = base64.b64encode(('yuanrenxue' + page).encode()).decode()
    print(m)
    return m


def get_resp(page , ck):
    ua = get_random_ua()
    tt = str(int(time.time()) * 1000)
    # tt = '1746814244000'
    cookies = {
        'sessionid': '10zwpnj1ljclbht04s41inzgtnpntrzt',
        'Hm_lvt_c99546cf032aaa5a679230de9a95c7db': '1746770541,1746776721,1746846259,1746860209',
        'qpfccr': 'true',
        'no-alert3': 'true',
        'tk': '8683284781106509632',
        'Hm_lvt_9bcbda9cbf86757998a2339a0437208e': '1746770631,1746776739,1746846273,1746860215',
        'Hm_lpvt_9bcbda9cbf86757998a2339a0437208e': '1746863253',
        'Hm_lpvt_c99546cf032aaa5a679230de9a95c7db': '1746863438',
        'yuanrenxue_cookie': ck,
    }

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'referer': 'https://match.yuanrenxue.cn/match/13',
        'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        # 'cookie': 'sessionid=9v4dut5gjjvapw0ox3ls3mp5rt5p3yov; Hm_lvt_434c501fe98c1a8ec74b813751d4e3e3=1745473253,1745670989,1745930833,1746704613; Hm_lvt_c99546cf032aaa5a679230de9a95c7db=1746770541,1746776721,1746846259,1746860209; HMACCOUNT=74E03469813A9187; Hm_lvt_9bcbda9cbf86757998a2339a0437208e=1746770631,1746776739,1746846273,1746860215; qpfccr=true; no-alert3=true; Hm_lpvt_9bcbda9cbf86757998a2339a0437208e=1746860996; yuanrenxue_cookie=1746861054|oqLh9tf9iE7zbtCIHsrJhEYf4ZKoD9aavUsiDOEyR7pi0OxMueRK09eNmwdtxrJxzjqLHqcrsAVamJdVqKUFreOKtrTuXskTrRZfGv5Thc3zHGBfT6lF0yMeET2Mnnd9LDX4C5Oy42CRc08bME1t0ReEXWGO0xkMMIlw0bHM; Hm_lpvt_c99546cf032aaa5a679230de9a95c7db=1746861055',
    }

    params = {
        'page': page,
    }

    response = requests.get('https://match.yuanrenxue.cn/api/match/13', params=params, cookies=cookies, headers=headers)

    print(response.json())

    return response.json()


def parse_data(data):
    nums = data['data']
    res = []
    for i in nums:
        res.append(i['value'])
    return res

def get_fisrt():
    import requests

    cookies = {
        'sessionid': '10zwpnj1ljclbht04s41inzgtnpntrzt',
        'Hm_lvt_c99546cf032aaa5a679230de9a95c7db': '1746770541,1746776721,1746846259,1746860209',
        'qpfccr': 'true',
        'no-alert3': 'true',
        'tk': '8683284781106509632',
        'Hm_lvt_9bcbda9cbf86757998a2339a0437208e': '1746770631,1746776739,1746846273,1746860215',
        'Hm_lpvt_9bcbda9cbf86757998a2339a0437208e': '1746863253',
        'Hm_lpvt_c99546cf032aaa5a679230de9a95c7db': '1746863371',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'referer': 'https://match.yuanrenxue.cn/match/13',
        'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        # 'cookie': 'sessionid=10zwpnj1ljclbht04s41inzgtnpntrzt; Hm_lvt_c99546cf032aaa5a679230de9a95c7db=1746770541,1746776721,1746846259,1746860209; qpfccr=true; no-alert3=true; tk=8683284781106509632; Hm_lvt_9bcbda9cbf86757998a2339a0437208e=1746770631,1746776739,1746846273,1746860215; Hm_lpvt_9bcbda9cbf86757998a2339a0437208e=1746863253; Hm_lpvt_c99546cf032aaa5a679230de9a95c7db=1746863371',
    }

    response = requests.get('https://match.yuanrenxue.cn/match/13', cookies=cookies, headers=headers)

    print(response.text)
    # 匹配所有 ('x') 形式中的字符
    chars = re.findall(r"\('([^']+)'\)", response.text)

    # 拼接成最终字符串
    cookie_str = ''.join(chars)
    print(cookie_str)
    return cookie_str.split('=')[-1]

if __name__ == '__main__':
    res = []
    yuan_ck = get_fisrt()
    for i in range(1, 6):
        data = get_resp(str(i) , yuan_ck)
        nums = parse_data(data)
        res.extend(nums)

    print(sum(res))
