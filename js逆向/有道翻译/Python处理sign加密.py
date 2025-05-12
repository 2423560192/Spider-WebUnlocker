import requests
import time
import hashlib
import subprocess
from functools import partial
subprocess.Popen = partial(subprocess.Popen, encoding="UTF-8")

tt = str(int(time.time() * 1000))
e = 'fsdsogkndfokasodnaso'
d = "fanyideskweb"
u = "webfanyi"


def encryp_data():
    m = hashlib.md5()
    i = f'client={d}&mysticTime={tt}&product={u}&key={e}'
    m.update(i.encode())
    res = m.hexdigest()
    print(res, tt)
    return res


sign = encryp_data()

cookies = {
    'OUTFOX_SEARCH_USER_ID': '994334556@123.147.249.82',
    'OUTFOX_SEARCH_USER_ID_NCOO': '649308628.0593178',
    '_uetsid': '2e2b7e207cc311efbbc427a271523435',
    '_uetvid': 'f6e2c4007bc811efa752ebc996289615',
    'DICT_DOCTRANS_SESSION_ID': 'NTI1NTQxMzgtYmE2Yy00YzUyLWFiMTItZjU5ZjE0YzIwZDA2',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    # 'Cookie': 'OUTFOX_SEARCH_USER_ID=994334556@123.147.249.82; OUTFOX_SEARCH_USER_ID_NCOO=649308628.0593178; _uetsid=2e2b7e207cc311efbbc427a271523435; _uetvid=f6e2c4007bc811efa752ebc996289615; DICT_DOCTRANS_SESSION_ID=NTI1NTQxMzgtYmE2Yy00YzUyLWFiMTItZjU5ZjE0YzIwZDA2',
    'Origin': 'https://fanyi.youdao.com',
    'Referer': 'https://fanyi.youdao.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

data = {
    'i': 'apple',
    'from': 'auto',
    'to': '',
    'useTerm': 'false',
    'dictResult': 'true',
    'keyid': 'webfanyi',
    'sign': sign,
    'client': 'fanyideskweb',
    'product': 'webfanyi',
    'appVersion': '1.0.0',
    'vendor': 'web',
    'pointParam': 'client,mysticTime,product',
    'mysticTime': tt,
    'keyfrom': 'fanyi.web',
    'mid': '1',
    'screen': '1',
    'model': '1',
    'network': 'wifi',
    'abtest': '0',
    'yduuid': 'abcdefg',
}

response = requests.post('https://dict.youdao.com/webtranslate', cookies=cookies, headers=headers, data=data)
print(response.text)

# 对结果进行解密

import execjs

with open("js结果解密.js") as f:
    js_code = f.read()

js_compile = execjs.compile(js_code)
key = 'ydsecret://query/key/B*RGygVywfNBwpmBaZg*WT7SIOUP2T0C9WHMZN39j^DAdaZhAnxvGcCY6VYFwnHl'
iv = 'ydsecret://query/iv/C@lZe2YzHtZ2CYgaXKSVfsb7Y4QWHjITPPZ0nQp87fBeJ!Iv6v^6fvi2WN@bYpJ4'
s = js_compile.call("jiemi", response.text)
print(s)
