import requests

import execjs

cookies = {
    'face': 'undefined',
    'locale': 'zh_CN',
    'saveUsername': 'true',
    'domain': '',
    'uid': '17782200192%40wo.cn',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    # 'Cookie': 'face=undefined; locale=zh_CN; saveUsername=true; domain=; uid=17782200192%40wo.cn',
    'Origin': 'https://mail.wo.cn',
    'Referer': 'https://mail.wo.cn/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

params = {
    'cus': '1',
    'sid': 'IAfAWlppNYepcVuCESNRNAihJCGOEbdl',
}

js = execjs.compile(open('./loader.js').read())

pwd = js.call('get_sign', 'Cs5201314dongge.')

print(pwd)

data = {
    'locale': 'zh_CN',
    'nodetect': 'false',
    'destURL': '',
    'supportLoginDevice': 'true',
    'accessToken': '',
    'timestamp': '',
    'signature': '',
    'nonce': '',
    'device': '{"uuid":"webmail_windows","imie":"webmail_windows","friendlyName":"chrome 130","model":"windows","os":"windows","osLanguage":"zh-CN","deviceType":"Webmail"}',
    'supportDynamicPwd': 'true',
    'supportBind2FA': 'true',
    'authorizeDevice': '',
    'loginType': '',
    'uid': '17782200192',
    'domain': '',
    'password': pwd,
    'action:login': '',
}

response = requests.post('https://mail.wo.cn/coremail/index.jsp', params=params, cookies=cookies, headers=headers,
                         data=data)

print(response.text)
