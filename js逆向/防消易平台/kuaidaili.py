#!/usr/bin/env Python
# -*- coding: utf-8 -*-

import requests


# 隧道域名:端口号

def get_ip():
    tunnel = "i817.kdltps.com:15818"

    # 用户名密码方式
    username = "t13519285360631"
    password = "c758qj88"
    proxies = {
        "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel},
        "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel}
    }
    return proxies

# 白名单方式（需提前设置白名单）
# proxies = {
#     "http": "http://%(proxy)s/" % {"proxy": tunnel},
#     "https": "http://%(proxy)s/" % {"proxy": tunnel}
# }
