import asyncio
import time
import random
from pyppeteer import launch
from lxml import etree


async def simulate_human_actions(page):
    for _ in range(5):  # 模拟5次鼠标移动
        x, y = random.randint(0, 800), random.randint(0, 600)
        await page.mouse.move(x, y)
        await asyncio.sleep(random.uniform(0.5, 1))


async def u_jd1(ck, url):
    browser = await launch(
        handleSIGINT=False,
        handleSIGTERM=False,
        handleSIGHUP=False,
        headless=True,
        executablePath=r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-blink-features=AutomationControlled']
    )
    page = await browser.newPage()
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36')

    # 规避检测
    await page.evaluateOnNewDocument("""
        () => {
            Object.defineProperty(navigator, 'webdriver', { get: () => false });
            Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
        }
    """)
    # 设置 Cookies
    # 打开目标页面
    await page.setCookie(*ck)
    # 打开目标页面
    await page.goto(url)
    # await page.waitForSelector('#item-stamp')  # 替换为目标页面的特定选择器

    # 模拟人类行为
    await simulate_human_actions(page)

    # 获取页面内容
    content = await page.content()
    tree = etree.HTML(content)
    sign = False

    try:
        # 等待元素加载
        await page.waitForXPath(
            '//*[@id="/item?stamp=1"]/taro-view-core/taro-view-core[2]/taro-view-core[1]/taro-view-core/taro-view-core/taro-view-core/taro-view-core[2]',
            timeout=1000
        )

        # 查找元素
        elements = await page.xpath(
            '//*[@id="/item?stamp=1"]/taro-view-core/taro-view-core[2]/taro-view-core[1]/taro-view-core/taro-view-core/taro-view-core/taro-view-core[2]')
        # 点击第一个匹配的元素
        if elements:
            await elements[0].click()
            sign = True
        else:
            print("Element not found!")
    except:
        pass

    # 2.
    try:
        # 等待父级容器加载完成
        await page.waitForXPath('//div[@class="btn-area"]', timeout=1000)

        elements = await page.xpath(
            '//div[@class="btn-area"]')

        # 点击第一个匹配的元素
        if elements:
            await elements[0].click()
            sign_text = tree.xpath('//*[@id="app"]/div/div/div/div/div[2]/div/div[1]/div[2]//text()')[0]
            if '购买' not in sign_text:
                sign = True
        else:
            print("Element not found!")
    except:
        pass

    # 3.
    try:
        # 等待父级容器加载完成
        await page.waitForXPath('//*[@id="J_babelOptPage"]/div/div[4]/div/div/div[2]/div[2]', timeout=1000)

        # 获取所有 span 元素
        elements = await page.xpath(
            '//*[@id="J_babelOptPage"]/div/div[4]/div/div/div[2]/div[2]//span[@class="btnText"]')

        if elements:
            print(f"找到 {len(elements)} 个符合条件的按钮")
            for index, element in enumerate(elements):
                try:
                    # 点击每个 span 元素
                    await element.click()
                    sign = True
                    print(f"第 {index + 1} 个按钮已点击")
                    # 根据实际需求，可能需要等待一定时间以避免请求冲突
                    await page.waitForTimeout(500)  # 等待 0.5 秒
                except Exception as e:
                    print(f"第 {index + 1} 个按钮点击失败: {e}")
        else:
            pass

    except:
        pass

    await browser.close()

    if sign:
        print(f'url：{url}领取成功! ')
        return '领取成功'
    else:
        print(f'url：{url}领取失败! ')
        return '此券已被领取或已被抢空，请早点来哟！'


def start_u_jd(ck, url):
    msg = asyncio.run(u_jd1(ck, url))
    return msg


def send_jd(ck, url):
    print(ck, '正在运行')
    if 'u.jd' in url:
        msg = start_u_jd(ck, url)
        return msg
