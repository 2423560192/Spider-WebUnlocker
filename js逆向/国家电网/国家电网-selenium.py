import time
import zipfile

from selenium import webdriver
from selenium.webdriver.common.by import By

url = 'https://ecp.sgcc.com.cn/ecp2.0/portal/#/doc/doci-bid/2023072854280663_2018032700291334'

option = webdriver.ChromeOptions()
# option.add_argument('headless')
option.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=option)
driver.get(url)
time.sleep(3)
driver.find_element(By.XPATH,'/html/body/app-root/app-main/app-doc/app-doci-bid/div/div/div[2]/div[2]/table/tbody/tr[6]/td[2]/a/span').click()

#
# time.sleep(5)


# # 解压文件
# def unzip_file(zip_src, dst_dir):
#     r = zipfile.is_zipfile(zip_src)
#     if r:
#         fz = zipfile.ZipFile(zip_src, 'r')
#         for file in fz.namelist():
#             fz.extract(file, dst_dir)
#     else:
#         print('This is not zip')
#
#
# # 示例用法
# zip_file_path = r'C:/Users/lenovo/Downloads/招标公告 (3).zip'  # 替换为你要解压的 ZIP 文件的路径
#
# extract_to_dir = r'C:\Users\lenovo\Desktop\解压文件'  # 替换为你要将文件解压到的目标文件夹路径
#
# unzip_file(zip_file_path, extract_to_dir)
