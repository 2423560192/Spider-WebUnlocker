import time
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from openpyxl import workbook


def get_page(driver, theme, author, origin):
    # 打开页面
    driver.get("https://kns.cnki.net/kns8/AdvSearch")

    # 选择作者单位
    WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, '''//*[@id="gradetxt"]/dd[1]/div[2]/div[1]/div[1]/span'''))).click()
    driver.find_element(By.XPATH, '//*[@id="gradetxt"]/dd[1]/div[2]/div[1]/div[2]/ul/li[9]').click()

    # 传入作者机构
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '''//*[@id="gradetxt"]/dd[1]/div[2]/input'''))).send_keys(theme)

    # 传入作者
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '''//*[@id="gradetxt"]/dd[2]/div[2]/input'''))).send_keys(author)

    # 传入文献来源
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '''//*[@id="gradetxt"]/dd[3]/div[2]/input'''))).send_keys(origin)

    elm1 = driver.find_element(By.XPATH, '//*[@id="datebox0"]')
    elm2 = driver.find_element(By.XPATH, '//*[@id="datebox1"]')
    js1 = 'arguments[0].removeAttribute("readonly");'
    driver.execute_script(js1, elm1)
    driver.execute_script(js1, elm2)
    # 传入时间
    t1 = input('请输入开始时间，请按照(2023-08-26)格式来:')
    t2 = input('请输入结束时间，请按照(2023-08-26)格式来:')
    now = driver.find_element(By.XPATH,'//*[@id="ModuleSearch"]/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[2]/b')
    elm1.send_keys(t1)
    elm1.click()
    elm2.send_keys(t2)
    time.sleep(1)
    elm2.click()


    # 点击搜索
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="ModuleSearch"]/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[3]/input'))).click()

    time.sleep(3)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="ModuleSearch"]/div[2]/div/div/ul/li[1]/a'))).click()
    time.sleep(1)
    # 获取总文献数和页数
    res_unm = WebDriverWait(driver, 20).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="countPageDiv"]/span[1]/em'))).text

    # 处理篇数
    res_unm = int(res_unm.replace(",", ''))
    page_unm = int(res_unm / 20) + 1
    print(f"共找到 {res_unm} 条结果, {page_unm} 页。")
    return res_unm


def crawl(driver, papers_need):
    count = 1  # 总篇数
    while count <= papers_need:
        time.sleep(2)

        # 获取所有的篇数对象
        title_list = WebDriverWait(driver, 100).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "fz14")))

        lst = []
        #  添加对象
        for i in title_list:
            if count <= papers_need:
                lst.append(i)
                count += 1

        for content_url in lst:
            time.sleep(1)
            content_url.click()
            n = driver.window_handles
            # driver切换至最新生产的页面
            driver.switch_to.window(n[-1])
            # 获取数据
            try:
                top = driver.find_elements(By.XPATH, '//div[@class="top-tip"]')[0]  # 顶部
                top = top.text
            except:
                top = '-'
            print(top)
            try:
                tt = driver.find_element(By.XPATH,'/html/body/div[2]/div[1]/div[3]/div/div/div[2]/div[1]/span').text  # 时间
            except Exception as e:
                tt = '空'
                print(e)
            title = driver.find_element(By.XPATH,'/html/body/div[2]/div[1]/div[3]/div/div/div[3]/div/h1').text  # 标题
            print(title)
            author = driver.find_elements(By.XPATH, '//*[@id="authorpart"]//span')  # 作者
            authors = ''
            for a in author:
                authors += str(a.text) + ';'
        #
            place = driver.find_elements(By.XPATH,
                                         '/html/body/div[2]/div[1]/div[3]/div/div[1]/div[3]/div[1]/h3[2]')  # 发表地
            place = [i.text for i in place][0]
        #
            detail_k = driver.find_elements(By.XPATH,"//div[@class='row']//span[@class='rowtit']")
            detail_k_now = []
            for i in detail_k:
                detail_k_now.append(i.text)

            detail_v = driver.find_elements(By.XPATH,"//div[@class='row']//p|//div[@class='row']//span[@class='abstract-text']")
            values = []
            for i in detail_v:
                values.append(i.text)
            dic = {}
            for k, v in zip(detail_k_now, values):
                k = k.replace('：', '')
                dic[k] = v
                print(k, v)

            # 做一些特殊处理
            try:
                dic['摘要'] = dic['摘要']
            except:
                dic['摘要'] = '无'
            try:
                dic['关键词'] = dic['关键词']
            except:
                dic['关键词'] = '无'
            try:
                dic['基金资助'] = dic['基金资助']
            except:
                dic['基金资助'] = '无'
            try:
                dic['专辑'] = dic['专辑']
            except:
                dic['专辑'] = '无'
            try:
                dic['专题'] = dic['专题']
            except:
                dic['专题'] = '无'
            try:
                dic['分类号'] = dic['分类号']
            except:
                dic['分类号'] = '无'

            info = [top, tt, title, authors, place, dic['摘要'], dic['关键词']
                , dic['基金资助'], dic['专辑'], dic['专题'], dic['分类号']]
            print(info)
            save_data(info)

            n2 = driver.window_handles
            if len(n2) > 1:
                driver.close()
                driver.switch_to.window(n2[0])

        time.sleep(2)

        # 翻下一页
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="PageNext"]'))).click()
        time.sleep(3)


def save_data(data):
    wb.append(data)
    ws.save('知网数据.xlsx')


if __name__ == "__main__":
    # 创建表
    ws = workbook.Workbook()
    wb = ws.active
    wb.append(['来源', '日期', '标题', '作者', '来源地', '摘要', '关键词', '基金资助', '专辑', '专题', '分类号'])
    ws.save('知网数据.xlsx')

    # 配置驱动器
    option = webdriver.ChromeOptions()
    option.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    # option.add_argument("headless")
    option.add_argument('--disable-gpu')
    option.add_experimental_option('detach', True)
    driver = webdriver.Chrome(options=option)

    # 设置搜索作者单位
    theme = input('请输入作者单位：')
    # 作者
    author = input('请输入作者：')
    # 文献来源
    origin = input('请输入来源：')

    print('正在获取页数，请等待.....')

    res_unm = int(get_page(driver, theme, author, origin))
    # 请输入你要获取的篇数
    papers_need = int(input('请输入你想要获取的篇数：'))

    # 判断篇数是否超出
    if (papers_need <= res_unm):
        papers_need = papers_need
    else:
        papers_need = res_unm
    crawl(driver, papers_need)
