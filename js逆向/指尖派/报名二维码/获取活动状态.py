import requests

# 请求参数
params = {
    "type": 2,
    "activityId": "11550"
}

headers = {
    'Host': 'h5.wmzjp.com',
    'accept': 'application/json, text/plain, */*',
    'xweb_xhr': '1',
    'authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdXRoIjp7InBhc3N3b3JkIjpudWxsLCJ1c2VybmFtZSI6InpqcDEwMDEwMDAwOTc2NDQiLCJhdXRob3JpdGllcyI6W10sImFjY291bnROb25FeHBpcmVkIjp0cnVlLCJhY2NvdW50Tm9uTG9ja2VkIjp0cnVlLCJjcmVkZW50aWFsc05vbkV4cGlyZWQiOnRydWUsImVuYWJsZWQiOnRydWUsInVzZXJJZCI6MTAwMTAwMDA5NzY0NCwib3BlbklkIjoib0ZPODI2U293V1hTZ0tMb0FEc3lXYUtkMzlpcyIsInNjaG9vbElkIjo1LCJiaW5kZWQiOjB9LCJqdGkiOiJiODI3ZTJiOC05Y2QxLTRlZmMtYmRlOC1hNDE5NTFiZmIwNWIiLCJpYXQiOjE3NDQ3NjkxOTQsImV4cCI6MTc0NTM3Mzk5NH0.8PgQ0RbtpCL0iVi4K2zAJhz8RGUT4DmbWLr4C8nVgQQ',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c33)XWEB/11581',
    'Content-type': 'application/json;charset=UTF-8',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://servicewechat.com/wxbd5a45d082ccacaa/34/page-frame.html',
    'accept-language': 'zh-CN,zh;q=0.9',
}

# 请求地址
url = "https://h5.wmzjp.com/act-activity-applicants/beforeSiteOnRegistration"

# 发起 GET 请求
response = requests.get(url, params=params, headers=headers)

# 打印响应内容
if response.status_code == 200:
    print("✅ 请求成功")
    print("响应数据:", response.json())
else:
    print("❌ 请求失败")
    print("状态码:", response.status_code)
    print("响应内容:", response.text)
