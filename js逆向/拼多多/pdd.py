import requests

import execjs

import requests

headers = {
    'Accept': 'application/json, text/javascript',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Origin': 'https://www.pinduoduo.com',
    'Referer': 'https://www.pinduoduo.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

anti_content = execjs.compile(open('./run.js').read()).call('get_anti_content')
print(anti_content)

params = {
    'tf_id': 'TFRQ0v00000Y_13400',
    'page': '1',
    'size': '39',
    'anti_content': anti_content,
}

response = requests.get('https://apiv2.pinduoduo.com/api/gindex/tf/query_tf_goods_info', params=params, headers=headers)

print(response.text)
