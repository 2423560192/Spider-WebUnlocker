"""
https://www.jiansheku.com/search/enterprise/
"""
import json
import time

import execjs

import requests

cookies = {
    'Hm_lvt_03b8714a30a2e110b8a13db120eb6774': '1735278707',
    'HMACCOUNT': '74E03469813A9187',
    'HWWAFSESID': 'e74468837c46ceaa96',
    'HWWAFSESTIME': '1735278705124',
    'Hm_lpvt_03b8714a30a2e110b8a13db120eb6774': '1735278718',
}

json_data = {
    'eid': '',
    'achievementQueryType': 'and',
    'achievementQueryDto': [],
    'personnelQueryDto': {
        'queryType': 'and',
    },
    'aptitudeQueryDto': {
        'queryType': 'and',
        'nameStr': '',
        'aptitudeQueryType': 'and',
        'businessScopeQueryType': 'or',
        'filePlaceType': '1',
        'aptitudeDtoList': [
            {
                'codeStr': '',
                'queryType': 'and',
                'aptitudeType': 'qualification',
            },
        ],
        'aptitudeSource': 'new',
    },
    'page': {
        'page': 2,
        'limit': 20,
        'field': '',
        'order': '',
    },
}

timestamp = str(int(time.time() * 1000))

print(timestamp)

sign = execjs.compile(open('loader.js', 'r', encoding='utf-8').read()).call('get_sign', json_data, timestamp)
print(sign)

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/json;charset=UTF-8',
    # 'cookie': 'Hm_lvt_03b8714a30a2e110b8a13db120eb6774=1735278707; HMACCOUNT=74E03469813A9187; HWWAFSESID=e74468837c46ceaa96; HWWAFSESTIME=1735278705124; Hm_lpvt_03b8714a30a2e110b8a13db120eb6774=1735278718',
    'devicetype': 'PC',
    'origin': 'https://www.jiansheku.com',
    'page': 'search-enterprise',
    'priority': 'u=1, i',
    'referer': 'https://www.jiansheku.com/',
    'sign': sign,
    'timestamp': timestamp,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

response = requests.post('https://capi.jiansheku.com/nationzj/enterprice/page', cookies=cookies, headers=headers,
                         json=json_data)

print(response.json())
