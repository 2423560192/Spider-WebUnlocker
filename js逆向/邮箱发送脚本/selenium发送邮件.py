import time

from selenium import webdriver  # # 驱动浏览器
from selenium.webdriver.common.by import By  # 选择器
from selenium.webdriver.common.keys import Keys  # 按键
from selenium.webdriver.support.wait import WebDriverWait  # 等待页面加载完毕，寻找某些元素
from selenium.webdriver.support import expected_conditions as EC  ##等待指定标签加载完毕



def get_driver(url):
    driver.get(url)
    time.sleep(10)
    print(driver.page_source)




if __name__ == '__main__':
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    option.add_experimental_option('detach', True)
    driver = webdriver.Chrome(options=option)
    url = 'https://mail.qq.com/'
    get_driver(url)