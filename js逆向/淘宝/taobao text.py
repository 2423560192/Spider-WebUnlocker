import json

from selenium import webdriver
from selenium.webdriver.common.by import By  # 选择器
import time
import random
from openpyxl import workbook

ws = workbook.Workbook()
wb = ws.active
wb.append(['书名', '店铺', '价格', '链接', '销量'])


def parse_data():
    # print(driver.page_source)
    test = driver.find_elements(By.XPATH, '//div[@class="shop"]/a/span[2]')  # 店铺名
    price = driver.find_elements(By.XPATH, '//div[@class="price g_price g_price-highlight"]/strong')  # 价格
    links = driver.find_elements(By.XPATH, '//a[@class="J_ClickStat"]')  # 链接
    buys = driver.find_elements(By.XPATH, '//div[@class="deal-cnt"]')  # 销量
    lst = []
    for t, p, l, b in zip(test, price, links, buys):
        print(t.text)
        print(p.text)
        print(l.get_attribute('href'))
        print(b.text)
        save_data([word,t.text, p.text, l.get_attribute('href'), b.text])


# 保存函数
def save_data(data):
    wb.append(data)
    ws.save('淘宝-书籍信息.xlsx')


if __name__ == '__main__':
    word = input('请输入要搜索的关键字：')
    # TODO 1、创建浏览器
    driver = webdriver.Chrome()
    # # TODO 2、修改了浏览器的内部属性，跳过了登录的滑动验证
    # driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
    #                        {"source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""})
    # TODO 3、执行浏览器操作
    driver.get('https://www.taobao.com/')
    driver.implicitly_wait(10)  # 智能化等待方法
    # 获取cookie值
    # with open("cookies.txt", 'r') as f:
    #     cookie_list = json.load(f)
    #     for cookie in cookie_list:
    #         print(cookie)
    #         if isinstance(cookie.get('expiry'), float):
    #             cookie['expiry'] = int(cookie['expiry'])
    #         driver.add_cookie(cookie)
    # driver.get('https://www.taobao.com/')
    # driver.refresh()

    driver.find_element(By.XPATH, '//*[@id="q"]').send_keys(word)
    time.sleep(random.randint(1, 3))
    driver.find_element(By.XPATH, '//*[@id="J_TSearchForm"]/div[1]/button').click()
    try:
        driver.find_element(By.XPATH, '//*[@id="login"]/div[1]/i').click()
    except:
        pass

    time.sleep(10)
    for page in range(0, 20):
        print(f'-----------------正在爬取第{page + 1}页-----------------')
        # TODO 调用商品解析的函数
        parse_data()
        driver.find_element(By.XPATH, '//li[@class="item next"]/a[@class="J_Ajax num icon-tag"]').click()
        time.sleep(random.randint(2, 3))
