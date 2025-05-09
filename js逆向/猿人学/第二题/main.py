import time

import requests

from CoreUtils.ua import get_random_ua
from CoreUtils.Encrypt import md5_encrypt
import execjs




def get_resp(page):
    ua = get_random_ua()
    tt = str(int(time.time()) * 1000)
    # tt = '1746814244000'

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "referer": "https://match.yuanrenxue.cn/match/3",
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
        "sessionid": "9v4dut5gjjvapw0ox3ls3mp5rt5p3yov",
        "qpfccr": "true",
        "Hm_lvt_434c501fe98c1a8ec74b813751d4e3e3": "1745473253,1745670989,1745930833,1746704613",
        "Hm_lvt_c99546cf032aaa5a679230de9a95c7db": "1746345812,1746622031,1746704061,1746708668",
        "HMACCOUNT": "74E03469813A9187",
        "no-alert3": "true",
        "Hm_lvt_9bcbda9cbf86757998a2339a0437208e": "1745930809,1746345846,1746704066,1746708671",
        "Hm_lpvt_9bcbda9cbf86757998a2339a0437208e": "1746715233",
        "Hm_lpvt_c99546cf032aaa5a679230de9a95c7db": "1746716911"
    }

    url = "https://match.yuanrenxue.cn/api/match/3"

    params = {
        "page": page
    }
    response = session.get(url, headers=headers, cookies=cookies, params=params)
    print(response.text)
    print(response.json())

    return response.json()


def parse_data(data):
    nums = data['data']
    res = []
    for i in nums:
        res.append(i['value'])
    return res

def get_first():
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "content-length": "0",
        "origin": "https://match.yuanrenxue.cn",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "referer": "https://match.yuanrenxue.cn/match/3",
        "sec-ch-ua": "\"Chromium\";v=\"136\", \"Google Chrome\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    }
    cookies = {
        "sessionid": "9v4dut5gjjvapw0ox3ls3mp5rt5p3yov",
        "qpfccr": "true",
        "Hm_lvt_434c501fe98c1a8ec74b813751d4e3e3": "1745473253,1745670989,1745930833,1746704613",
        "Hm_lvt_c99546cf032aaa5a679230de9a95c7db": "1746345812,1746622031,1746704061,1746708668",
        "HMACCOUNT": "74E03469813A9187",
        "no-alert3": "true",
        "Hm_lvt_9bcbda9cbf86757998a2339a0437208e": "1745930809,1746345846,1746704066,1746708671",
        "Hm_lpvt_9bcbda9cbf86757998a2339a0437208e": "1746715233",
        "Hm_lpvt_c99546cf032aaa5a679230de9a95c7db": "1746716911"
    }

    url = "https://match.yuanrenxue.cn/jssm"
    response = session.post(url, headers=headers, cookies=cookies)

    print(response.text)
    print(response)


if __name__ == '__main__':
    res = []
    session = requests.Session()
    for i in range(1, 6):
        first = get_first()
        data = get_resp(str(i))
        nums = parse_data(data)
        res.extend(nums)

    print(sum(res) // len(res))
