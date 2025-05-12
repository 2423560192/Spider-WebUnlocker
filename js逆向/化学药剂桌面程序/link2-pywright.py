import configparser
import time
import random

import pymysql
from playwright.sync_api import sync_playwright
from lxml import etree

def loadConf():
    config = configparser.RawConfigParser()
    with open('utils/conf.ini', 'r', encoding='utf-8') as f:
        config.read_file(f)
    return config

# 初始化 MySQL 连接
def init_mysql(config):
    conn = pymysql.connect(
        host=config['DATABASE']['host'],
        user=config['DATABASE']['user'],
        password=config['DATABASE']['password'],
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    database = config['DATABASE']['database']

    # 创建数据库
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        print(f"数据库 '{database}' 创建成功。")
    except Exception as e:
        print(f"数据库创建失败: {e}")
    conn.select_db(database)

    return conn, cursor


def get_data(text):
    lxml = etree.HTML(text)
    try:
        name = lxml.xpath("//*[@id='maincontent']/div[2]/div/div[2]/div[1]/h1/span/text()")[0]  # 名字
        CAS = lxml.xpath("//*[@id='maincontent']/div[2]/div/div[2]/div[5]/div/ul/li[1]/span/a/text()")[0]  # CAS
        molecular_weight = lxml.xpath("/html/body/div[4]/main/div[2]/div/div[2]/div[5]/div/ul/li[3]/text()[2]")[0].strip()  # 分子量
        purity = lxml.xpath('//*[@id="maincontent"]/div[2]/div/div[2]/div[5]/ul/li/text()')[0]  # 纯度

    except IndexError:
        print("某些数据未找到！")
        return
    products = []
    rows = lxml.xpath('//table[@id="super-product-table"]/tbody/tr')
    for row in rows:
        sku = row.xpath('./td[@data-th="货号 (SKU) "]/text()')[0].strip()
        Spec = row.xpath('./td[@data-th="包装规格"]/text()')[0].strip()
        Storage = row.xpath('./td[contains(@class, "ajaxStock_")]/text()')[0].strip()
        original_price = row.xpath('./td[contains(@class, "ajaxPrice")]//span[@class="price"]//text()')[0].strip()
        dic = {
            'Name':name,
            'CAS':CAS,
            'Sku': sku,
            'Brand':'',

            'Molecular_weight':molecular_weight.strip(),
            'Purity':purity,
            'Price': original_price,
            'Spec': Spec,

            'Storage': Storage,
            'Source':url
        }
        products.append(dic)
        print(dic)
    save_data(products)

def save_data(goods_data):
    try:
        with conn.cursor() as cursor:
            # 插入数据的SQL语句
            insert_query = """
            INSERT INTO goods (goodsName, casIndexNo, goodsErpCode, brandName, goodsSpec, goodsStorePrice, goodsShowStorage, purity, molecularWeight, source)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            # 提取每个商品的数据，并格式化为适合执行插入的列表
            values = [(item['Name'], item['CAS'], item['Sku'], item['Brand'], item['Spec'], item['Price'],
                       item['Storage'], item['Purity'], item['Molecular_weight'], item['Source']) for item in goods_data]

            # 执行批量插入
            cursor.executemany(insert_query, values)

            # 提交事务
            conn.commit()
            print(f"成功插入 {cursor.rowcount} 条记录.")
    except Exception as e:
        print(f"数据库操作失败: {e}")

def main(url):
    with sync_playwright() as p:
        bro = p.chromium.launch(headless=True,
                                args=['--disable-blink-features=AutomationControlled',
                                      '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'])
        context = bro.new_context(user_agent=random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0.1 Safari/537.36",
            # 添加更多用户代理
        ]))

        # 打开主页面
        page = context.new_page()
        with open('stealth.min.js', 'r') as f:
            js = f.read()
        page.add_init_script(js)

        js = """
                Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});
                """
        page.add_init_script(js)


        page.goto(url)
        page.get_by_role("link", name="视图  Grid").click()
        page.get_by_label("显示", exact=True).select_option("48")
        page.goto(
            "https://www.aladdin-e.com/zh_cn/catalogsearch/result/index/?product_list_limit=48&product_list_mode=grid&q=%E4%B9%99%E9%86%87")

        # 等待商品链接加载完成
        page.wait_for_selector('a.product-item-link')
        try:
            while True:
                links = page.locator('a.product-item-link').all()

                # 点击所有链接，打开多个页面
                for link in links:
                    url = link.get_attribute('href')
                    print(url)
                    new_page = context.new_page()
                    with open('stealth.min.js', 'r') as f:
                        js = f.read()
                    new_page.add_init_script(js)

                    try:
                        # 尝试导航到链接
                        new_page.goto(url, timeout=60000)  # 60秒超时
                        time.sleep(1)  # 等待页面加载完成
                        text = new_page.content()
                        get_data(text)
                    except Exception as e:
                        print(f"无法打开页面 {url}，错误：{e}")
                    finally:
                        new_page.close()  # 关闭新页面以释放资源
                page.locator('//*[@id="amasty-shopby-product-list"]/div[4]/div[1]/ul/li[7]/a').click()
                time.sleep(5)
        except Exception as e:
            print(e)



        # 关闭主页面和浏览器
        page.close()
        bro.close()

if __name__ == '__main__':
    config = loadConf()
    conn, cursor = init_mysql(config)
    url = "https://www.aladdin-e.com/zh_cn/catalogsearch/result/index/?product_list_limit=60&q=%E4%B9%99%E9%86%87"
    main(url)
