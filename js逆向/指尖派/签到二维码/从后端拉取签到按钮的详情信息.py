import requests


def get_sign_button_details(sign_id, activity_id):
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
    # 构造请求参数
    params = {
        'signId': sign_id,
        'activityId': activity_id
    }

    # 添加检查参数（此部分需要根据实际情况进行处理）
    # 假设 addCheckParams 是某种用于处理请求参数的函数
    # 可以直接将 params 传入，或者加入其他校验逻辑
    # params = add_check_params(params)

    url = "https://h5.wmzjp.com/act-activity-sign-button/getSignButtonDetails"

    # 发送 GET 请求
    response = requests.get(url, params=params, headers=headers)

    # 处理响应
    if response.status_code == 200:
        return response.json()  # 返回 JSON 数据
    else:
        return f"Error: {response.status_code}"


# 示例调用
sign_id = 11550  # 替换为实际的 signId
activity_id = 11550  # 替换为实际的 activityId
details = get_sign_button_details(sign_id, activity_id)
print(details)
