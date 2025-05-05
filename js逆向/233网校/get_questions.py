import json

import jsonpath
import requests
from utils import get_sid_sign, decrypt_content


def get_data(data):
    sid ,sign = get_sid_sign('post', data, is_form_data=False)

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": "https://wx.233.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://wx.233.com/",
        "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sid": sid,
        "sign": sign,
        "token": "eyJhbGciOiJIUzI1NiJ9.eyJkZXZpY2VUeXBlIjoi5pyq55-l57G75Z6LIiwic3ViIjoiNjUwNjAzMjQiLCJ1bmlvbklkIjoiMDAwMDAxIiwiYm9zc05hbWUiOiIiLCJpc1N0YWZmIjowLCJyb2xlQ29kZXMiOm51bGwsInVzZXJOYW1lIjoicXFfMTFkMXgxIiwidXNlcklkIjoiNjUwNjAzMjQiLCJoZWFkUGljIjoiaHR0cDovL3RoaXJkcXEucWxvZ28uY24vZWtfcXFhcHAvQVFGcGNoc0JTUE9vdThqUDd5cDZKajRGY09uaWJVOWY3a2NGeHhTTXY4Sk51VHU3SjhiWkw4QnRJajJJNjNzVEpLUVpCNmFtSzVpY0t2bEt2TExZYW5LbENTc3VOMHhZeW1ZY0I5ZE9VZ3NEaHJGeFhndTIyemhzMzVmaWIyaHlRLzAiLCJkZXZpY2VOYW1lIjoi572R5qChUEPnvZHpobUiLCJwbGF0Zm9ybSI6MSwicm9sZUlkcyI6WzFdLCJuaWNrbmFtZSI6IuiKnCIsInVzZXJUeXBlIjoxLCJleHAiOjE3NDU3MTYzMTEsImlhdCI6MTc0NDg1MjMxMSwianRpIjoiYmVlNDZiNjItMjUxNi00ZGQ1LWEyMmUtYzNkMDY3Zjk2MjFiIn0.Ia9mNRWklx8la_nYWG-2qaEP0lZKiqx-yKrDtbSpwyo",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }

    data = json.dumps(data, separators=(',', ':'))

    response = requests.post('https://japi.233.com/ess-tiku-api/front/extract/page', headers=headers, data=data)

    print(response.json())
    return response.json()


# 定义提取题目信息的函数
def extract_questions(data):
    """
    从JSON数据中提取题目信息
    """
    questions = []
    # 解析
    question_list = jsonpath.jsonpath(data, '$.data.extractQuestionDataRspList[*]')

    for q in question_list:
        # 跳过未解锁题目
        if q.get("isFree", 1) == 0:
            continue
        # 解密题干内容
        encrypted_content = q.get('content', '')
        decrypted_content = decrypt_content(encrypted_content) if encrypted_content else "内容不可用"

        # 提取选项信息，使用A, B, C, D等作为选项标识
        options = [
            {
                "选项标识": chr(65 + i),  # 使用A, B, C, D等
                "选项内容": opt["content"],  # 选项内容
                "是否是正确答案": bool(opt["isCorrectAnswer"])
            }
            for i, opt in enumerate(q.get('questionOptionRspList', []))
        ]

        # 提取题目详细信息
        question = {
            "科目名称": data.get('data', {}).get('subjectName', '未知'),  # 科目名称
            "章节名称": q.get('questionChapterRsp', {}).get('chapterName'),  # 章节名称
            "知识点名称": q.get('questionChapterRsp', {}).get('childKnowledgeName'),  # 知识点名称
            "题目名称": decrypted_content,  # 解密后的题干内容
            "选项": options,  # 选项列表
            "正确答案": q.get('correctAnswer'),  # 正确答案
            "解析": q.get('analysis'),  # 解析
            "题目类型": "单选题" if q.get('baseQuestionType') == 1 else "多选题",  # 题目类型
            "分值": q.get('questionRuleModRsp', {}).get('score'),  # 分值
            "正确率": str(q.get('rightRatio')) + '%',  # 正确率
            "做过人数": q.get('doneNum')  # 做过的人数
        }
        questions.append(question)

    return questions





def main(ztNo):
    data = {
        "pageSize": 500,
        "pageNo": 1,
        "ztNo": ztNo,
        "isCustomizedPage": 0,
        "e": 1
    }

    data = get_data(data)

    # 获取数据
    questions = extract_questions(data)

    # 打印第一个题目作为示例
    print(json.dumps(questions[0], ensure_ascii=False, indent=2))
    return questions