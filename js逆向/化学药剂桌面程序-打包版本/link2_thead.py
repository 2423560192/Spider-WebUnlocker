import time
import random
import pymysql
import requests
from DrissionPage import ChromiumPage, ChromiumOptions
from lxml import etree
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

# 获取商品数据
def get_price(original_price, cookies):
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.aladdin-e.com',
        'referer': 'https://www.aladdin-e.com/zh_cn/e111964.html',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    response = requests.post('https://www.aladdin-e.com/zh_cn/catalogb/ajax/price/', cookies=cookies, headers=headers,
                             data=original_price)

    price_data = response.json()
    price_pattern = re.compile(r'¥([\d\.]+)')
    prices = {}
    for key, html in price_data.items():
        match = price_pattern.search(html)
        if match:
            prices[key] = float(match.group(1))

    return prices


def get_data(text, cookies , conn):
    lxml = etree.HTML(text)
    name = lxml.xpath("//*[@id='maincontent']/div[2]/div/div[2]/div[1]/h1/span/text()")[0]

    try:
        CAS = lxml.xpath('//li[strong[contains(text(), "CAS")]]//span/a//text()')[0]  # CAS
    except Exception as e:
        CAS = ''

    try:
        molecular_weight = lxml.xpath('//li[strong[contains(text(), "分子量")]]//text()[2]')[0]  # 分子量
    except Exception as e:
        molecular_weight = ''

    try:
        purity = lxml.xpath('//td[@data-th="规格或纯度"]/text()')[0]  # 纯度
    except Exception as e:
        purity = ''

    products = []
    rows = lxml.xpath('//table[@id="super-product-table"]/tbody/tr')
    price_lst = []
    for row in rows:
        sku = row.xpath('./td[@data-th="货号 (SKU) "]/text()')[0].strip()
        spec = row.xpath('./td[@data-th="包装规格"]/text()')[0].strip()
        storage = row.xpath('./td[contains(@class, "ajaxStock_")]/text()')[0].strip()
        original_price = row.xpath('./td[contains(@class, "ajaxPrice")]/@id')[0].strip()
        price_lst.append(original_price)

        dic = {
            'Name': name.strip(),
            'CAS': CAS.strip(),
            'Sku': sku.strip(),
            'Molecular_weight': molecular_weight.strip(),
            'Purity': purity.strip(),
            'Price': '',
            'Spec': spec,
            'Storage': storage,
            'Source': 'https://www.aladdin-e.com/zh_cn/'
        }
        print(dic)
        products.append(dic)
    try:
        price_data = get_price({f"{price}": price for i, price in enumerate(price_lst)}, cookies)
        for price, product in zip(price_data.values(), products):
            product['Price'] = price
    except:
        pass

    save_data(products, conn)


# 保存数据到 MySQL
def save_data(goods_data, conn):
    try:
        with conn.cursor() as cursor:
            insert_query = """
            INSERT INTO goods (goodsName, casIndexNo, goodsErpCode, goodsSpec, goodsStorePrice, goodsShowStorage, purity, molecularWeight, source)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            values = [(item['Name'], item['CAS'], item['Sku'], item['Spec'], item['Price'],
                       item['Storage'], item['Purity'], item['Molecular_weight'], item['Source']) for item in
                      goods_data]

            cursor.executemany(insert_query, values)
            conn.commit()
            print(f"成功插入 {cursor.rowcount} 条记录.")
    except Exception as e:
        print(f"数据库操作失败: {e}")


# 获取 URL
def get_urls(cp, base_url):
    cp.get(base_url, retry=3, interval=2, timeout=15)

    f = open('urls.txt', 'w')

    for i in range(1, 2):
        urls = cp.eles('tag:a@class=product-item-link')

        for i in urls:
            url = i.link
            f.write(str(url) + '\n')

        next = cp.ele('xpath://a[@class="action next"]', timeout=3)
        if next:
            next.click()
        else:
            print('没有下一页了')
            break
    f.close()


# 多线程爬取数据
def link2_main(name):
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
    ]

    headers = random.choice(USER_AGENTS)

    co = ChromiumOptions()
    co.auto_port()
    # co.incognito(True)
    co.set_argument("--disable-gpu")
    co.set_user_agent(headers)
    co.headless(True)

    cp = ChromiumPage(co)

    base_url = f'https://www.aladdin-e.com/zh_cn/catalogsearch/result/index/?p=1&product_list_limit=16&product_list_mode=grid&q={name}'

    get_urls(cp, base_url)

    cookies_list = cp.cookies()
    cookies = {cookie['name']: cookie['value'] for cookie in cookies_list}

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    # 线程池，抓取多个 URL
    with open('urls.txt', 'r') as f:
        urls = [line.strip() for line in f.readlines() if line.strip() != 'None']

    def fetch_url(url):
        import db
        conn = db.pool.connection()
        try:
            print(f'开始爬取：{url}')
            text = requests.get(url, cookies=cookies, headers=headers).text
            get_data(text, cookies , conn)
        except Exception as e:
            print(f"抓取 {url} 失败: {e}")
        finally:
            conn.close()

    # 使用线程池
    with ThreadPoolExecutor(max_workers=5) as executor:  # 设定最大并发线程数
        futures = [executor.submit(fetch_url, url) for url in urls]
        for future in as_completed(futures):
            future.result()  # 获取每个线程的执行结果
    cp.close()

