import requests

cookies = {
    'lianjia_uuid': 'cba19070-1545-448a-b4a9-5047867f62be',
    'select_city': '500000',
    'lianjia_ssid': '8e76cf9e-1917-42b8-9825-5ee86b86d3ef',
    'Hm_lvt_b160d5571570fd63c347b9d4ab5ca610': '1736399920',
    'HMACCOUNT': '74E03469813A9187',
    'sajssdk_2015_cross_new_user': '1',
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%2219449801a7324ea-0c85435d4a24b8-26011851-1638720-19449801a742665%22%2C%22%24device_id%22%3A%2219449801a7324ea-0c85435d4a24b8-26011851-1638720-19449801a742665%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24latest_referrer_host%22%3A%22www.google.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D',
    'Hm_lpvt_b160d5571570fd63c347b9d4ab5ca610': '1736399988',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    # 'Cookie': 'lianjia_uuid=cba19070-1545-448a-b4a9-5047867f62be; select_city=500000; lianjia_ssid=8e76cf9e-1917-42b8-9825-5ee86b86d3ef; Hm_lvt_b160d5571570fd63c347b9d4ab5ca610=1736399920; HMACCOUNT=74E03469813A9187; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219449801a7324ea-0c85435d4a24b8-26011851-1638720-19449801a742665%22%2C%22%24device_id%22%3A%2219449801a7324ea-0c85435d4a24b8-26011851-1638720-19449801a742665%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24latest_referrer_host%22%3A%22www.google.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D; Hm_lpvt_b160d5571570fd63c347b9d4ab5ca610=1736399988',
    'Origin': 'https://cq.ke.com',
    'Referer': 'https://cq.ke.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

import execjs

pwd = execjs.compile(open('loader.js' , encoding='utf-8').read()).call('get_pwd' , '12345678cs')

print(pwd)

json_data = {
    'service': 'https://ajax.api.ke.com/login/login/getuserinfo',
    'mainAuthMethodName': 'username-password',
    'accountSystem': 'customer',
    'credential': {
        'username': '17782200192',
        'password': pwd,
        'encodeVersion': '2',
    },
    'context': {
        'ua': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'clientSource': 'pc',
        'os': 'Windows',
        'osVersion': '10',
        'registerPosLx': 824.8333740234375,
        'registerPosLy': 237.1666717529297,
        'registerPosRx': 1104.8333740234375,
        'registerPosRy': 281.1666717529297,
        'clickPosX': 960,
        'clickPosY': 268,
        'screen': '1691_421',
        'dataId': 'uZYOqT81IvC41sXBxffWEkEUd/rSQs20S7Aan00/1mdv0Ywj9iN6ckzyf/UNTzKQ',
    },
    'loginTicketId': 'gAp51i2VU9uBuzPIfGkJXscbCgZZFA3R',
    'version': '2.0',
    'srcId': 'eyJ0Ijoie1wiZGF0YVwiOlwiZDFiMTc4MGE2MTIwMzFkZWU2ZTI4YzM5MjhkNjUwYTZlN2ZhMTRjMzU1YTNlMGJmNzQxODgxYjhhODkzNWRjZGYyYTYwZWVlYzc2MjNiM2E1ODUyOTA4YmE5NGI5N2IzODcyYjRhZTA1MDA5YjBkNzJjMmEzNzA0N2U5MDJkMjZkY2U2MWQzNTZmYmZmZjgyMzcwZTk1YmY0ZWU4OTFhMTUxMGRmZWM4MjhmMmFjNTE4YmNiOTA5NTFkNjU5MThmZGNjYzBmNGYxNmRmMzc3NzZkNzUyNmFhNGNiMzQzNmNiZGI0ZGU3YmY0MTY5Mzk5MzBmMzE5Yjk4YjUxNjg3M1wiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCIxMjZjMWMyZVwifSIsInIiOiJodHRwczovL2NxLmZhbmcua2UuY29tL2xvdXBhbi8iLCJvcyI6IndlYiIsInYiOiIwLjEifQ==',
    'ticketMaxAge': 604800,
}

response = requests.post('https://clogin.ke.com/authentication/authenticate', cookies=cookies, headers=headers, json=json_data)

print(response.json())

