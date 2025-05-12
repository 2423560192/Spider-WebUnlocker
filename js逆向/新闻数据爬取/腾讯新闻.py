import time
from selenium import webdriver  # # 驱动浏览器
from selenium.webdriver.common.by import By  # 选择器
import pymysql


# 连接数据库
db = pymysql.connect(
    user='root',
    password='root',
    database='learn',
    port=3306,
    host='127.0.0.1',
    charset='utf8mb4'

)
cursor = db.cursor()
# selenium配置
option = webdriver.ChromeOptions()
option.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=option)

# 请求数据
def parse_data(url):
    driver.get(url)
    # 往下翻页
    while True:
        data = driver.find_elements(By.XPATH, '//li[@class="item cf itme-ls"]//div[@class="detail"]/h3/a')
        for i in data:
            # 保存数据
            info = i.text
            print(info)
            save_data(info)
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)
        if '返回腾讯网' in driver.page_source:
            break

# 保存数据
def save_data(data):
    f = open('./腾讯新闻.txt', 'a', encoding='utf-8', newline='')
    f.write(data+'\n')
    # 保存数据
    # sql = 'insert into 腾讯新闻数据(标题) values (%s)'
    # cursor.execute(sql, data)
    # db.commit()

# 运行
def main():
    # 建表
    try:
        sql = 'create table 腾讯新闻数据 (标题 text)'
        cursor.execute(sql)
    except:
        print('数据表已经存在')
    url = 'https://new.qq.com/'
    parse_data(url)

main()

