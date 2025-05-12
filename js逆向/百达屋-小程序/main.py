import requests
import time
import execjs
import uuid

headers = {
    'Connection': 'keep-alive',
    'BusinessType': '1',
    'MessageId': str(uuid.uuid1()),
    'pageSize': '20',
    'pageNo': '1',
    'AppType': '2',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1 wechatdevtools/1.06.2407110 MicroMessenger/8.0.5 Language/zh_CN webview/',
    'content-type': 'application/json',
    'AppVersion': '3.3.5',
    'OsVersion': 'iOS 10.0.1',
    'DeviceManufacture': 'devtools',
    # 'Signature': 'B1950BF201295BC451CC737E',
    'Channel': 'bdw',
    'Timestamp': str(int(time.time() * 1000)),
    'ClientType': '5',
    'DeviceModel': 'iPhone 12/13 (Pro)',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://servicewechat.com/wx4f7fd5dc9bc0cd35/devtools/page-frame.html',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

sign = execjs.compile(open('bdw.js', encoding='utf-8').read()).call('get_sign', headers)
print(sign)

headers['Signature'] = sign

json_data = {
    'querySource': 2,
    'channelType': 1,
    'sourceType': 10,
    'serviceType': [
        '3',
    ],
    'searchType': 0,
    'dateStartTime': 1739376000000,
    'dateEndTime': 1739462400000,
    'destination': '重庆',
}

response = requests.post('https://api.betterwood.com/base/app/store/listV2', headers=headers, json=json_data)

print(response.json())
