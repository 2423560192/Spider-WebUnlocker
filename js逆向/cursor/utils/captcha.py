import requests
import time
import json

CLIENT_KEY = "cf823a34eaea4cd8bb67584c8dd7aeb2764679"
WEBSITE_URL = "https://authenticator.cursor.sh"
WEBSITE_KEY = "0x4AAAAAAAMNIvC45A4Wjjln"  # Cursor 使用的 Turnstile sitekey（这个 key 是公开可抓包得到的）


def get_turnstile_token():
    create_payload = {
        "clientKey": CLIENT_KEY,
        "task": {
            "type": "CloudFlareTurnstileTask",
            "websiteURL": WEBSITE_URL,
            "websiteKey": WEBSITE_KEY,
            "rqData": {
                "mode": "",
                "metadataAction": "-sign-up-password",
                "metadataCdata": ""
            }
        }
    }
    resp = requests.post("https://api.ez-captcha.com/createTask", json=create_payload)
    task_id = resp.json()["taskId"]
    print("创建任务成功，task_id:", task_id)

    # 等待识别完成
    for _ in range(30):
        time.sleep(3)
        result_payload = {
            "clientKey": CLIENT_KEY,
            "taskId": task_id
        }
        result = requests.post("https://api.ez-captcha.com/getTaskResult", json=result_payload)
        result_json = result.json()
        print(result_json)
        if result_json.get("status") == "ready":
            token = result_json["solution"]["token"]
            print("获取token成功：", token)
            return token
        elif result_json.get("status") == "processing":
            print("识别中...")
        else:
            raise Exception("识别失败：" + result.text)
    raise TimeoutError("识别超时")

# get_turnstile_token()
