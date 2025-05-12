import json

from selenium import webdriver
from selenium.webdriver.common.by import By  # 选择器
import time
import random
from openpyxl import workbook

if __name__ == '__main__':
    word = '123'
    # TODO 1、创建浏览器
    driver = webdriver.Chrome()
    # # TODO 2、修改了浏览器的内部属性，跳过了登录的滑动验证
    # driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
    #                        {"source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""})
    # TODO 3、执行浏览器操作
    driver.get('https://www.taobao.com/')
    driver.implicitly_wait(10)  # 智能化等待方法
    driver.maximize_window()  # 最大化

    driver.find_element(By.XPATH, '//*[@id="q"]').send_keys(word)
    time.sleep(random.randint(1, 3))
    driver.find_element(By.XPATH, '//*[@id="J_TSearchForm"]/div[1]/button').click()
    try:
        driver.find_element(By.XPATH, '//*[@id="login"]/div[1]/i').click()
    except:
        pass
    time.sleep(20)
    """用户账号及密码登录"""
    # 获取cookie值
    with open("cookies.txt", 'w') as f:
        f.write(json.dumps(driver.get_cookies()))
