import time

from selenium import webdriver
from selenium.webdriver.common.by import By
import pymysql
from TEXT import YdmVerify

# 链接数据库

db = pymysql.connect(
        user='root',
        password='root',
        port=3306,
        host='127.0.0.1',
        charset='utf8mb4',
        database='learn'
    )
cursor = db.cursor()

# 创建数据库表
try:
    sql = 'create table 知网大数据(id int not null auto_increment primary key,title varchar(255),name varchar(255),source varchar(255),date varchar(255))'
    cursor.execute(sql)
except Exception as e:
    print('建表错误', e)

url = 'https://kns.cnki.net/KNS8/AdvSearch?dbcode=CJFQ'

# 配置selenium
option = webdriver.ChromeOptions()
# option.add_argument('headless')
option.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=option)

driver.get(url)
time.sleep(3)

# 输入大数据关键词
word = driver.find_element(By.XPATH,'//*[@id="gradetxt"]/dd[1]/div[2]/input').send_keys('大数据')
# 选择大数据
driver.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/input').click()

time.sleep(5)
# 开始查找
driver.find_element(By.XPATH,'//*[@id="divGroup"]/dl[1]/dd[1]/div/ul/li[1]/input').click()
time.sleep(3)
i = 0



# 获取数据
def info():
    title = driver.find_elements(By.XPATH, '//td[@class="name"]/a')
    name = driver.find_elements(By.XPATH, '//td[@class="author"]')
    source = driver.find_elements(By.XPATH, '//td[@class="source"]/a')
    date = driver.find_elements(By.XPATH, '//td[@class="date"]')
    for t, n, s, d in zip(title, name, source, date):
        lst = []
        print(t.text)
        print(n.text)
        print(s.text)
        print(d.text)
        lst.append(t.text)
        lst.append(n.text)
        lst.append(s.text)
        lst.append(d.text)
        # 插入数据进数据库
        sql = 'insert into 知网大数据(title,name,source,date) values ("%s", "%s","%s","%s")'
        try:
            cursor.execute(sql, lst)
            # 提交数据库
            db.commit()
        except Exception as e:
            print(e)
        print('=================')
    # 点击下一页
    driver.find_element(By.XPATH, '//*[@id="PageNext"]').click()
    time.sleep(2)

try:
    while True:
        try:
            info()
        except:
            # 获取验证码图片
            img_code = driver.find_element(By.ID, 'changeVercode')
            img_code.screenshot('img.png')  # 保存成图片
            # 调用验证码解析
            Y = YdmVerify()
            with open('img.png', 'rb') as f:
                s = f.read()
            data = Y.click_verify(image=s, extra="家,炉,私")
            # 获取到的验证码
            print(data)
            # 输入验证码
            driver.find_element(By.XPATH, '//*[@id="vericode"]').send_keys(data)
            driver.find_element(By.XPATH, '//*[@id="checkCodeBtn"]').click()
            time.sleep(3)
            # 如果验证码错误，将再一次执行输入验证码
            if '验证码错误' in driver.page_source:
                driver.find_element(By.XPATH, '//*[@id="changeVercode"]').click()
                time.sleep(1)
                # 清空
                driver.find_element(By.XPATH, '//*[@id="vericode"]').clear()
                time.sleep(2)
                # 输入验证码
                driver.find_element(By.XPATH, '//*[@id="vericode"]').send_keys(data)
                driver.find_element(By.XPATH, '//*[@id="checkCodeBtn"]').click()
                time.sleep(1)


except:
    print('错误')




