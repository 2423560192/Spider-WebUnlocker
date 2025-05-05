import json
import random
import time
import get_questions

import requests
from jsonpath_ng import parse
from utils import get_sid_sign, save_to_json


def get_resp():
    import requests

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'origin': 'https://wx.233.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://wx.233.com/center/study/tiku/chapter?domain=zaojia&subjectId=40',
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sid': 'ucpage202503171341483965368809',
        'sign': 'B8FE0E5FE8E56674C80F80DB0688DC09',
        'token': 'eyJhbGciOiJIUzI1NiJ9.eyJkZXZpY2VUeXBlIjoi5pyq55-l57G75Z6LIiwic3ViIjoiNjUwNjAzMjQiLCJ1bmlvbklkIjoiMDAwMDAxIiwiYm9zc05hbWUiOiIiLCJpc1N0YWZmIjowLCJyb2xlQ29kZXMiOm51bGwsInVzZXJOYW1lIjoicXFfMTFkMXgxIiwidXNlcklkIjoiNjUwNjAzMjQiLCJoZWFkUGljIjoiaHR0cDovL3RoaXJkcXEucWxvZ28uY24vZWtfcXFhcHAvQVFGcGNoc0JTUE9vdThqUDd5cDZKajRGY09uaWJVOWY3a2NGeHhTTXY4Sk51VHU3SjhiWkw4QnRJajJJNjNzVEpLUVpCNmFtSzVpY0t2bEt2TExZYW5LbENTc3VOMHhZeW1ZY0I5ZE9VZ3NEaHJGeFhndTIyemhzMzVmaWIyaHlRLzAiLCJkZXZpY2VOYW1lIjoi572R5qChUEPnvZHpobUiLCJwbGF0Zm9ybSI6MSwicm9sZUlkcyI6WzFdLCJuaWNrbmFtZSI6IuiKnCIsInVzZXJUeXBlIjoxLCJleHAiOjE3NDU3MTYzMTEsImlhdCI6MTc0NDg1MjMxMSwianRpIjoiYmVlNDZiNjItMjUxNi00ZGQ1LWEyMmUtYzNkMDY3Zjk2MjFiIn0.Ia9mNRWklx8la_nYWG-2qaEP0lZKiqx-yKrDtbSpwyo',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    }

    params = {
        'chapterType': '1',
        'isApplet': '0',
        'subjectId': '40',
    }

    response = requests.get('https://japi.233.com/ess-tiku-api/front/chapter/do/init', params=params, headers=headers)

    return response.json()


def parse_data(data):
    try:
        jsonpath_expr = parse('$.data.chapterInfoFrontRspList[*].childList[*]')

        matches = jsonpath_expr.find(data)
        # 提取字段
        result = [
            {
                "domain": match.value.get("domain"),
                "id": match.value.get("id"),
                "subjectId": match.value.get("subjectId"),
                "name": match.value.get("name")
            }
            for match in matches
        ]
        return result


    except Exception as e:
        print(f"Error: {str(e)}")


def get_zt(parm):
    domain = parm['domain']
    id = parm['id']
    subjectId = parm['subjectId']
    name = parm['name']
    print('正在爬：', name, id)
    json_data = {
        "client": 1,
        "mode": 1,
        "domain": domain,
        "subjectId": subjectId,
        "objectId": id,
        "type": 3,
        "attachType": 1
    }

    sid, sign = get_sid_sign('post', json_data, is_form_data=False)

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://wx.233.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://wx.233.com/center/study/tiku/chapter?domain=zaojia&subjectId=40',
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sid': sid,
        'sign': sign,
        'token': 'eyJhbGciOiJIUzI1NiJ9.eyJkZXZpY2VUeXBlIjoi5pyq55-l57G75Z6LIiwic3ViIjoiNjUwNjAzMjQiLCJ1bmlvbklkIjoiMDAwMDAxIiwiYm9zc05hbWUiOiIiLCJpc1N0YWZmIjowLCJyb2xlQ29kZXMiOm51bGwsInVzZXJOYW1lIjoicXFfMTFkMXgxIiwidXNlcklkIjoiNjUwNjAzMjQiLCJoZWFkUGljIjoiaHR0cDovL3RoaXJkcXEucWxvZ28uY24vZWtfcXFhcHAvQVFGcGNoc0JTUE9vdThqUDd5cDZKajRGY09uaWJVOWY3a2NGeHhTTXY4Sk51VHU3SjhiWkw4QnRJajJJNjNzVEpLUVpCNmFtSzVpY0t2bEt2TExZYW5LbENTc3VOMHhZeW1ZY0I5ZE9VZ3NEaHJGeFhndTIyemhzMzVmaWIyaHlRLzAiLCJkZXZpY2VOYW1lIjoi572R5qChUEPnvZHpobUiLCJwbGF0Zm9ybSI6MSwicm9sZUlkcyI6WzFdLCJuaWNrbmFtZSI6IuiKnCIsInVzZXJUeXBlIjoxLCJleHAiOjE3NDU3MTYzMTEsImlhdCI6MTc0NDg1MjMxMSwianRpIjoiYmVlNDZiNjItMjUxNi00ZGQ1LWEyMmUtYzNkMDY3Zjk2MjFiIn0.Ia9mNRWklx8la_nYWG-2qaEP0lZKiqx-yKrDtbSpwyo',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    }

    url = "https://japi.233.com/ess-tiku-api/front/extract/questions"

    data = json.dumps(json_data, separators=(',', ':'))

    response = requests.post(url, headers=headers, data=data)
    return response.json()['data']['ztNo']


if __name__ == '__main__':
    data = get_resp()
    # 获取数据
    res = parse_data(data)
    print(res)
    # 遍历获取zt
    q_res = []
    for i in res:
        zt = get_zt(i)
        print(zt)
        # # 爬取题库
        questions = get_questions.main(zt)
        q_res.extend(questions)
        time.sleep(random.randint(1 , 3))
    # 保存
    save_to_json(q_res)

    with open('questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
        print(f"📦 文件 questions.json 中共保存了 {len(questions)} 道题目")
