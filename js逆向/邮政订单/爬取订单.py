"""
2023-09-06
https://mall.11185.cn/web/myOrder
by: 小廉
"""

import requests
import time
from jsonpath import jsonpath

import requests

url = "https://ord.11185.cn/ZxptRestOrdWEB/ordCommon/listOrderTimeCondition"

payload = ""
headers = {
  'Content-Type': 'application/json;charset=UTF-8',
  'Cookie': 'Hm_lvt_998c186922e9ba78bef6811cb0496a8a=1693967994,1694095636; Hm_lpvt_998c186922e9ba78bef6811cb0496a8a=1694096491; SERVERID=fb1f218c4795902c1d09649e05963857|1694096501|1694095663; wLsBD3ExEc9TO=575NfP3nHgtPByP7a.I7ZVpSWlm_oA0hctPEeZOzN0JpyrLUtblINhmdRGQwTU0IA6NfsLgtqldwYTRyFRT.alA',
  'Origin': 'https://mall.11185.cn',
  'Referer': 'https://mall.11185.cn/',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
  'requestId': '735bfcf8-0067-0d31-1a17-e0cab719bc9c',
  'token': '893126ce865446e8a83a5b24ab0eb49a8dbcf3cab6840435cdfe93aa10239eacecdc'
}

response = requests.request("get", url, headers=headers, data=payload)

print(response.text)
print(response.url)


