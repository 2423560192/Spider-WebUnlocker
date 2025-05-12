import json
import random
import asyncio
import aiohttp
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from redis import Redis, ConnectionPool
from lxml import etree
from utils.send_mail import Mail


async def loadConf():
    import configparser

    config = configparser.RawConfigParser()
    with open('conf.ini', 'r', encoding='utf-8') as f:
        config.read_file(f)

    return config


async def get_data(session, url):
    pc_USE_AGENT = [
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3451.0 Safari/537.36',
        # 省略其他User-Agent
    ]
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'user-agent': random.choice(pc_USE_AGENT),
    }
    params = {
        'brand': 'ANC',
    }

    async with session.get(url, params=params, headers=headers) as response:
        return await response.text()


async def start(url, config):
    # 在每个协程中创建连接池
    pool = ConnectionPool(host='127.0.0.1', port=6379, db=0)
    conn = Redis(connection_pool=pool)

    async with aiohttp.ClientSession() as session:
        text = await get_data(session, url)
        text = etree.HTML(text)
        try:
            name = text.xpath('//*[@id="maincontent"]/div[2]/div[1]/div[2]/div[1]/h1//text()')[0].strip()
            price = text.xpath('//*[@id="maincontent"]/div[2]/div[1]/div[2]/div[2]/div[1]/span/span/span//text()')[0].strip()
            status = "".join(i.strip() for i in text.xpath('//*[@id="maincontent"]/div[2]/div[1]/div[2]/div[3]/div/div[1]//text()'))
            print("name: ", name)
            print("price: ", price)
            print("status: ", status)

            statu = conn.hget(f'shop:{name}', 'status')

            if statu is None:
                statu = 'ok'
            else:
                statu = statu.decode('utf-8')

            if '无库存' not in status and statu != status:
                conn.hset(f'shop:{name}', 'name', name)
                conn.hset(f'shop:{name}', 'price', price)
                conn.hset(f'shop:{name}', 'status', status)
                print('有最新数据更新，正在爬取......', name)

                # 发送邮件
                sender = config['MAIL']['sender']
                accepter = config['MAIL']['accepter'].split(',')
                password = config['MAIL']['password']
                for i in accepter:
                    i = i.strip()
                    Mail().start(f'有库存更新: {str(name)}——{str(price)}——{str(status)}, 链接:{url}', sender, i, password)

                # 发送短信
                mobile = config['PHONE']['mobile']
                account = config['PHONE']['account']
                password = config['PHONE']['password']
                content = config['PHONE']['content']

                from utils.send_code import send_sms
                send_sms(mobile, account, password, content)
            else:
                conn.hset(f'shop:{name}', 'name', name)
                conn.hset(f'shop:{name}', 'price', price)
                conn.hset(f'shop:{name}', 'status', status)
                print(name, '无库存更新')
            print('\n')
        except:
            pass


async def job():
    config = await loadConf()
    start_urls = json.loads(open('urls.json', encoding='utf-8').read())

    # 使用 asyncio.gather 并发处理所有URL
    tasks = [start(url, config) for url in start_urls]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    scheduler.add_job(job, 'interval', seconds=20, max_instances=4)
    print("定时任务开始...")
    scheduler.start()
    asyncio.get_event_loop().run_forever()
