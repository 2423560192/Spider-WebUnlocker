import time
import execjs



header = execjs.compile(open('loader.js').read()).call('get_sign')
print(header)



import requests

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://m.cnhnb.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://m.cnhnb.com/',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36',
    'x-b3-traceid': '0M5S9KIXCXI57AXZ',
    'x-client-appid': '5',
    'x-client-environment': 'pro',
}

headers.update(header)
print(headers)

json_data = {
    'pageNumber': 1,
    'pageSize': 8,
    'ad_ch': 1,
}

response = requests.post('https://appapi.cnhnb.com/recq/api/transform/supply/v501/index', headers=headers,
                         json=json_data)

print(response.json())
