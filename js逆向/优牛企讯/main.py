import json

import execjs



import requests

cookies = {
    'Hm_lvt_09314a434d0e1a54e3fbc904fe7009aa': '1732676698',
    'HMACCOUNT': '74E03469813A9187',
    'ynqx_log_tk': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo4MTg1LCJ1c2VybmFtZSI6IjEzMDA4MzIyNjIwIiwiZXhwIjoxNzMyNzYzMjkwLCJlbWFpbCI6IiJ9.ttHs62SWwARxy1r31_msKuRNx0-nGfp0FuZpZW_c2qA',
    'Hm_lpvt_09314a434d0e1a54e3fbc904fe7009aa': '1732676891',
    '_clck': 'lsoiu4%7C2%7Cfr8%7C0%7C1792',
    '_clsk': 'j65t0z%7C1732676892630%7C1%7C1%7Cl.clarity.ms%2Fcollect',
    '_uetsid': '6303f960ac6c11efa55039915017b821',
    '_uetvid': '6303f860ac6c11efa4f273bdd4a0eeb6',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo4MTg1LCJ1c2VybmFtZSI6IjEzMDA4MzIyNjIwIiwiZXhwIjoxNzMyNzYzMjkwLCJlbWFpbCI6IiJ9.ttHs62SWwARxy1r31_msKuRNx0-nGfp0FuZpZW_c2qA',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    # 'Cookie': 'Hm_lvt_09314a434d0e1a54e3fbc904fe7009aa=1732676698; HMACCOUNT=74E03469813A9187; ynqx_log_tk=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo4MTg1LCJ1c2VybmFtZSI6IjEzMDA4MzIyNjIwIiwiZXhwIjoxNzMyNzYzMjkwLCJlbWFpbCI6IiJ9.ttHs62SWwARxy1r31_msKuRNx0-nGfp0FuZpZW_c2qA; Hm_lpvt_09314a434d0e1a54e3fbc904fe7009aa=1732676891; _clck=lsoiu4%7C2%7Cfr8%7C0%7C1792; _clsk=j65t0z%7C1732676892630%7C1%7C1%7Cl.clarity.ms%2Fcollect; _uetsid=6303f960ac6c11efa55039915017b821; _uetvid=6303f860ac6c11efa4f273bdd4a0eeb6',
    'Origin': 'https://youniudata.com',
    'Referer': 'https://youniudata.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    't': '624613895288d03253f74f5a9963a3a2',
}



json_data = {
    'regions': [
        '430100',
    ],
    'page_index': '1',
    'page_size': '20',
}

json_d = json.dumps(json_data)

sign = execjs.compile(open('loader.js' , 'r').read()).call('get_sign' , json_d)['time']

print(sign)
params = {
    'sign': sign,
}

response = requests.post(
    'https://youniudata.com/api/report_api/get_company_search/',
    params=params,
    # cookies=cookies,
    headers=headers,
    json=json_data,
)
response.encoding = 'utf-8'
print(response.json())