import time

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from lxml import etree

lst = []

def get_data(url):
    driver.get(url)
    time.sleep(3)
    lxml = etree.HTML(driver.page_source)
    links = lxml.xpath('//div[@class="postPiccaipu"]//div[@class="pic_art_img"]//a/@href')
    print(links)
    for i in range(3):
        for j in links:
            lst.append(j)
        time.sleep(3)
        print(driver.page_source)
        driver.find_element(By.XPATH,'//div[@class="pages"]//a[@class="a1"]').click()
    for i in lst:
        parse_data(i)



def parse_data(url):
    driver.get(url)
    lxml = etree.HTML(driver.page_source)
    content = lxml.xpath('//div[@class="content "]//text()')
    content = ''.join(content).strip()
    print(content)
    name = lxml.xpath('//*[@id="content"]/h1/text()')[0]
    with open(f'./数据/{name}.txt','w',encoding='utf-8') as f:
        f.write(content)


if __name__ == '__main__':
    driver = webdriver.Chrome()
    url = 'https://www.meishic.com/caipu/zhuanti/huigerou.html'
    get_data(url)


