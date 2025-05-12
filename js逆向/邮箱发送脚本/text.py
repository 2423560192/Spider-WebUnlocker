from telnetlib import EC

from time import sleep
from selenium import webdriver  # # 驱动浏览器
from selenium.webdriver.common.by import By  # 选择器
from selenium.webdriver.common.keys import Keys  # 按键
from selenium.webdriver.support.wait import WebDriverWait  # 等待页面加载完毕，寻找某些元素
from selenium.webdriver.support import expected_conditions as EC  ##等待指定标签加载完毕


def get_driver(url):
    driver.get('https://mail.qq.com/')

    sleep(5)

    # 定位账号、密码，并输入

    driver.find_element(By.XPATH, '//*[@id="composebtn"]').click()

    # 切换到mainFrame

    driver.switch_to.frame('mainFrame')

    sleep(1)

    # 定位收件人，并输入

    driver.find_element(By.XPATH, "//*[@id='toAreaCtrl']/div[2]/input").send_keys("2480419172@qq.com")

    # 定位主题，并输入

    driver.find_element(By.XPATH, '//*[@id="subject"]').send_keys(" from lucas")

    # 定位邮件正文，先进入到iframe

    driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@class="qmEditorIfrmEditArea"]'))

    # 必须先点击正文，再send_keys

    driver.find_element(By.XPATH, '/html/body').click()

    driver.find_element(By.XPATH, '/html/body').send_keys("Hello World", "\nlucas")

    # 返回到mainframe

    driver.switch_to.parent_frame()

    # 定位发送按钮

    driver.find_element(By.XPATH, '//*[@name="sendbtn"]').click()

    sleep(5)


if __name__ == '__main__':
    option = webdriver.ChromeOptions()
    # option.add_argument('headless')
    option.add_experimental_option('detach', True)
    driver = webdriver.Chrome(options=option)
