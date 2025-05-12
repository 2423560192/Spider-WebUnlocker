import re
import time

import scrapy
from lxml.html import tostring
from lxml import etree
import pandas as pd
from long.items import LongItem


class ZixunSpider(scrapy.Spider):
    name = "zixun"
    allowed_domains = ["toutiao.com"]
    key_word = ['陶瓷', '茶杯', '茶具', '陶制品', '茶壶', '餐具', '电子产品',
                '手机', '平板', '电脑', '笔记本', '智能家电', '啤酒', '啤酒瓶', '碳酸饮料', '果汁', '茶壶',
                '食品', '糕点', '糖果', '零食', '咖啡', '方便面',
                ]

    # start_urls = ['https://so.toutiao.com/search?dvpf=pc&source=pagination&keyword=%E9%87%8D%E5%BA%86%E5%85%89%E7%BE%A4%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&pd=information&action_type=pagination&page_num=4&from=news&cur_tab_title=news&search_id=20230722173257F1CA623CD02FCD041D73']
    #

    def start_requests(self):
        lst = []
        # 所有企业
        df = pd.read_excel('企业基础信息.xlsx')

        for k, v in df.iterrows():
            lst.append(v[0])
        for k in lst[6962:]:
            for i in range(5):
                url = f'https://so.toutiao.com/search?dvpf=pc&source=pagination&keyword={k}&pd=information&action_type=pagination&page_num={i}&&from=news&cur_tab_title=news'
                yield scrapy.Request(url=url, callback=self.parse, meta={'company': k})

    def parse(self, response):
        # print(response.text)
        data = response.text
        company = response.meta['company']
        # titles = response.xpath(
        #     '//div[@class="s-result-list"]//div[@class="result-content"]//a[@class="text-ellipsis text-underline-hover"]')
        lxml = etree.HTML(data)
        titles = lxml.xpath(
            '//div[@class="s-result-list"]//div[@class="result-content"]//a[@class="text-ellipsis text-underline-hover"]')

        for j in titles:

            items = LongItem()
            items['company'] = company

            title = j.xpath('.//text()')
            print(''.join(title))
            items['title'] = ''.join(title)
            link = 'https://www.toutiao.com' + str(j.xpath('.//@href')[0])
            print(link)
            print('-----------------')
            items['link'] = link
            try:
                id = re.findall(r'%2Fa(.+?)%2F', link)[0]
                link = f'https://www.toutiao.com/article/{id}/?channel=&source=news'
                yield scrapy.Request(url=link, callback=self.get_content, meta={'items': items})
            except Exception as e:
                print(e)

    def get_content(self, response):
        data = response.text
        items = response.meta['items']
        lxml = etree.HTML(data)
        ti = lxml.xpath('//div[@class="article-meta"]/span[1]/text()')[0]
        if '-' not in ti:
            ti = lxml.xpath('//div[@class="article-meta"]/span[2]/text()')[0]
        items['date'] = ti

        content = lxml.xpath('//article')[0]
        html = tostring(content, encoding="utf-8").decode("utf-8")

        # 处理数据
        html = re.sub(r'<img .*?>', '', html)  # 去除图片
        html = re.sub(r'<p>.*?本头条号.*?</p>', '', html)
        html = re.sub(r'<p>.*?关注私信.*?</p>', '', html)
        html = re.sub(r'<p>.*?更多数据落地案例.*?</p>', '', html)
        html = re.sub(r'<p>.*?本文来自.*?</p>', '', html)
        html = re.sub(r'<p>.*?公众号.*?</p>', '', html)
        html = re.sub(r'<p>.*?此处已添加小程序，请到今日头条客户端查看.*?</p>', '', html)
        items['article'] = html

        # 临时关键字
        temp_key = []
        for k in self.key_word:
            if k in str(html):
                temp_key.append(k)
        if (items['company'] in str(html)) and temp_key:
            items['key'] = ','.join(temp_key)
            print(items)
            yield items


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute('scrpay crawl zixun --nolog'.split())
