import requests
import time
from datetime import datetime
import json
import sys


def request_sign_button(activity_id, headers):
    url = f'https://h5.wmzjp.com/act-activity-sign-button/getSignButtonByActivityId?activityId={activity_id}'
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ 请求失败，状态码: {response.status_code}")
            return None
    except Exception as e:
        print(f"⚠️ 请求异常: {e}")
        return None


def main():
    activity_id = 15217

    headers = {
        'Host': 'h5.wmzjp.com',
        'accept': 'application/json, text/plain, */*',
        'xweb_xhr': '1',
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdXRoIjp7InBhc3N3b3JkIjpudWxsLCJ1c2VybmFtZSI6InpqcDEwMDEwMDAwNTMxMjciLCJhdXRob3JpdGllcyI6W10sImFjY291bnROb25FeHBpcmVkIjp0cnVlLCJhY2NvdW50Tm9uTG9ja2VkIjp0cnVlLCJjcmVkZW50aWFsc05vbkV4cGlyZWQiOnRydWUsImVuYWJsZWQiOnRydWUsInVzZXJJZCI6MTAwMTAwMDA1MzEyNywib3BlbklkIjoib0ZPODI2U2lSRjlCbE5KVXo3bWxoMWptaE8wYyIsInNjaG9vbElkIjo2LCJiaW5kZWQiOjB9LCJqdGkiOiI4NjE2YTViOS1mNDkwLTRmZjgtOTBkMC1lN2Q3OTBiZDE4ZTkiLCJpYXQiOjE3NDQxNzQ0NTYsImV4cCI6MTc0NDc3OTI1Nn0.y4r1sUZkylduCdWL2rXgDnLJj8M4LIpn08M8W5388ww',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c33)XWEB/11581',
        'Content-type': 'application/json;charset=UTF-8',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://servicewechat.com/wxbd5a45d082ccacaa/34/page-frame.html',
        'accept-language': 'zh-CN,zh;q=0.9',
    }

    last_response_text = None

    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now}] 正在请求接口...")

        data = request_sign_button(activity_id, headers)
        if data is None:
            print("🚫 请求失败，5分钟后重试。\n")
            time.sleep(300)
            continue

        try:
            current_response_text = json.dumps(data, sort_keys=True, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ JSON 序列化失败: {e}")
            time.sleep(300)
            continue

        try:
            print(current_response_text.encode('utf-8').decode('utf-8'))
        except UnicodeEncodeError:
            print("⚠️ 控制台不支持中文输出，尝试转义方式输出：")
            print(current_response_text.encode('utf-8', errors='replace').decode('utf-8'))

        if last_response_text is None:
            last_response_text = current_response_text
            print("✅ 首次请求成功，进入监控中...\n")
        elif current_response_text != last_response_text:
            print("⚠️ 检测到内容变化！接口返回内容已更新！")
            print("🆕 新内容如下：")
            print(current_response_text)
            print("🛑 程序已停止。")
            break
        else:
            print("✅ 内容未变，5分钟后再次检查。\n")

        time.sleep(300)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 用户手动终止程序。")
        sys.exit(0)
