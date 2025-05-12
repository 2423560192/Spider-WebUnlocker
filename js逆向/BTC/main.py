"""
url: https://www.oklink.com/zh-hans
"""

import requests
import execjs

cookies = {
    'aliyungf_tc': 'a56047127cb19fb91c6434cc3e36fe7eda2ad967c9d8327e23389cfb5961d4a5',
    'devId': 'a423b052-4b28-4e5c-a51d-498d3cad5536',
    'ok_site_info': '9FjOikHdpRnblJCLiskTJx0SPJiOiUGZvNmIsIiTDJiOi42bpdWZyJye',
    'locale': 'zh_CN',
    'ok-exp-time': '1729580722666',
    'browserVersionLevel': 'v5.6ad2a8e37c01',
    'okg.currentMedia': 'xl',
    'oklink.unaccept_cookie': '1',
    'first_ref': 'https%3A%2F%2Fwww.oklink.com%2Fzh-hans%2Fapi-plans',
    'ok-ses-id': 'pMyODblOwBZunP2YouspzlgX/vAL5N7tdyUgApk+H5YAlAGY04n+pipLxdfWdtyjY1qdMpxD4HLN0xc9FXhKWepOochHWWaPlhmmp+95Rw1G3otAz4FHXkI4jcppcCsv',
    '_monitor_extras': '{"deviceId":"nJNFzDJq3tRRGVh9hO74yd","eventId":30,"sequenceNumber":30}',
    'amp_d77757': 'a423b052-4b28-4e5c-a51d-498d3cad5536...1iapgmqep.1iapguojg.t.0.t',
    'traceId': '2040195809884250001',
}

js = execjs.compile(open('jiemi.js').read())
key = js.call('u')
print('key', key)

headers = {
    'accept': 'application/json',
    'accept-language': 'zh-CN,zh;q=0.9',
    'app-type': 'web',
    # 'cookie': 'aliyungf_tc=a56047127cb19fb91c6434cc3e36fe7eda2ad967c9d8327e23389cfb5961d4a5; devId=a423b052-4b28-4e5c-a51d-498d3cad5536; ok_site_info=9FjOikHdpRnblJCLiskTJx0SPJiOiUGZvNmIsIiTDJiOi42bpdWZyJye; locale=zh_CN; ok-exp-time=1729580722666; browserVersionLevel=v5.6ad2a8e37c01; okg.currentMedia=xl; oklink.unaccept_cookie=1; first_ref=https%3A%2F%2Fwww.oklink.com%2Fzh-hans%2Fapi-plans; ok-ses-id=pMyODblOwBZunP2YouspzlgX/vAL5N7tdyUgApk+H5YAlAGY04n+pipLxdfWdtyjY1qdMpxD4HLN0xc9FXhKWepOochHWWaPlhmmp+95Rw1G3otAz4FHXkI4jcppcCsv; _monitor_extras={"deviceId":"nJNFzDJq3tRRGVh9hO74yd","eventId":30,"sequenceNumber":30}; amp_d77757=a423b052-4b28-4e5c-a51d-498d3cad5536...1iapgmqep.1iapguojg.t.0.t; traceId=2040195809884250001',
    'devid': 'a423b052-4b28-4e5c-a51d-498d3cad5536',
    'priority': 'u=1, i',
    'referer': 'https://www.oklink.com/zh-hans/alpha-signals',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'x-apikey': key,
    'x-cdn': 'https://static.oklink.com',
    'x-id-group': '2040195809884250001-c-1',
    'x-locale': 'zh_CN',
    'x-site-info': '9FjOikHdpRnblJCLiskTJx0SPJiOiUGZvNmIsIiTDJiOi42bpdWZyJye',
    'x-utc': '8',
    'x-zkdex-env': '0',
}

params = {
    't': '1729580987898',
}

response = requests.get(
    'https://www.oklink.com/api/explorer/v2/index/all-chain-order',
    params=params,
    cookies=cookies,
    headers=headers,
)

print(response.text)