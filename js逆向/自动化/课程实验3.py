from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from openpyxl import Workbook
from openpyxl import load_workbook
import os

# 初始化浏览器
driver = webdriver.Chrome()
driver.get("https://www.saucedemo.com/")
username = 'standard_user'
password = 'secret_sauce'
# 登录
driver.find_element(By.XPATH, '//*[@id="user-name"]').send_keys(username)
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(password)
driver.find_element(By.XPATH, '//*[@id="login-button"]').click()

# 购物

shops = driver.find_elements(By.XPATH, '//*[@id="inventory_item"]')
for shop in shops:
    shop.click()
