import requests

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
    'sign': 'd958f5847c3febfbb31e0ed46b9f4ee6',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

params = {
    'appId': '5053',
    't': '1736244596678',
    'cityCode': '110100',
    'pageIndex': '1',
    'pageSize': '12',
    'keyword': '英语',
    'order': '0',
}

response = requests.get('https://dsapi.xdf.cn/product/v2/class/search', params=params, headers=headers)

print(response.json())