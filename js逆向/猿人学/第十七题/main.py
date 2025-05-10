import base64
import re
import time

import httpx
import requests

from CoreUtils.ua import get_random_ua
from CoreUtils.Encrypt import md5_encrypt
import execjs





def get_resp(page):
    ua = get_random_ua()  # 假设你有这个函数
    tt = str(int(time.time()) * 1000)

    cookies = {
        'sessionid': '10zwpnj1ljclbht04s41inzgtnpntrzt',
        'Hm_lvt_c99546cf032aaa5a679230de9a95c7db': '1746770541,1746776721,1746846259,1746860209',
        'qpfccr': 'true',
        'no-alert3': 'true',
        'tk': '8683284781106509632',
        'Hm_lvt_9bcbda9cbf86757998a2339a0437208e': '1746770631,1746776739,1746846273,1746860215',
        'Hm_lpvt_9bcbda9cbf86757998a2339a0437208e': '1746864076',
        'Hm_lpvt_c99546cf032aaa5a679230de9a95c7db': '1746864082',
    }

    headers = {
        'Host': 'match.yuanrenxue.cn',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua-platform': '"Windows"',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': ua,
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://match.yuanrenxue.cn/match/17',
        'accept-language': 'zh-CN,zh;q=0.9',
        'priority': 'u=0, i',
    }

    params = {'page': page}

    # 使用 HTTP/2 请求
    with httpx.Client(http2=True, cookies=cookies, headers=headers) as client:
        response = client.get('https://match.yuanrenxue.cn/api/match/17', params=params)
        print("使用协议:", response.http_version)
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
