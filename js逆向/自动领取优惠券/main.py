# -*- coding: utf8 -*-
import threading

from wchat_tool import Wchat
from receive import send_jd
import requests, re
from datetime import datetime


def date_difference(target_date_str):
    current_date_str = datetime.now().strftime('%Y-%m-%d')
    current_date = datetime.strptime(current_date_str, '%Y-%m-%d')
    target_date = datetime.strptime(target_date_str, '%Y-%m-%d')
    difference = (current_date - target_date).days
    return difference


def send_msg(token, msg, phone,msg2 ,  date):
    params = {
        'title':'领券通知',
        'content':f"{msg}\n  \n{phone} {msg2}  还剩{date}天",
    }
    requests.get(f'https://xizhi.qqoq.net/{token}.send', params=params)


def Read_txt():
    with open('配置文件.txt', 'r', encoding='utf-8') as (file):
        f = file.read()
    f = f.strip()
    f_list = f.split('\n')

    data_list = []
    for x in f_list:
        if not x:
            pass
        else:
            data_list.append(x.split('---'))
    else:
        return data_list

def parse_cookies(cookie_str):
    cookies = []
    for item in cookie_str.split('; '):
        try:
            name, value = item.split('=', 1)
            cookies.append({
                'name': name,
                'value': value,
                'domain': '.jd.com',  # 京东域名
                'path': '/',
            })
        except ValueError:
            print(f"忽略无效的 Cookie 项目: {item}")
    return cookies

def Start(url, msg):

    for date, phone, token, ck in data_list:
        ck = parse_cookies(ck)
        sub_date = date_difference(date)
        if sub_date > 0:
            print(phone, '使用期限已到')
            return None
        try:
            send = send_jd(ck, url)
            send_msg(token=token, msg=msg, phone=phone,msg2 = send ,  date=sub_date)
        except Exception:
            pass

if __name__ == '__main__':
    data_list = Read_txt()
    wchat = Wchat()

    # 启动后台线程来监听消息
    threading.Thread(target=wchat.listen_msg, daemon=True).start()

    # 外部循环，获取消息
    while True:
        msg = wchat.get_msg()  # 从队列中获取消息
        print(f"[{msg['ActualNickName']}] {msg['Content']}")  # 打印消息内容
        msg_content = msg['Content']

        # 链接
        links = re.findall('http.*', msg_content)
        for url in links:
            print('url：' , url)
            bl1 = 'linkKey' not in url
            bl2 = 'key' not in url
            bl3 = 'u.jd' not in url
            if bl1 and bl2 and bl3:
                pass
            else:
                Start(url, msg_content)
