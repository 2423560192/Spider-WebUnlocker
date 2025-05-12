"""
https://search.bidcenter.com.cn/search?keywords=%e6%9c%8d%e5%8a%a1%e5%99%a8
"""

import execjs

import requests

headers = {
    'accept': 'text/plain, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://search.bidcenter.com.cn',
    'priority': 'u=1, i',
    'referer': 'https://search.bidcenter.com.cn/',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

data = {
    'from': '6137',
    'guid': '7224fe25-bf72-4d10-b7b7-18156d589910',
    'location': '6138',
    'token': '',
    'next_token': '',
    'keywords': '%E6%9C%8D%E5%8A%A1%E5%99%A8',
    'mod': '0',
    'page': '2',
}

response = requests.post('https://interface.bidcenter.com.cn/search/GetSearchProHandler.ashx', headers=headers,
                         data=data)



print(response.text)

print(execjs.compile(open('loader.js').read()).call('get_aes', response.text))
