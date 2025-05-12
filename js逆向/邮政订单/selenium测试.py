import time

from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By

# option = webdriver.ChromeOptions()
# # option.add_argument('headless')
# option.add_argument("--start-maximized")
#
# # 如报错 chrome-extensions
# option.add_argument("--disable-extensions")
#
#
# # 修改webdriver get属性
# script = '''
# Object.defineProperty(navigator, 'webdriver', {
# get: () => undefined
# })
# '''
#
#
# # 关闭webdriver的一些标志
# option.add_experimental_option('excludeSwitches', ['enable-automation'])
#
#
# option.add_experimental_option('detach', True)
# driver = webdriver.Chrome(options=option)
# driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#     "source": """
#     Object.defineProperty(navigator, 'webdriver', {
#       get: () => false
#     })
#   """
# })
# driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')

driver = Chrome(options=chrome_options)

with open('stealth.min.js') as f:
    js = f.read()

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": js
})


driver.implicitly_wait(20)

driver.get('https://mall.11185.cn/web/myOrder')

driver.find_element(By.XPATH,'//*[@id="username"]').send_keys('17710489140')
driver.find_element(By.XPATH,'//*[@id="password"]').send_keys('20230907lbs')
driver.find_element(By.XPATH,'//*[@id="upwLoginButton"]').click()
driver.find_element(By.XPATH,'//*[@id="uRight"]/li[3]/a').click()
time.sleep(3)
print(driver.page_source)




