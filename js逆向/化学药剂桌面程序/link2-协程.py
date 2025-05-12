import asyncio
import random
import traceback
import configparser
from lxml import etree
import aiohttp
import aiomysql
from DrissionPage._configs.chromium_options import ChromiumOptions
from DrissionPage._pages.chromium_page import ChromiumPage

# 配置加载
def loadConf():
    config = configparser.RawConfigParser()
    with open('utils/conf.ini', 'r', encoding='utf-8') as f:
        config.read_file(f)
    return config

# 异步数据库操作：初始化 MySQL 连接池
async def init_mysql_pool(config):
    pool = await aiomysql.create_pool(
        host=config['DATABASE']['host'],
        user=config['DATABASE']['user'],
        password=config['DATABASE']['password'],
        db=config['DATABASE']['database'],
        charset='utf8mb4',
        minsize=2,
        maxsize=10,
    )
    return pool

# 数据提取
async def get_data(text, url, conn):
    lxml = etree.HTML(text)
    products = []
    try:
        name = lxml.xpath("//*[@id='maincontent']/div[2]/div/div[2]/div[1]/h1/span/text()")[0]  # 名字

        try:
            CAS = lxml.xpath('//li[strong[contains(text(), "CAS")]]//span/a//text()')[0]  # CAS
        except Exception as e:
            print(f"CAS提取失败: {e}")
            CAS = ''

        try:
            molecular_weight = lxml.xpath('//li[strong[contains(text(), "分子量")]]//text()[2]')[0]  # 分子量
        except Exception as e:
            print(f"分子量提取失败: {e}")
            molecular_weight = ''

        try:
            purity = lxml.xpath('//td[@data-th="规格或纯度"]/text()')[0]  # 纯度
        except Exception as e:
            print(f"纯度提取失败: {e}")
            purity = ''

        rows = lxml.xpath('//table[@id="super-product-table"]/tbody/tr')

        for row in rows:
            sku = row.xpath('./td[@data-th="货号 (SKU) "]/text()')[0].strip()
            spec = row.xpath('./td[@data-th="包装规格"]/text()')[0].strip()
            storage = row.xpath('./td[contains(@class, "ajaxStock_")]/text()')[0].strip()
            original_price = row.xpath('./td[contains(@class, "ajaxPrice")]//span[@class="price"]//text()')[0].strip()

            dic = {
                'Name': name.strip(),
                'CAS': CAS.strip(),
                'Sku': sku,
                'Brand': '',
                'Molecular_weight': molecular_weight.strip(),
                'Purity': purity.strip(),
                'Price': original_price,
                'Spec': spec,
                'Storage': storage,
                'Source': url
            }
            products.append(dic)
            print(dic)
    except Exception as e:
        print(e)
        traceback.print_exc()  # 打印完整的异常堆栈信息

    await save_data(products, conn)

# 异步数据库操作：保存数据
async def save_data(goods_data, conn):
    try:
        async with conn.cursor() as cursor:
            insert_query = """
            INSERT INTO goods (goodsName, casIndexNo, goodsErpCode, brandName, goodsSpec, goodsStorePrice, goodsShowStorage, purity, molecularWeight, source)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = [(item['Name'], item['CAS'], item['Sku'], item['Brand'], item['Spec'], item['Price'],
                       item['Storage'], item['Purity'], item['Molecular_weight'], item['Source']) for item in
                      goods_data]
            await cursor.executemany(insert_query, values)
            await conn.commit()
            print(f"成功插入 {len(goods_data)} 条记录.")
    except Exception as e:
        print(f"数据库操作失败: {e}")

# 爬取任务
async def crawl_task(url_group, pool):
    headers = random.choice(USER_AGENTS)
    co = ChromiumOptions()
    co.auto_port()
    co.incognito(True)
    co.set_argument("--disable-gpu")
    co.set_user_agent(headers)
    co.headless(True)
    cp = ChromiumPage(co)

    try:
        # 从连接池获取数据库连接
        async with pool.acquire() as conn:
            for url in url_group:
                print(f"开始爬取: {url}")
                cp.listen.start('/catalogb/ajax/price/')
                cp.get(url, retry=2, interval=2, timeout=5)
                prices = cp.listen.wait()

                cp.wait.ele_displayed('//td[contains(@class, "ajaxPrice")]//span[@class="price"]', timeout=15)
                cp.wait.ele_displayed('//li[strong[contains(text(), "CAS")]]//span/a', timeout=15)
                text = cp.html
                await get_data(text, url, conn)
    except Exception as e:
        print(f"爬取任务失败: {e}")
    finally:
        cp.close()
        print('浏览器关闭')

# 主函数
async def main():
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    ]

    config = loadConf()

    # 初始化数据库连接池
    pool = await init_mysql_pool(config)

    with open('urls.txt', 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    # 将 URL 分组
    grouped_urls = [urls[i:i + 3] for i in range(0, len(urls), 3)]

    # 使用协程来并发执行爬取任务
    tasks = [crawl_task(group, pool) for group in grouped_urls]
    await asyncio.gather(*tasks)

# 运行主函数
if __name__ == '__main__':
    asyncio.run(main())
