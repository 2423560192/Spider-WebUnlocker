import requests

cookies = {
    'HMF_CI': 'd71d8f1324059c9901febcfb6962950e096984fad4f84451dc89af3e0e755c356b7867737f5099cecee81b21b8214c6771eecf41d3a66eaede700c2a1b19eb6999',
    'FECW': 'c271796ce23247e22a67aa5d25df3f7e64507cb11fbca46dc83f83a10b694e7d2cf58eb17a2fc63579d7e7c5f1c0924b1d4f3915c69e49f991536b6c9f42fd5a37374951dc52918a5d86ab4a8a5f96aadc',
    'cookiePolicy': 'Accepted',
    'cookiePreference': 'Accepted',
    'unified_account_switch': 'true',
    'Hm_lvt_d16e4336470e6b4d88aa16ff927d7daf': '1730113459',
    'Hm_lpvt_d16e4336470e6b4d88aa16ff927d7daf': '1730113459',
    'HMACCOUNT': '74E03469813A9187',
    'django_language': 'zh-cn',
    'sessionid': 'ehiut32d016asnw0bdwh5utyr8xoe0je',
    'FECA': 'cr1fvpz5fd0bCauyzlaQNPkX0rAUEzucpQtSY4kqCLRTbuXBICpotYxDUpX75wg6t7zbHBLcKYW4RtPfZhwEjgfIg2ceyFkjxq5LZ3SYM/MtmrOaQJHsN0ijH6gaLMC1t8qWz4j0P6QUD57hdneAzPCbORoeCBBPFJjLIZwaZnD+tUNBqkJNGZGcJ0TcMPnOV5',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    # 'Cookie': 'HMF_CI=d71d8f1324059c9901febcfb6962950e096984fad4f84451dc89af3e0e755c356b7867737f5099cecee81b21b8214c6771eecf41d3a66eaede700c2a1b19eb6999; FECW=c271796ce23247e22a67aa5d25df3f7e64507cb11fbca46dc83f83a10b694e7d2cf58eb17a2fc63579d7e7c5f1c0924b1d4f3915c69e49f991536b6c9f42fd5a37374951dc52918a5d86ab4a8a5f96aadc; cookiePolicy=Accepted; cookiePreference=Accepted; unified_account_switch=true; Hm_lvt_d16e4336470e6b4d88aa16ff927d7daf=1730113459; Hm_lpvt_d16e4336470e6b4d88aa16ff927d7daf=1730113459; HMACCOUNT=74E03469813A9187; django_language=zh-cn; sessionid=ehiut32d016asnw0bdwh5utyr8xoe0je; FECA=cr1fvpz5fd0bCauyzlaQNPkX0rAUEzucpQtSY4kqCLRTbuXBICpotYxDUpX75wg6t7zbHBLcKYW4RtPfZhwEjgfIg2ceyFkjxq5LZ3SYM/MtmrOaQJHsN0ijH6gaLMC1t8qWz4j0P6QUD57hdneAzPCbORoeCBBPFJjLIZwaZnD+tUNBqkJNGZGcJ0TcMPnOV5',
    'Origin': 'https://synconhub.coscoshipping.com',
    'Referer': 'https://synconhub.coscoshipping.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'X-Client-Timestamp': '1730113485624',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

params = {
    'FECU': 'cr1fvpz5fd0bCauyzlaQNPkX0rAUEzucpQtSY4kqCLRTbuXBICpotYxDUpX75wg6t7zbHBLcKYW4RtPfZhwEjgfIg2ceyFkjxq5LZ3SYM/MtmrOaQJHsN0ijH6gaLMC1t8qWz4j0P6QUD57hdneAzPM3V2QRhKD/bUpXCbJEjHgakr6lIjL5dtdw8VLQuPvIi5',
}

json_data = {
    'username': '1',
    'password': 'g4O+fM9OXDjGwf2X9+qNVt7VUzHW/HoyoC6bOrjUkT/Dhu+Ox9rOeMgES6SExMXxbkOBvdh7b8BuctWHD7uDDz3Zlbg1ff5nHVKdaaJ0/Bp+goESxrLK8utPPj1UuGl70o3Vqb+zvxNKFPhUWecvVDP7Hpp8x6tZPx9KlSdCSqINqTGvsLrokfzaetM5SIbAO7n9FJ2ZW04bz9KEUUuVCWQzsgUXEPn9wemc++CFPpi1P8VapbDPErdWpfy/AuL1PHtlFlVu/DEOSuzHNp5KDXPogvFHxeXfXVBSmnJ3xag+Aw4YK7nnNbjw0K21r76axmNu0mu2uupFCsAH1U/sMg==',
    'captchaVerification': 'HdhyOTchfE3v2mxvmVWGmla/11QSmE16WvaNQPMaG89HimMcf9+RmEIfMb2arGC2fO2Bce6lPNLUGb99GaLpjQ==',
}

response = requests.post(
    'https://synconhub.coscoshipping.com/api/auth/sch/authorization/client/login',
    params=params,
    cookies=cookies,
    headers=headers,
    json=json_data,
)

print(response.text)