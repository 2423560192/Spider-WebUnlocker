import json

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import requests


def login(url, username, password, driver):
    """模拟登录"""
    driver.get(url)
    # 最大化浏览器
    driver.maximize_window()
    try:
        with open('cookies_1.txt', 'r') as f:
            cookies_list = json.load(f)
            # 将expiry类型变为int
            for cookie in cookies_list:
                if isinstance(cookie.get('expiry'), float):
                    cookie['expiry'] = int(cookie['expiry'])
                driver.add_cookie(cookie)
    except:
        if not username and not password:
            # qq登录
            driver.find_element(By.XPATH, '//*[@id="qqLogin"]').click()
            # 跳转到最新页
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(20)  # 等待20s扫码
            ele = WebDriverWait(driver, 30, 0.5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="north"]/div/div[2]/div/div/a[2]'))
            )
        with open('cookies_1.txt', 'w') as f:
            # 将cookies保存为json格式
            f.write(json.dumps(driver.get_cookies()))
    driver.get(url)


def get_all_nums(url, driver):
    """获取主目录"""
    now_page_source = driver.page_source
    # print(now_page_source)
    # 获取主目录
    main_all = driver.find_elements(By.XPATH,
                                    '//*[@id="chapters-list"]//li[@class!="item one open" and @class!="item one close"]')

    # 获取主目录的时候，应该先把所有展开
    all_class_temp = driver.find_elements(By.XPATH,
                                          '//*[@id="chapters-list"]//li[@class="item one open" or @class="item one close"]')

    for i in all_class_temp[1:]:
        i.click()
    return main_all


def get_now_class(driver):
    """获取全部子小节"""
    time.sleep(3)
    # 获取当前课程
    all_class = driver.find_elements(By.XPATH, '//*[@id="slide_list"]//li')
    return all_class


def start_class(main_class, driver):
    """开始刷课"""
    for i in main_class[:-1]:
        # time.sleep(0.5)
        i.click()
        time.sleep(2)
        # 先判断是不是视频
        clas = i.get_attribute('class')

        is_player = True if 'v2' in clas else False

        # print('当前是否是视频：', is_player)

        try:
            ele = WebDriverWait(driver, 3, 0.5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="countText"]/span'))
            )
            tt = ele.text
            if tt == '已完成':
                continue
        except:
            pass

        if is_player:
            # 是视频
            # 开始播放视频
            driver.find_element(By.XPATH, '//*[@id="videoPlayer"]/xg-start/div[1]').click()
            # time.sleep(1)
            time.sleep(40)
            continue
            # while True:
            #     # 播放完成
            #     ele = WebDriverWait(driver, 10, 0.5).until(
            #         EC.presence_of_element_located((By.XPATH, '//*[@id="countText"]/span'))
            #     )
            #     if ele.text == '已完成':
            #         break
            #     # 开始播放
            #     else:
            #         # 获取时间
            #         tt = driver.find_element(By.XPATH, '//*[@id="videoPlayer"]/xg-controls/xg-time/span[2]').text
            #         # time.sleep(40)
            #         # t1 = int(tt.split(':')[0])
            #         # t2 = int(tt.split(':')[1])
            #         time.sleep(40)
            #         # if el.text == '重播':
            #         #     break
            #         driver.refresh()

        else:
            ele = WebDriverWait(driver, 600, 0.5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="countText"]/span'))
            )
            tt = ele.text
            if tt == '已完成':
                break
            else:
                # 获取时间
                tt = tt.replace('s', '')
                time.sleep(int(tt) + 3)


def get_pages(l, driver, nums):
    """每个章节"""
    for i in nums[l:l + 1]:
        i.click()
        # 获取当前所有的课程
        all_class = get_now_class(driver)
        # print(all_class)
        # 开始执行刷课
        start_class(all_class, driver)


def start(l):
    """运行主函数"""
    print('当前正在刷第几课： ', l)
    opt = Options()
    # opt.add_argument("--headless")
    opt.add_argument('--disable-gpu')
    opt.add_experimental_option("detach", True)
    driver = Chrome(options=opt)
    login(url, 0, 0, driver)  # 0,0代表使用qq登录
    time.sleep(3)
    nums = get_all_nums(url, driver)
    # 获取章节数量
    # 前往每个章节
    get_pages(l, driver, nums)
    print('当前课程已完成: ', l)
    driver.close()


# def get_len(url):
#     """获取课程长度"""
#     headers = {
#         'Cookie': '_abfpc=4f1b8fbf76e1984419119b84077062a018ac6bc5_2.0; __qc_wId=970; pgv_pvid=3322708320; cna=a8ebff09469ca4c83f6d1f222debdc51; thirdType=1; xsid=367EA1A2DADA9001; player=1',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
#     }
#     html_data = requests.get(url, headers=headers).text
#     print(html_data)
#     lxml = etree.HTML(html_data)
#     l = lxml.xpath('//*[@id="chapters-list"]//li[@class!="item one open" and @class!="item one close"]')
#     return len(l)


if __name__ == '__main__':
    url = 'https://www.cqooc.com/learn/mooc/structure?id=334572513'
    # le = get_len(url)
    # print('所有课程数： ', le)
    # 获取章节数量

    # 添加线程池
    with ThreadPoolExecutor(5) as t:
        for i in range(4, 21):
            try:
                t.submit(start, l=i)
            except Exception as e:
                print('唔哟，错误啦', e)
