"""
url: https://www.dxy.cn/bbs/newweb/pc/case/search?keyword=%E7%96%AB%E6%83%85
"""
import random
import time

import requests

import execjs

cookies = {
    'dxy_da_cookie-id': 'dbbbb255af00996f399e4632c08cdf741729231890200',
    '_ga': 'GA1.1.856206800.1729231891',
    'ifVisitOldVerBBS': 'false',
    'JUTE_SESSION_ID': 'c8549fdd-c8fd-4124-a31f-22546f871406',
    'Hm_lvt_5fee00bcc4c092fe5331cc51446d8be2': '1729231891,1729516903',
    'Hm_lpvt_5fee00bcc4c092fe5331cc51446d8be2': '1729516903',
    'HMACCOUNT': '74E03469813A9187',
    '_ga_LTBPLJJK75': 'GS1.1.1729516902.3.0.1729516902.0.0.0',
}

headers = {
    'accept': 'application/json',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/json;charset=utf-8',
    # 'cookie': 'dxy_da_cookie-id=dbbbb255af00996f399e4632c08cdf741729231890200; _ga=GA1.1.856206800.1729231891; ifVisitOldVerBBS=false; JUTE_SESSION_ID=c8549fdd-c8fd-4124-a31f-22546f871406; Hm_lvt_5fee00bcc4c092fe5331cc51446d8be2=1729231891,1729516903; Hm_lpvt_5fee00bcc4c092fe5331cc51446d8be2=1729516903; HMACCOUNT=74E03469813A9187; _ga_LTBPLJJK75=GS1.1.1729516902.3.0.1729516902.0.0.0',
    'priority': 'u=1, i',
    'referer': 'https://www.dxy.cn/bbs/newweb/pc/case/search?keyword=%E7%96%AB%E6%83%85',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
}

params = {
    'keyword': '疫情',
    'sectionCode': '0',
    'pageSize': '20',
    'pageNum': '2',
    'serverTimestamp': int(time.time() * 1000) - 2,
    'timestamp': int(time.time() * 1000),
    'noncestr': str(random.randint(0, 100000000)).rjust(8, '0'),
}
print(params)

# 加密
f = f'appSignKey=4bTogwpz7RzNO2VTFtW7zcfRkAE97ox6ZSgcQi7FgYdqrHqKB7aGqEZ4o7yssa2aEXoV3bQwh12FFgVNlpyYk2Yjm9d2EZGeGu3&keyword={params["keyword"]}&noncestr={params["noncestr"]}&pageNum={params["pageNum"]}&pageSize={params["pageSize"]}&sectionCode=0&serverTimestamp={params["serverTimestamp"]}&timestamp={params["timestamp"]}'

js = execjs.compile(open('js逆向.js').read())
sign = js.call('u', f)
print('sign', sign)
params['sign'] = sign



response = requests.get('https://www.dxy.cn/bbs/newweb/case-bank/page-post-info', params=params, cookies=cookies,
                        headers=headers)

res = response.text

print(res)
