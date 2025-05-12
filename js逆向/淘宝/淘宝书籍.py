import time

from selenium import webdriver  # # 驱动浏览器
from selenium.webdriver.common.by import By  # 选择器
from selenium.webdriver.common.keys import Keys  # 按键
from selenium.webdriver.support.wait import WebDriverWait  # 等待页面加载完毕，寻找某些元素
from selenium.webdriver.support import expected_conditions as EC  ##等待指定标签加载完毕


def get_data(url):
    driver.get(url)
    # # 模拟登录
    driver.find_element(By.XPATH,'//*[@id="J_SiteNavLogin"]/div[1]/div[1]/a[1]').click()
    driver.find_element(By.XPATH,'//*[@id="login-form"]/div[5]/a[2]').click()
    time.sleep(20)
    # 输入关键字
    driver.find_element(By.XPATH,'//*[@id="q"]').send_keys('三国演义')
    driver.find_element(By.XPATH,'//*[@id="J_TSearchForm"]/div[1]/button').click()
    time.sleep(1)
    print(driver.page_source)
    with open('淘宝.txt','w',encoding='utf-8') as f:
        f.write(driver.page_source)

def parse_data():
    pass

if __name__ == '__main__':
    url = 'https://www.taobao.com/?spm=a2e0b.20350158.1581860521.1.15bf468aW4uC7l&pid=mm_26632258_3504122_32538762&union_lens=recoveryid%3A201_33.8.53.32_26949837_1685846243829%3Bprepvid%3A201_33.8.53.32_26949837_1685846243829&clk1=8b69cea7638192a146019a331e25e561'
    option = webdriver.ChromeOptions()
    # option.add_argument('headless')
    option.add_experimental_option('detach', True)
    driver = webdriver.Chrome(options=option)
    get_data(url)