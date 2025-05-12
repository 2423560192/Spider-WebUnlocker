"""
https://www.jinglingshuju.com/articles
"""
import requests

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://www.jinglingshuju.com',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

data = {
    'page': '2',
    'num': '20',
    'uid': 'undefined',
}

response = requests.post('https://vapi.jinglingshuju.com/Data/getNewsList', headers=headers, data=data)

print(response.json())

import execjs

data = execjs.compile(open('loader.js').read()).call('get_data' , response.json()['data'])
print(data)



