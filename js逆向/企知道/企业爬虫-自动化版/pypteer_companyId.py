import asyncio
import random
from pyppeteer import launch
from lxml import etree


async def login(username , password):
    # 启动浏览器
    browser = await launch(
        handleSIGINT=False,
        handleSIGTERM=False,
        handleSIGHUP=False,
        headless=False,  # 可设置为 True 启动无头模式
        executablePath=r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-blink-features=AutomationControlled',
              '--disable-infobars']
    )

    page = await browser.newPage()

    # 设置 User-Agent
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    await page.setUserAgent(ua)

    # 设置 Headers
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    }
    await page.setExtraHTTPHeaders(headers)

    # 伪装自动化特征
    await page.evaluateOnNewDocument('''() => {
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
        }''')

    # 自动登录
    await page.goto(
        'https://www.qizhidao.com/login?redirect=https%3A%2F%2Fqiye.qizhidao.com%2F&businessSource=PC%E7%AB%99%E6%9F%A5%E4%BC%81%E4%B8%9A%E9%A6%96%E9%A1%B5-%E9%A1%B6%E6%A0%8F-%E7%AB%8B%E5%8D%B3%E7%99%BB%E5%BD%95&registerPage=https%3A%2F%2Fqiye.qizhidao.com%2F')

    # 模拟用户操作以绕过反爬
    await page.mouse.move(random.randint(100, 500), random.randint(100, 500))
    await page.mouse.click(random.randint(100, 500), random.randint(100, 500))

    # 登录流程
    await click_button(page,
                       '//*[@id="__layout"]/div/div[4]/div[2]/div/div/div[1]/div/div/div[2]/div/div[1]/div[2]/span')  # 点击登录
    await type_input(page,
                     '//*[@id="__layout"]/div/div[4]/div[2]/div/div/div[1]/div/div/div[2]/div/div[2]/form/div[1]/div/div/input',
                     username)  # 输入账号
    await type_input(page,
                     '//*[@id="__layout"]/div/div[4]/div[2]/div/div/div[1]/div/div/div[2]/div/div[2]/form/div[2]/div/div/input',
                     password)  # 输入密码
    await click_button(page,
                       '//*[@id="__layout"]/div/div[4]/div[2]/div/div/div[1]/div/div/div[2]/div/div[2]/form/div[4]/span/span/div/label/span/span')  # 同意协议
    await click_button(page,
                       '//*[@id="__layout"]/div/div[4]/div[2]/div/div/div[1]/div/div/div[2]/div/div[2]/form/div[5]/div/button')  # 点击登录按钮

    return page


async def click_button(page, xpath):
    """点击指定 XPath 的按钮"""
    element = await page.xpath(xpath)
    if element:
        await element[0].click()
    else:
        print(f"Element not found: {xpath}")


async def type_input(page, xpath, text):
    """在指定 XPath 的输入框中输入文本"""
    input_field = await page.xpath(xpath)
    if input_field:
        await input_field[0].type(text)
    else:
        print(f"Input field not found: {xpath}")


async def get_company_name(url, page):
    """
    使用 Pyppeteer 获取每一页企业的名称
    :param url: 目标 URL
    :param page: 已登录的页面对象
    :return: 企业名称列表
    """
    await page.goto(url, timeout=60000)

    # 等待关键元素加载
    await page.waitForSelector('span.companyName')

    # 获取页面内容
    content = await page.content()

    # 使用 lxml 解析内容
    lxml_tree = etree.HTML(content)
    name = lxml_tree.xpath('//span[@class="companyName"]//text()')

    return name


async def main():
    username = '13008322620'
    password = '5201314dongge'

    page = await login(username , password)  # 登录并获取页面对象


    for i in range(1, 100):
        print(f"抓取页数 {i}")
        target_url = f'https://qiye.qizhidao.com/lib/sce1c28e0ea7605b9280ecd7e73ce7dcb1/page-{i}/'
        company_names = await get_company_name(target_url, page)
        print(company_names)

        await asyncio.sleep(3)  # 模拟用户等待，避免过快请求


# 启动事件循环
if __name__ == '__main__':
    asyncio.run(main())
