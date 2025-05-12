import requests
import execjs

from  urllib.parse import quote
params = {
    "cityCode": "110100",
    "pageIndex": 2,
    "pageSize": 12,
    "keyword": quote('英语'),
    "order": "0"
}

res = execjs.compile(open('loader.js', encoding='utf-8').read()).call('get_sign', params)
print(res)

sign = res['sign']
params = res['params']
print(params)

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://souke.xdf.cn',
    'priority': 'u=1, i',
    'referer': 'https://souke.xdf.cn/search?cityCode=110100&kw=%E8%8B%B1%E8%AF%AD',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'sign': sign,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

response = requests.get('https://dsapi.xdf.cn/product/v2/class/search?' + params, headers=headers)

print(response.json())
