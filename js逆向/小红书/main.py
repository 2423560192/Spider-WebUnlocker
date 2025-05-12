import requests

import json

import execjs

cookies = {
    'abRequestId': 'd9b7b7d3-db34-5a78-b11e-a798c15e0b49',
    'a1': '19306a5c831clugjnsz2x8ueuh304hvdqqvw8z1da50000304720',
    'webId': 'abbe710385045283578e34747aeeaccd',
    'gid': 'yjq8K02f4WA0yjq8K02SYAuyqyS17kVIMuJChf0Y7d7xqE2884xhfY888q84WJ88dJ4Y0WY2',
    'web_session': '030037a01fe1c23176309ff11f204a6dff29df',
    'xsecappid': 'xhs-pc-web',
    'webBuild': '4.56.0',
    'acw_tc': '0a0bb22a17397857418435224eca44997cecfa1988b093df49d42233137510',
    'websectiga': '9730ffafd96f2d09dc024760e253af6ab1feb0002827740b95a255ddf6847fc8',
    'sec_poison_id': '9199db2e-d62c-4f74-99e5-67dbc799c2cd',
    'unread': '{%22ub%22:%22678f22b4000000002900e697%22%2C%22ue%22:%226791bfed000000002902cf3c%22%2C%22uc%22:25}',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://www.xiaohongshu.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.xiaohongshu.com/',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'x-b3-traceid': 'ec75e103318e83cd',
    'x-mns': 'awnZYvYh008nbS+WnhuIzcF0xtI143J4JkQIlzyDdxDw9j1/XD76da0nWw4aCbT5YiGNceZf94t/5CS2m5OEi4o9ovR+uBPu1x9OMOo6ToBKLeiipIizvBH+FI2QNfixIQOySFj1ES5Fz7FziZdviDkYP2n901dYIbOmKkoZ57g9buy9QgynSgnMbTxDH8vCYo0JvmPRWTo8oKaJ/Ho2N/TH3403755ZOL+Git+aTHTLC7GvgQ9ZY/hpTz7xfKo6hDi7d/S1gMWSPSZylzjhI9kMk0dj9LM2jYdkYbP1GuG0b1OcZLzOP5TfXgbhbt8F3zbbTpIgSelpBRh3fOENhR5aMtcXomnxmfXJaDiMOT5LQKPOnTJxDuJbLRBbPEt1FjyeFZtEY4BPgQlYHwKZTS3DWoyNcJzvKXWo69GlbQb7/am5/2cdhYyKNTgEoZFvzxZxOOXKa3BoIbXvK00Qjd8uzcy/yfmbXST/jXKzNQLmf4dPTK/Jjio1i7dL',
    # 'x-s': 'XYW_eyJzaWduU3ZuIjoiNTYiLCJzaWduVHlwZSI6IngyIiwiYXBwSWQiOiJ4aHMtcGMtd2ViIiwic2lnblZlcnNpb24iOiIxIiwicGF5bG9hZCI6IjI3Y2Y0NDEyODk4ZTQxYjllNmQwNDNhOWExYWM5YjA3ODNiMjNhYzllMzMwNTliNzY3YmE2ODk2MTZlZWQwNjMyODQwMmFkODIzOTYzZWE1N2IzZjI3NjMyYjg4NjE5ZjE4MjJlYjg4Yjg4OGZkM2MyYmJkODE0YTVjOTk0NTk4NGFiZmNmZWY2OTNiYjgyNmM2ZmE0MDBkMGM1NGI0NzdhY2YxZmJhMGUxMjZjN2M5ZWEwMDcyYmUwZGJmYTY1NjgyMTk1ZDQyYzRiNzBiMzg2ZTI2ODcyMzIwYjkwNjIwZjI5OTBkOWRjMDhkZTcwM2RmZWM5ZTc0ZjdiMzA3NjlmZDJmZTk1ZjExNDNlNWY2MDZjYzZhNmQ5ODVhNzNmN2Y1M2QyYjYyMDM5NDZmNGM2MjA3YjEwY2JmNjk1ZTc2YjdlMTZiYjQwNTExNGNkYzM1YTMxMzgxNjYxZDg4NDE0MDUwMmJmOTA1NzRhZDhkYmFhOGM2YTM5NzUxZmRkMWRkMjhiNWY4NTA2OWQzMjU3MGRmNjVlMGQ1MDRhMzllIn0=',
    'x-s-common': '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',
    # 'x-t': '1739785751129',
    'x-xray-traceid': 'ca89a7e5254490b63edf631a8ce24337',
    # 'cookie': 'abRequestId=d9b7b7d3-db34-5a78-b11e-a798c15e0b49; a1=19306a5c831clugjnsz2x8ueuh304hvdqqvw8z1da50000304720; webId=abbe710385045283578e34747aeeaccd; gid=yjq8K02f4WA0yjq8K02SYAuyqyS17kVIMuJChf0Y7d7xqE2884xhfY888q84WJ88dJ4Y0WY2; web_session=030037a01fe1c23176309ff11f204a6dff29df; xsecappid=xhs-pc-web; webBuild=4.56.0; acw_tc=0a0bb22a17397857418435224eca44997cecfa1988b093df49d42233137510; websectiga=9730ffafd96f2d09dc024760e253af6ab1feb0002827740b95a255ddf6847fc8; sec_poison_id=9199db2e-d62c-4f74-99e5-67dbc799c2cd; unread={%22ub%22:%22678f22b4000000002900e697%22%2C%22ue%22:%226791bfed000000002902cf3c%22%2C%22uc%22:25}',
}

json_data = {
    'cursor_score': '',
    'num': 35,
    'refresh_type': 1,
    'note_index': 35,
    'unread_begin_note_id': '',
    'unread_end_note_id': '',
    'unread_note_count': 0,
    'category': 'homefeed_recommend',
    'search_key': '',
    'need_num': 10,
    'image_formats': [
        'jpg',
        'webp',
        'avif',
    ],
    'need_filter_image': False,
}

p = '/api/sns/web/v1/homefeed'

json_data = json.dumps(json_data, separators=(',', ':'))

res = execjs.compile(open('source.js', encoding='utf-8').read()).call('get_x_s', p, json_data)

print(res)

x_s = res['X-s']

x_t = res['X-t']

print(x_s)
print(x_t)
#
headers["x-s"] = x_s
headers["x-t"] = str(x_t)

print(headers)

response = requests.post('https://edith.xiaohongshu.com/api/sns/web/v1/homefeed', cookies=cookies, headers=headers,
                         data=json_data)

print(response.json())
