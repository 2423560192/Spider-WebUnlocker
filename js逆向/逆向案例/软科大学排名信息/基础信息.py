import time

import requests

from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By

from openpyxl import workbook

# 获取学校基础信息
def get_data(url):
    # html_data = driver.get(url)
    resp = driver.page_source
    # print(html_data)
    # print(resp)
    lxml = etree.HTML(resp)
    all_scool = lxml.xpath('//div[@class="rk-table-box"]//table[@class="rk-table"]//tr')
    for i in all_scool[1:]:
        info = []
        rank = i.xpath('.//td[1]/div/text()')
        name = i.xpath('.//td[2]//a[@class="name-cn"]/text()')
        en_name = i.xpath('.//td[2]//a[@class="name-en"]/text()')
        prevence = i.xpath('.//td[3]/text()')
        category = i.xpath('.//td[4]/text()')
        all_sum = i.xpath('.//td[5]/text()')
        place = i.xpath('.//td[2]//p[@class="tags"]/text()')
        try:
            place = place[0].split('/')
        except:
            place = []

        try:
            info.append(rank[0].strip())
            info.append(name[0].strip())
            info.append(en_name[0].strip())
            info.append(prevence[0].strip())
            info.append(category[0].strip())
            info.append(all_sum[0].strip())
            if '双一流' in place:
                info.append('true')
            else:
                info.append('false')
            if '985' in place:
                info.append('true')
            else:
                info.append('false')
            if '211' in place:
                info.append('true')
            else:
                info.append('false')
        except:
            pass
        print(info)
        save_data(info)
    try:
        driver.find_element(By.XPATH, '//*[@id="content-box"]/ul//li//i[@class="anticon anticon-right"]').click()


        time.sleep(2)
        get_data(url)
    except Exception as e:
        print(e)
        print('已爬取完毕')
        return 0

def save_data(info):
    wb.append(info)
    ws.save('软科大学排名基础信息.csv')


if __name__ == '__main__':
    option = webdriver.ChromeOptions()
    # option.add_argument('headless')
    option.add_experimental_option('detach', True)
    driver = webdriver.Chrome(options=option)
    ws = workbook.Workbook()
    wb = ws.active
    wb.append(['排名', '名称', '英文名称', '省市', '类型', '总分', '双一流', '985', '211'])
    ws.save('软科大学排名基础信息.csv')
    url = 'https://www.shanghairanking.cn/rankings/bcur/202311'
    driver.get(url)
    get_data(url)
