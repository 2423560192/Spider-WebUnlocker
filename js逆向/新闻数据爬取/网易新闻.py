import time
from selenium import webdriver  # # 驱动浏览器
from selenium.webdriver.common.by import By  # 选择器
import csv
import pymysql


class SpiderWangYi:
    def __init__(self):
        self.option = webdriver.ChromeOptions()
        self.option.add_experimental_option('detach', True)
        self.driver = webdriver.Chrome(options=self.option)
        self.url = 'https://news.163.com/'

    # 请求数据
    def get_data(self, url):
        self.driver.get(url)
        self.driver.find_element(By.XPATH,
                                 '//*[@id="index2016_wrap"]/div[3]/div[2]/div[2]/div[2]/div/ul/li[5]/a').click()
        time.sleep(3)
        windows = self.driver.window_handles

        # 步骤2：切换到新窗口
        self.driver.switch_to.window(windows[-1])
        # print(self.driver.page_source)
        data = self.driver.find_elements(By.XPATH, '//div[@class="news_title"]//a')
        # print(data)
        for i in data:
            # 保存数据
            print(i.text)
            self.save_data(i.text)
        # 往下翻页
        while True:
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(1)
            # 每下拉一页获取当前页源码
            data = self.driver.page_source
            ata = self.driver.find_elements(By.XPATH, '//div[@class="news_title"]//a')
            for i in ata:
                # 保存数据
                print(i.text)
                self.save_data(i.text)
            if 'Complaint Center' in data:
                break

    # 保存数据
    def save_data(self, data):
        f = open('./网易新闻.csv', 'a', encoding='utf-8', newline='')
        csv_w = csv.writer(f)
        csv_w.writerow([data])
        # 保存为数据库
        try:
            # 建表
            sql = 'create table 网易新闻数据 (title text)'
            cursor.execute(sql)
            # 保存数据
            sql = 'insert into 网易新闻数据(title) values (%s)'
            cursor.execute(sql, data)
            db.commit()
        except:
            # 保存数据
            sql = 'insert into 网易新闻数据(title) values (%s)'
            cursor.execute(sql, data)
            db.commit()

    # 主方法
    def main(self):
        self.get_data(self.url)


if __name__ == '__main__':
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

    spider = SpiderWangYi()
    spider.main()
