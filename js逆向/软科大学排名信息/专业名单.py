# -*- coding: utf-8 -*-
import time

import requests
import pandas as pd

from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By

from openpyxl import workbook


# 获取学校基础信息
def get_data(url,j):
    html_data = driver.get(url)
    resp = driver.page_source
    # print(html_data)
    # print(resp)
    lxml = etree.HTML(resp)
    all_scool = lxml.xpath('//*[@id="bcmr"]/div[3]/div[1]/div[2]/table/tbody//tr')
    for i in all_scool:
        id = i.xpath('./td[1]/text()')[0]
        name = i.xpath('./td[2]/text()')[0]
        rank = i.xpath('./td[3]/text()')[0]
        quq = i.xpath('./td[4]/text()')[0]
        info = [id, name, rank, quq]
        print(info)
        save_data(info,j)


def save_data(info,j):
    wb.append(info)
    ws.save(f'zhuanye/{j}.csv')


if __name__ == '__main__':
    option = webdriver.ChromeOptions()
    # option.add_argument('headless')
    option.add_experimental_option('detach', True)
    driver = webdriver.Chrome(options=option)
    ws = workbook.Workbook()
    wb = ws.active
    wb.append(['专业代码', '专业名称', '评级', '专业排名'])
    ws.save('软科大学排名专业信息.csv')
    df = pd.read_excel('软科大学排名基础信息.xlsx')
    lst = []
    lst2 = []
    for k, v in df.iterrows():
        s = '-'.join(v['英文名称'].split(' '))
        name = v['名称']
        lst.append(s)
        lst2.append(name)
    print(lst)
    for i,j in zip(lst,lst2):
        url = f'https://www.shanghairanking.cn/institution/{i}'
        get_data(url,j)
