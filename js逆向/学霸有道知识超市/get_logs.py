import os
import re
import time
from urllib.parse import urlparse, parse_qs

import requests

from utils.jiemi import decrypt
from jsonpath import jsonpath

from js逆向.学霸有道知识超市 import extract_words, get_text, word_detail_fetcher, crawler


def get_resp_data():
    headers = {
        'Host': 'api.shansiweilai.com',
        'Scope': 'com.dy.wordrecite.wx',
        'xweb_xhr': '1',
        'Authorization': '7866f46214a7d8103df4b1715bbec2840c5eece513db53baedfa325cd33b0225',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c33)XWEB/11581',
        'Content-type': 'application/json;charset=UTF-8',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://servicewechat.com/wx04555c1935d6e836/66/page-frame.html',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    json_data = {
        'op_path': 'wordrecite.chapter.getcoursedetailinfo',
        'business_id': 104,
        'course_id': 18296,
    }

    response = requests.post(
        'https://api.shansiweilai.com/api/wordrecite/chapter/getcoursedetailinfo',
        headers=headers,
        json=json_data,
    )

    return response.json()['encrypt_body']


def get_parse_data(data):
    course_name = jsonpath(data, '$.data..course_name')[0]
    names = jsonpath(data, '$.data..catalog_list..name')
    link_url = jsonpath(data, '$.data..catalog_list..link_url')
    catalog_files = jsonpath(data, '$.data..catalog_list..catalog_files')
    path = os.path.join('故事', course_name)
    i = 0
    for name, file, link in zip(names, catalog_files, link_url):
        print('当前：', i)
        i += 1
        # 解析 URL
        parsed_url = urlparse(link)

        # 提取查询参数
        query_params = parse_qs(parsed_url.query)

        # 获取 note_id 的值
        note_id = query_params.get('note_id', [None])[0]  # 默认值为 None，如果没有找到
        if not note_id:
            continue
        print(name)
        print(file)
        print(link)
        print(note_id)

        # 新路径
        new_name = re.sub(r'[<>:"/\\|?*]', '-', name)
        new_name = re.sub(r'[！!]', '!', new_name)
        new_name = new_name.replace(' ', '')

        new_path = os.path.join(path, new_name)

        if not os.path.exists(new_path):
            os.makedirs(new_path)

        crawler.main(new_path, note_id)
        get_text.main(new_path)
        extract_words.main(new_path)
        word_detail_fetcher.main(new_path)
        # break
        # 获取文件
        # for fi in file:
        #     file_url = fi['file_url']
        #     file_name = fi['file_name']
        #     response = requests.get(file_url)
        #     with open(os.path.join(new_path, f'{file_name}.pdf'), 'wb') as f:
        #         f.write(response.content)
        #         print(file_name, '保存成功')
        time.sleep(1)
        print('---------------------')
        # break


def get_data():
    data = get_resp_data()
    data = decrypt(data)
    # print(data)
    # 解析数据
    get_parse_data(data)
