"""
https://qiye.qizhidao.com/lib/sc2eacfae297225dbba2cb5da30da2be6a/page-11/
高级筛选企业
爬取基础信息和补贴信息
"""
import sys
import time
import traceback

from utils.request_company import  get_company_detail_data, get_company_detail_butie
from utils.handle_data import save_base_data, save_butie_data

from utils.sql_table import init_mysql, create_database_and_table
from utils.extends import execute_command, change_ip_cookie, send_msg

from utils.apis.companyId import get_company_id


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
    # 创建表
    create_database_and_table(conn, cursor)
    # 发送信息
    token = config['INFO']['token']
    # 输入要爬取的链接
    url = input('请输入爬取链接: ')
    page = int(input('请输入爬取页数：'))

    end_url = url  # 当前这个地区
    try:
        for i in range(page, 1001):
            print('当前页数: ', i)
            new_url = url + f'/page-{i}/'
            print(new_url)

            try:
                execute_command(new_url)

                proxy , cookie , ua = change_ip_cookie()
                urls = get_company_id(new_url)
                # name = get_company_name(new_url)

                print('urls获取完毕: ' , urls)

                for url_p in urls:
                    print('当前url：' , url_p)
                    base_info = get_company_detail_data(url_p , proxy , cookie , ua)
                    # 保存信息
                    save_base_data(conn, base_info)
                    # 抓取补贴
                    print('正在抓取补贴...')

                    butie_info = get_company_detail_butie(
                        base_info['company_name'], base_info['company_id'] ,  proxy , cookie , ua)
                    save_butie_data(conn, butie_info)
                    print('-------------------------')
                    time.sleep(5)

            except Exception as e:
                print(e)
                tb = traceback.format_exc()
                print(tb)
                print('当前页数数据爬取异常：', i)
                # execute_command(end_page)

                send_msg(new_url, token, '爬取异常')

                sys.exit()
    except Exception as e:
        tb = traceback.format_exc()
        print(tb)
        print(f"程序运行时遇到错误: {e}")


    send_msg(end_url, token, '爬取完毕')