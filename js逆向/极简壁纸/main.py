import requests

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://bz.zzzmh.cn',
    'priority': 'u=1, i',
    'referer': 'https://bz.zzzmh.cn/',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
}

json_data = {
    'size': 24,
    'current': 2,
    'sort': 0,
    'category': 0,
    'resolution': 0,
    'color': 0,
    'categoryId': 0,
    'ratio': 0,
}

response = requests.post('https://api.zzzmh.cn/v2/bz/v3/getData', headers=headers, json=json_data)

print(response.text)