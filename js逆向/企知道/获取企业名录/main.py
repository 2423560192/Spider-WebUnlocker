"""
https://qiye.qizhidao.com/lib/sc2eacfae297225dbba2cb5da30da2be6a/page-11/
高级筛选企业
爬取基础信息和补贴信息
"""
import atexit
import random
import sys
import time
import traceback
from lxml import etree

import pymysql
import requests
from utils.sql_table import init_mysql, create_database_and_table
from utils.extends import change_ip_cookie, execute_command, send_msg
from utils.companyBase import get_company_base
from utils.handle_info import save_base_info
from utils.auto_login.login import login_now


def loadConf():
    import configparser

    config = configparser.RawConfigParser()
    with open('utils/conf.ini', 'r', encoding='utf-8') as f:
        config.read_file(f)

    return config


if __name__ == '__main__':
    # 加载配置文件
    config = loadConf()
    # 初始化数据库
    conn, cursor = init_mysql(config)
    # 创建公司名录表
    create_database_and_table(conn, cursor)

    # 发送信息
    token = config['INFO']['token']

    # 输入要爬取的链接
    # url = input('请输入爬取链接: ')
    page = int(input('请输入爬取页数：'))

    # end_url = url  # 当前这个地区
    # 自动登录
    session , tokens = login_now()
    # session = requests
    try:
        for i in range(page, 1001):
            try:

                proxy, cookie, ua = change_ip_cookie()

                cookies = session.cookies.get_dict()
                base_info = get_company_base(session, i ,  tokens , proxy , cookies)

                print('基础信息获取完毕: ', base_info)

                # save_base_info(conn , base_info)
                time.sleep(random.randint(1, 5))

            except Exception as e:
                print(e)
                tb = traceback.format_exc()
                print(tb)
                print('当前页数数据爬取异常：', i)
                # execute_command(end_page)
                sys.exit()
    except Exception as e:
        tb = traceback.format_exc()
        print(tb)
        print(f"程序运行时遇到错误: {e}")