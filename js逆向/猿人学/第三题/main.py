import time
from collections import defaultdict

import requests

from CoreUtils.ua import get_random_ua
from CoreUtils.Encrypt import md5_encrypt
import execjs


def get_resp(page):
    ua = get_random_ua()
    tt = str(time.time())[:-4]
    # tt = '1746814244000'
    print(tt)

    url = "https://match.yuanrenxue.cn/api/match/3"

    params = {
        "page": page
    }
    response = session.get(url, params=params)
    print(response.json())

    return response.json()


def parse_data(data):
    nums = data['data']
    res = []
    for i in nums:
        res.append(i['value'])
    return res


def get_first():
    res = session.post('https://match.yuanrenxue.cn/jssm')
    print(res.cookies)


if __name__ == '__main__':
    session = requests.Session()

    session.cookies.update({
        "sessionid": "9v4dut5gjjvapw0ox3ls3mp5rt5p3yov",
        "Hm_lvt_434c501fe98c1a8ec74b813751d4e3e3": "1745473253,1745670989,1745930833,1746704613",
        "qpfccr": "true",
        "Hm_lvt_c99546cf032aaa5a679230de9a95c7db": "1746708668,1746756776,1746770541,1746776721",
        "HMACCOUNT": "74E03469813A9187",
        "no-alert3": "true",
        "Hm_lvt_9bcbda9cbf86757998a2339a0437208e": "1746708671,1746756927,1746770631,1746776739",
        "Hm_lpvt_9bcbda9cbf86757998a2339a0437208e": "1746776739",
        "Hm_lpvt_c99546cf032aaa5a679230de9a95c7db": "1746776748"
    })
    session.headers = {
        "content-length": "0",
        "sec-ch-ua-platform": "\"Windows\"",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "sec-ch-ua": "\"Chromium\";v=\"136\", \"Google Chrome\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "accept": "*/*",
        "origin": "https://match.yuanrenxue.cn",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://match.yuanrenxue.cn/match/3",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9"
    }

    res = []
    dic = defaultdict(int)
    for i in range(1, 6):
        get_first()
        data = get_resp(str(i))
        nums = parse_data(data)
        print(nums)
        for j in nums:
            dic[j] += 1
        res.extend(nums)

    print(dic)
