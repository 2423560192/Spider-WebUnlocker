"""
https://qiye.qizhidao.com/lib/sc2eacfae297225dbba2cb5da30da2be6a/page-11/
爬取企业名录
"""

import asyncio

from utils.sql_table import init_mysql, create_database_and_table
from utils.extend import login, get_company_info, save_base_info


def loadConf():
    import configparser

    config = configparser.RawConfigParser()
    with open('utils/conf.ini', 'r', encoding='utf-8') as f:
        config.read_file(f)

    return config


async def main(username, password, url):
    page = await login(username, password)  # 登录并获取页面对象

    for i in range(1, 1001):
        print(f"抓取页数 {i}")
        new_url = url + f'/page-{i}/'
        print(new_url)
        company_info = await get_company_info(new_url, page)

        # 保存信息

        # print(company_info)
        save_base_info(conn, company_info)

        await asyncio.sleep(1)  # 模拟用户等待，避免过快请求
        # break
    # 退出前关闭浏览器
    await page.browser.close()


if __name__ == '__main__':
    # 加载配置文件
    config = loadConf()
    # 初始化数据库
    conn, cursor = init_mysql(config)
    # 创建公司名录表
    create_database_and_table(conn, cursor)

    # 发送信息
    token = config['INFO']['token']
    username = config['INFO']['username'].split(',')
    password = config['INFO']['password'].split(',')


    usr_len = len(username) - 1
    now = 0
    # 获取连接
    urls = open('utils/urls.txt', 'r', encoding='utf-8').readlines()
    print(urls)

    # 输入要爬取的链接
    # pg = int(input('请输入爬取页数：'))
    for url in urls:
        if now > usr_len:
            now = 0

        uname = username[now]
        pwd = password[now]

        print('当前账户密码：' , uname , pwd)
        new_url = url.strip('\n')
        print('当前链接： ', new_url)
        # 开始
        asyncio.run(main(uname, pwd, new_url))

        now += 1
