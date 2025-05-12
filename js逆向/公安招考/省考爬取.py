import json
import sys
import time

import requests
from jsonpath import jsonpath
from openpyxl import workbook
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re


def post_ans(id):
    import requests

    url = f"https://tiku.fenbi.com/api/gazj/async/exercises/{id}/submit?app=web&kav=100&av=100&hav=100&version=3.0.0.0"

    payload = 'status=1'
    headers = {
        'authority': 'tiku.fenbi.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': 'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22136617049%22%2C%22first_id%22%3A%2218e17d7eff4751-01c6f8f87c537f-26001b51-2073600-18e17d7eff51011%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%7D%2C%22%24device_id%22%3A%2218e17d7eff4751-01c6f8f87c537f-26001b51-2073600-18e17d7eff51011%22%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMThlMTk2ODkzNjI1NmYtMDAxN2MxYTIwNzI5ZWRlMS0yNjAwMWI1MS0yMDczNjAwLTE4ZTE5Njg5MzYzMTI4MyIsIiRpZGVudGl0eV9sb2dpbl9pZCI6IjEzNjYxNzA0OSJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22136617049%22%7D%7D; acw_tc=0bd17c0a17098807415758440e985c9ca02e409a2058f5cb9333b09f89637a; userid=126763883; sess=9yxmUs7JDsCAzIyJ38en6PL/KehtQH3BvByQyZ04VHQLB34WXoY8quEanGKLPHsrCbEUXNl/lMeRYwHMirDxM3TnrA2raKR5buxPmckSbSw=; sid=3067726; persistent=nXSfN7VAXfX14HR5YCTGc1FRYEqNkv2UNs4KjKX60MbhXJkiPHh+VzMG2qGh4wtMnzuY5B93o26GFVyAkX846A==',
        'origin': 'https://www.fenbi.com',
        'referer': 'https://www.fenbi.com/',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def get_data(id, sheng):
    # 提交答案
    post_ans(id)
    print(sheng, '省份')
    time.sleep(2)
    ws = workbook.Workbook()
    wb = ws.active

    wb.append(['题号', '省份', '材料', '题目正文', '选项', '正确答案', '题目解析'])
    url = f"https://tiku.fenbi.com/api/gazj/universal/auth/solutions?type=0&id={id}&app=web&kav=100&av=100&hav=100&version=3.0.0.0"

    payload = {}
    headers = {
        'authority': 'tiku.fenbi.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22136617049%22%2C%22first_id%22%3A%2218e17d7eff4751-01c6f8f87c537f-26001b51-2073600-18e17d7eff51011%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%7D%2C%22%24device_id%22%3A%2218e17d7eff4751-01c6f8f87c537f-26001b51-2073600-18e17d7eff51011%22%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMThlMTk2ODkzNjI1NmYtMDAxN2MxYTIwNzI5ZWRlMS0yNjAwMWI1MS0yMDczNjAwLTE4ZTE5Njg5MzYzMTI4MyIsIiRpZGVudGl0eV9sb2dpbl9pZCI6IjEzNjYxNzA0OSJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22136617049%22%7D%7D; acw_tc=0bd17c0a17098807415758440e985c9ca02e409a2058f5cb9333b09f89637a; userid=126763883; sess=9yxmUs7JDsCAzIyJ38en6PL/KehtQH3BvByQyZ04VHQLB34WXoY8quEanGKLPHsrCbEUXNl/lMeRYwHMirDxM3TnrA2raKR5buxPmckSbSw=; sid=3067726; persistent=nXSfN7VAXfX14HR5YCTGc1FRYEqNkv2UNs4KjKX60MbhXJkiPHh+VzMG2qGh4wtMnzuY5B93o26GFVyAkX846A==',
        'origin': 'https://www.fenbi.com',
        'referer': 'https://www.fenbi.com/',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    js_data = response.json()
    # print(js_data)
    questions = jsonpath(js_data, '$..solutions..content')
    options = jsonpath(js_data, '$..solutions..options')
    types = jsonpath(js_data, '$..solutions..type')
    print(types)
    typpes = []
    mater_index = jsonpath(js_data, '$..solutions..materialIndexes')
    answers = jsonpath(js_data, '$..solutions..correctAnswer.choice')
    jiexi = jsonpath(js_data, '$..solutions..solution')
    materials = jsonpath(js_data, '$..materials..content')
    for i in types:
        if len(str(i)) < 3:
            typpes.append(i)
    # 预先处理判断题
    for i in typpes:
        if i == 5:
            options.insert(0, ['正确', '错误'])
    all_ques = []
    num = 1
    for ques, op, ans, jie, index, typ in zip(questions, options, answers, jiexi, mater_index, typpes):
        # 判断题
        # if type == '5':
        ques = ques.replace('<p>', '').replace('</p>', '')
        if 'img' in ques:
            img_url = re.findall('src="(.*?)"', ques)[0]

            ques = re.sub('<img(.*?)/>', img_url, ques)
        if 'img' in ans:
            img_url = re.findall('src="(.*?)"', ans)[0]

            ans = re.sub('<img(.*?)/>', img_url, ans)
        if 'img' in jie:
            img_url = re.findall('src="(.*?)"', jie)[0]

            jie = re.sub('<img(.*?)/>', img_url, jie)
            # img_url = re.findall('src="(.*?)"', jie)[0]
            #
            # jie = re.sub('<img(.*?)/>', img_url, jie)

        temp_lst = []
        dic = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        for i, j in enumerate(op, 0):
            if 'img' in j:
                img_url = re.findall('src="(.*?)"', j)[0]

                j = re.sub('<img(.*?)/>', img_url, j)
                temp_lst.append(dic[i] + '、' + j.replace('<p>', '').replace('</p>', '').replace('<br>', '\n'))
            else:
                temp_lst.append(dic[i] + '、' + j.replace('<p>', '').replace('</p>', '').replace('<br>', '\n'))
        op = "\n".join(temp_lst)
        anss = ''
        if len(ans) > 0:
            for j in ans:
                if j == ',':
                    continue
                anss += dic[int(j)] + '\n'
        jie = jie.replace('<p>', '').replace('</p>', '').replace('<br>', '\n')
        # print(ques, op, anss, jie)
        #
        if not index:
            print(op)
            wb.append([sheng, num, '-', ques, op, anss, jie])
        else:
            mater = materials[index[0]].replace('<p>', '').replace('</p>', '').replace('<br>', '\n')
            if 'img' in mater:
                img_url = re.findall('src="(.*?)"', mater)[0]

                mater = re.sub('<img(.*?)/>', img_url, mater)
            wb.append(
                [sheng, num, mater, ques, op, anss,
                 jie])

        ws.save(rf'{sheng[:19]}.xlsx')

        num += 1


def selenium_click():
    url = 'https://www.fenbi.com/spa/tiku/guide/realTest/gazj/gazj'
    option = webdriver.ChromeOptions()
    # option.add_argument('headless')
    option.add_experimental_option('detach', True)
    chorme = webdriver.Chrome(options=option)
    chorme.get(url)
    cookie_list = [{'domain': '.fenbi.com', 'expiry': 1741417484, 'httpOnly': True, 'name': 'persistent', 'path': '/',
                    'sameSite': 'Lax', 'secure': False,
                    'value': 'nXSfN7VAXfX14HR5YCTGc1FRYEqNkv2UNs4KjKX60MbhXJkiPHh+VzMG2qGh4wtMwDJsnJPOcplCsVZ9DC/fpA=='},
                   {'domain': '.fenbi.com', 'expiry': 1741417484, 'httpOnly': True, 'name': 'sid', 'path': '/',
                    'sameSite': 'Lax', 'secure': False, 'value': '3067726'},
                   {'domain': '.fenbi.com', 'httpOnly': True, 'name': 'sess', 'path': '/', 'sameSite': 'Lax',
                    'secure': False,
                    'value': '9yxmUs7JDsCAzIyJ38en6PL/KehtQH3BvByQyZ04VHQLB34WXoY8quEanGKLPHsr2rKqGzHd4DQNUnV348TWbUtzupvEGuKhXGzQGAAlauE='},
                   {'domain': '.fenbi.com', 'httpOnly': True, 'name': 'userid', 'path': '/', 'sameSite': 'Lax',
                    'secure': False, 'value': '126763883'},
                   {'domain': '.fenbi.com', 'expiry': 1744441484, 'httpOnly': False,
                    'name': 'sensorsdata2015jssdkcross', 'path': '/', 'sameSite': 'Lax', 'secure': False,
                    'value': '%7B%22distinct_id%22%3A%2218e1ce005a818ec-0711656723100d-26001b51-2073600-18e1ce005a922f8%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%2218e1ce005a818ec-0711656723100d-26001b51-2073600-18e1ce005a922f8%22%7D'},
                   {'domain': '.fenbi.com', 'expiry': 1709913599, 'httpOnly': False,
                    'name': 'sajssdk_2015_cross_new_user', 'path': '/', 'sameSite': 'Lax', 'secure': False,
                    'value': '1'},
                   {'domain': 'www.fenbi.com', 'expiry': 1709883226, 'httpOnly': True, 'name': 'acw_tc', 'path': '/',
                    'sameSite': 'Lax', 'secure': False,
                    'value': '0bdd34c217098814277611966e7ca73ec3fcd7874930f0dcd52edb492b39f7'}]

    for cookie in cookie_list:
        chorme.add_cookie(cookie)
    # 刷新页面或进行其他操作，以便新的Cookie生效
    chorme.refresh()
    time.sleep(1)
    chorme.find_element(By.XPATH, '//*[@id="qusetion-list"]/main/nav/div[1]/span[3]').click()
    doman = '//*[@id="qusetion-list"]/main/nav/div[3]//span'
    domans = chorme.find_elements(By.XPATH, doman)
    for i in range(8, len(domans)):
        sheng_element = WebDriverWait(chorme, 10).until(EC.element_to_be_clickable((By.XPATH, doman)))
        sheng_element = chorme.find_elements(By.XPATH, doman)[i]
        print(sheng_element.text)
        sheng_element.click()
        time.sleep(2)
        sheng = sheng_element.text
        pages = chorme.find_elements(By.XPATH, '//*[@id="qusetion-list"]/main/div[2]//div[@class="paper-item"]')

        # 该页面所有的考试
        le = len(pages)
        ll = 0
        while ll < le:
            WebDriverWait(chorme, 10).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="qusetion-list"]/main/div[2]//div[@class="paper-item"]')))

            pages = chorme.find_elements(By.XPATH, '//*[@id="qusetion-list"]/main/div[2]//div[@class="paper-item"]')
            name = pages[ll].text
            pages[ll].click()
            # 开始交卷
            time.sleep(1)
            id = chorme.current_url.split('/')[-2]
            get_data(id, f'{name}')
            # time.sleep(2)
            chorme.find_element(By.XPATH,
                                '//*[@id="app-practice"]/header/app-simple-nav-header/header/div/button').click()
            ll += 1


selenium_click()
# get_data('1835176766', 'diaomao')
