import json

import requests

import execjs

cookies = {
    'abRequestId': 'e19b7a31-6084-54e5-aa98-525bdf246c4f',
    'webBuild': '4.55.1',
    'xsecappid': 'xhs-pc-web',
    'a1': '194a1492acbaxih9c2fcducad5o7hvvw8uvlu405z50000817150',
    'webId': 'a751d249712ac3024d891c25c924dd54',
    'web_session': '030037a0a6813a70ad070293ed204a6e88f0ae',
    'gid': 'yj40y4jqi2Yiyj40y4jJ0748SD0C3xjSJiSfh2u7S0f2l128WxhhE7888YyWy288fqid840q',
    'acw_tc': '0a0b147517378766418502793eb32087b92ad87ed3ac68d486cc89bf570ec9',
    'websectiga': '6169c1e84f393779a5f7de7303038f3b47a78e47be716e7bec57ccce17d45f99',
    'sec_poison_id': '1f480678-349e-4c41-93da-d7c09feb8282',
    'unread': '{%22ub%22:%22676f4790000000001300dc47%22%2C%22ue%22:%226777354c000000000902f191%22%2C%22uc%22:26}',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json;charset=UTF-8',
    # 'cookie': 'abRequestId=e19b7a31-6084-54e5-aa98-525bdf246c4f; webBuild=4.55.1; xsecappid=xhs-pc-web; a1=194a1492acbaxih9c2fcducad5o7hvvw8uvlu405z50000817150; webId=a751d249712ac3024d891c25c924dd54; web_session=030037a0a6813a70ad070293ed204a6e88f0ae; gid=yj40y4jqi2Yiyj40y4jJ0748SD0C3xjSJiSfh2u7S0f2l128WxhhE7888YyWy288fqid840q; acw_tc=0a0b147517378766418502793eb32087b92ad87ed3ac68d486cc89bf570ec9; websectiga=6169c1e84f393779a5f7de7303038f3b47a78e47be716e7bec57ccce17d45f99; sec_poison_id=1f480678-349e-4c41-93da-d7c09feb8282; unread={%22ub%22:%22676f4790000000001300dc47%22%2C%22ue%22:%226777354c000000000902f191%22%2C%22uc%22:26}',
    'origin': 'https://www.xiaohongshu.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.xiaohongshu.com/',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'x-b3-traceid': '39561163a13055a9',
    'x-mns': 'awvpnQF60fESpwGCvgX3G+T8Pk+c9gOyvWb0+l9NF9MFz6wJYKoXJa7vW4dHoMNiPwEwt4uPuQ36POfzFvpaO9/OBzBd/DScMvKyatCtQlyj5F9udNKWmM89KwJJ6nDyP4x+wSDcWvz1F8uXBCZ3+v2Zlw1OMBPkMTb9+m0WIgB3IXShj4yckMxG9M4mtRk+3PWLkNl9+IfHQ1jN//FMpkZGIWa5/aWtRNQyumb3mwvOx5T98lWT6JLYjE+oWC/w1lhO+0zbzMcBIpIGy7ZGjOE1z8mcoJmGwozkwo8Qxb1FdmOL96hFtEMTWflQbLy/GwknTCa9/ZuNLtipSpKR0uZ7CRgyRCadIFMjNkYPwjnxmKNnd4kEoyonKLa5Q7z82tbhn6aQl5ImtxQLDgyc8COB/zHkdEDLT0tM/PWtGHG/jMoa9onoZhQ2e/kmG0KtKYHe0R+L1vdhy545w0cE0btIMIBbYmvZ9OWjEO1HTMeYEx+uaSFnoR8YBEYGo7GeJ',
    'x-s': 'XYW_eyJzaWduU3ZuIjoiNTYiLCJzaWduVHlwZSI6IngyIiwiYXBwSWQiOiJ4aHMtcGMtd2ViIiwic2lnblZlcnNpb24iOiIxIiwicGF5bG9hZCI6ImFiODNmZjhlYTdiZTFiODY0M2E0YzE4NDk3ZTA4YzY1MmQyMmI5MjUzMWYxY2FlZDUwY2Y4ZmM5MjY2MTQ2OTk0MTI5MzRiZjQzMTgxN2U0YjcxMDAyYTRiZTRjNGIzZWIzNWFiNzJkOTM2NTFiMjVlOGI3YjBmMjJhMGVjMWQ3ZGNjZDk3YmIyNmQ3MmU0N2UxYTZkNzMzZDQwMDM5MTk1N2ZiNWVlOTZmM2E3YzgwMGM4ZDZiOWY3ZjMyOGJkNmExYWUyMTU0ZTY2ZjczOTY5OWI2MzI5NzcyNmNjYWFlNTIwMDZlYzU5NmVmNmQxYjY3MjZmMWMyMTg3MTVmNDM0NTUwZTExYzY0ZGQ2YjJkNjQwOWRjNjcwMGRlMTUxN2ZkYjVmZmYzM2U0MTYzZjUyYTgxNjYxMjg2ZmUxOTVlMTQ0NmIzOWUzYjg2MDNlNDFmMThlN2I2MWQyZTIxOWE1YWI1Zjg4OTJkZDAzZTNkYWIzNjgwNjQ3OTNiYzJjYTdhYzUyMjZiMWM0NzBiNDg4ZWJhY2RhYWQwNTBhNTNhIn0=',
    'x-s-common': '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',
    'x-t': '1737878194419',
    'x-xray-traceid': 'ca50ce6473b8e6612b1f7c04d14a9841',
}

json_data = {
    'cursor_score': '',
    'num': 35,
    'refresh_type': 1,
    'note_index': 36,
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

res = execjs.compile(open('source.js', encoding='utf-8').read()).call('get_x_s', p, json_data)

json_data = json.dumps(json_data, separators=(',', ':'))


print(res)

x_s = res['X-s']

x_t = res['X-t']

print(x_s)
print(x_t)
#
headers["x-s"] = x_s
headers["x-t"] = str(x_t)

response = requests.post('https://edith.xiaohongshu.com/api/sns/web/v1/homefeed', cookies=cookies, headers=headers,
                         data=json_data)

print(response.json())