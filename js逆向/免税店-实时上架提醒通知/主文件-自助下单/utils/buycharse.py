
import asyncio
import time

from pyppeteer import launch
from lxml import etree
from pyppeteer.errors import ElementHandleError


def loadConf():
    import configparser

    config = configparser.RawConfigParser()
    with open('conf.ini', 'r', encoding='utf-8') as f:
        config.read_file(f)

    return config

def parse_cookies(cookie_str):
    cookies = []
    for item in cookie_str.split('; '):
        try:
            name, value = item.split('=', 1)
            cookies.append({
                'name': name,
                'value': value,
                'domain': '.kixdutyfree.jp',
                'path': '/',
            })
        except ValueError:
            print(f"忽略无效的 Cookie 项目: {item}")
    return cookies

async def start(url):
    # 对应的pyppeteer相关的操作要写在特殊函数内部
    # 1.创建一个浏览器对象
    bro = await launch(
        handleSIGINT=False,
        handleSIGTERM=False,
        handleSIGHUP=False,
        headless=False,
        executablePath=r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-blink-features=AutomationControlled' , '--disable-infobars']
    )

    print(cookie)

    # 2.创建一个新的page
    page = await bro.newPage()
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36')
    await page.setCookie(*cookie)
    # 规避检测
    await page.evaluate('delete navigator.__proto__.webdriver')
    await page.evaluateOnNewDocument("""
            () => {
                Object.defineProperty(navigator, 'webdriver', { get: () => false });
                Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
                Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
            }
        """)
    #
    # # 3.发起请求
    # await page.goto(url)
    # # 4.获取页面源码数据
    # page_text = await page.content()
    # # 5.数据解析
    # # 选择目标元素的 XPath
    # input_xpath = '//*[@id="maincontent"]/div[2]/div[1]/div[2]/div[4]/div/div[2]/div[1]/input'
    #
    # # 等待元素加载
    # await page.waitForXPath(input_xpath)
    #
    # # 获取元素并输入内容
    # input_element = await page.xpath(input_xpath)
    # if input_element:
    #     # 点击元素以聚焦
    #     await input_element[0].click()
    #
    #     # 清空内容：选择全部文本然后删除
    #     await page.keyboard.down('Control')
    #     await page.keyboard.press('A')
    #     await page.keyboard.up('Control')
    #     await page.keyboard.press('Backspace')
    #     await input_element[0].type('1')  # 向输入框写入内容
    # else:
    #     print("元素未找到")
    #
    # # 点击添加
    # click_buy = '//*[@id="maincontent"]/div[2]/div[1]/div[2]/div[5]/div/div/button'
    #
    # # 确保按钮可见并加载完成
    # await page.waitForXPath(click_buy, options={'visible': True, 'timeout': 10000})
    #
    # buy_btn = await page.xpath(click_buy)
    #
    # await page.screenshot({'path': 'before_click.png'})
    #
    # if buy_btn:
    #     # 检查按钮是否禁用
    #     disabled = await page.evaluate('(element) => element.disabled', buy_btn[0])
    #     if not disabled:
    #         # 尝试点击按钮
    #         try:
    #             await buy_btn[0].hover()  # 悬停
    #             await buy_btn[0].click()  # 点击
    #         except:
    #             # 使用 JavaScript 模拟点击
    #             await page.evaluate('(element) => element.click()', buy_btn[0])
    #     else:
    #         print("购物车按钮被禁用")
    # else:
    #     print("购物车按钮未找到")

    # 进入购物车
    await page.goto('https://www.kixdutyfree.jp/cn/cart/')

    # 刷新页面
    await page.reload()

    # 进行信息填写
    # 日期
    departure_date_xpath = '//*[@id="departureDate"]'

    # 等待元素加载
    await page.waitForXPath(departure_date_xpath)

    # 获取输入框元素
    departure_input = await page.xpath(departure_date_xpath)

    if departure_input:
        # 点击输入框以聚焦
        await departure_input[0].click()

        # 清空输入框内容
        await page.keyboard.down('Control')
        await page.keyboard.press('A')
        await page.keyboard.up('Control')
        await page.keyboard.press('Backspace')

        # 填写日期
        date_value = "2024/11/25"  # 需要填写的日期
        await departure_input[0].type(date_value)

        print(f"成功填写日期: {date_value}")
    else:
        print("未找到出发日期输入框")

    # 时间
    # 选择时间选择器的 XPath
    departure_time_xpath = '//*[@id="departureTime"]'
    hours_xpath = '/html/body/div[6]/span[1]/select'
    minutes_xpath = '/html/body/div[6]/span[3]/select'

    # 点击 "departureTime" 元素
    await page.waitForXPath(departure_time_xpath)  # 等待元素加载完成
    departure_time_element = await page.xpath(departure_time_xpath)
    if departure_time_element:
        await departure_time_element[0].click()  # 点击 "departureTime"
        print("成功点击 's' 元素")
    else:
        print("'departureTime' 元素未找到")

    # 等待时间选择器显示并选择小时和分钟
    await page.waitForXPath(hours_xpath)  # 等待小时选择器加载
    await page.waitForXPath(minutes_xpath)  # 等待分钟选择器加载

    # 获取小时和分钟选择框元素
    hours_select = await page.xpath(hours_xpath)
    minutes_select = await page.xpath(minutes_xpath)

    if hours_select and minutes_select:
        # 选择小时，例如选择 10 点
        await page.evaluate('''(selectElement, value) => {
            const option = Array.from(selectElement.options).find(option => option.value === value);
            if (option) {
                selectElement.value = option.value;
                selectElement.dispatchEvent(new Event('change', { bubbles: true }));
            }
        }''', hours_select[0], '23')  # 选择 10 点

        # 选择分钟，例如选择 30 分钟
        await page.evaluate('''(selectElement, value) => {
            const option = Array.from(selectElement.options).find(option => option.value === value);
            if (option) {
                selectElement.value = option.value;
                selectElement.dispatchEvent(new Event('change', { bubbles: true }));
            }
        }''', minutes_select[0], '59')  # 选择 30 分

        print("成功选择时间: 10:30")
    else:
        print("未找到时间选择框")

    # 选择航空公司
    # 等待 select 元素加载
    await page.waitForSelector('#airlines')

    options = await page.xpath('//*[@id="airlines"]')

    await options[0].click()

    time.sleep(1)
    # 使用 `select` 方法选择值为 '3K' 的选项
    await page.select('#airlines', 'OD')  # '3K' 是选中的航空公司值

    # 手动触发事件，确保表单正确更新
    await page.evaluate('document.querySelector("#airlines").dispatchEvent(new Event("change"))')

    # 可选：检查是否已正确选择
    selected_value = await page.evaluate('document.querySelector("#airlines").value')
    print("Selected airline:", selected_value)

    # 选择航班
    # 等待 select 元素加载
    await page.waitForSelector('#flightno')

    # 使用 pyppeteer 的 select 方法来选择航班号
    await page.select('#flightno', '0881')  # 选择航班号 '0881'

    # 手动触发 change 事件，确保表单更新
    await page.evaluate('document.querySelector("#flightno").dispatchEvent(new Event("change"))')

    # 可选：检查已选中的值
    selected_value = await page.evaluate('document.querySelector("#flightno").value')
    print("Selected flight number:", selected_value)

    # 点击下一步
    # 等待目标按钮元素加载
    await page.waitForXPath('//*[@id="maincontent"]/div[3]/div[2]/div[1]/div[2]/div/div[8]/form/div[11]/button')

    # 获取按钮元素并点击
    button = await page.xpath('//*[@id="maincontent"]/div[3]/div[2]/div[1]/div[2]/div/div[8]/form/div[11]/button')
    await button[0].click()  # 点击第一个符合条件的按钮

    # 选择到店付
    # 等待目标按钮元素加载
    await page.waitForXPath('//div[@class="tab-link instore-payment-select"]')

    # 获取按钮并点击
    button = await page.xpath('//div[@class="tab-link instore-payment-select"]')
    await button[0].click()  # 点击第一个符合条件的按钮

    # 下单
    # 等待目标按钮元素加载
    await page.waitForXPath('//*[@id="checkout-main"]/div[1]/div[5]/div[2]/div[4]/div/div/button[2]')

    # 获取按钮并点击
    button = await page.xpath('//*[@id="checkout-main"]/div[1]/div[5]/div[2]/div[4]/div/div/button[2]')
    await button[0].click()  # 点击第一个符合条件的按钮


    # 确认
    # 等待目标按钮元素加载
    await page.waitForXPath('//*[@id="checkout-main"]/div[1]/div[8]/div[2]/div[3]/div/div/button[3]')

    # 获取按钮并确认
    button = await page.xpath('//*[@id="checkout-main"]/div[1]/div[8]/div[2]/div[3]/div/div/button[3]')
    if button:
        print("元素已找到，准备点击...")
        await button[0].click()  # 点击第一个符合条件的按钮
    else:
        print("元素未找到。")

    # 保持页面可见（开发调试时用）
    await page.waitFor(5000)  # 或者直接进入调试模式

    while True:
        time.sleep(1)
    # 关闭浏览器
    # await page.close()

def zizhu_buy(url):
    # 创建一个协程对象
    c = start(url)
    # 创建且启动事件循环对象
    loop = asyncio.get_event_loop()
    loop.run_until_complete(c)

if __name__ == '__main__':
    config = loadConf()
    cookie = config['INFO']['cookie']
    cookie = parse_cookies(cookie)
    url = 'https://www.kixdutyfree.jp/cn/%E7%BA%A2%E8%89%B2%E8%9C%9C%E9%9C%B2%E7%B2%BE%E5%8D%8E%E5%8C%96%E5%A6%86%E6%B6%B2%3C%E7%B2%BE%E5%8D%8E%E5%8C%96%E5%A6%86%E6%B6%B2%3E145ml-3425003416.html'
    zizhu_buy(url)
