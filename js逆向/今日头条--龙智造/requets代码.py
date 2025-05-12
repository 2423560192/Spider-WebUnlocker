import time

import requests
from lxml import etree
import re
from lxml.html import tostring
import pandas as pd
import pymysql

h = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'tt_webid=7247401290177824293; _ga=GA1.1.386789261.1687417110; _S_IPAD=0; s_v_web_id=verify_lj6ta9w4_DX5qBcJM_vBzv_4EFb_AuYh_Apgy89fUX4oh; notRedShot=1; _tea_utm_cache_4916=undefined; msToken=uypY8Tm9w3B5na-VL-WgGWFvsFSS-vj6LenKTN6T9iMDN3vxk9twFX4erR5zsEoFog1bxZwAxmgRx91YK1YlZf3MN2b74h2FQ5xB7Pn7; ttwid=1%7CiFUajE4ULqVqoAzJb14gh_wySX2dBfeNv0O0Z9YY9og%7C1689990557%7C05252dd5a371410a2de98b6199ef7d242c0e0ca5ea0e017ec0fb340ba7ffb8da; _ga_QEHZPBE5HH=GS1.1.1689990537.4.0.1689990537.0.0.0; _S_DPR=1.5; _S_WIN_WH=1707_835; ttwid=1%7CiFUajE4ULqVqoAzJb14gh_wySX2dBfeNv0O0Z9YY9og%7C1689990557%7C05252dd5a371410a2de98b6199ef7d242c0e0ca5ea0e017ec0fb340ba7ffb8da',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
}

# 关键字列表
key_word = ['陶瓷', '茶杯', '茶具', '陶制品', '茶壶', '餐具', '电子产品',
            '手机', '平板', '电脑', '笔记本', '智能家电', '啤酒', '啤酒瓶', '碳酸饮料', '果汁', '茶壶',
            '食品', '糕点', '糖果', '零食', '咖啡', '方便面',
            ]


def parse(id, lst):
    try:
        url = f'https://www.toutiao.com/article/{id}/?channel=&source=news'
        data = requests.get(url, headers=h).text
        lxml = etree.HTML(data)
        ti = lxml.xpath('//div[@class="article-meta"]/span[1]/text()')[0]
        if '-' not in ti:
            ti = lxml.xpath('//div[@class="article-meta"]/span[2]/text()')[0]
        content = lxml.xpath('//article')[0]
        html = tostring(content, encoding="utf-8").decode("utf-8")  # 编码格式为源码编码格式

        # 处理数据
        html = re.sub(r'<img .*?>', '', html)  # 去除图片
        html = re.sub(r'<p>.*?本头条号.*?</p>', '', html)
        html = re.sub(r'<p>.*?关注私信.*?</p>', '', html)
        html = re.sub(r'<p>.*?更多数据落地案例.*?</p>', '', html)
        html = re.sub(r'<p>.*?本文来自.*?</p>', '', html)
        html = re.sub(r'<p>.*?公众号.*?</p>', '', html)
        html = re.sub(r'<p>.*?此处已添加小程序，请到今日头条客户端查看.*?</p>', '', html)
        lst.append(ti)
        lst.append(html)
        # 临时关键字
        temp_key = []
        for k in key_word:
            if k in str(html):
                temp_key.append(k)
        if (lst[1] in str(html)) and temp_key:
            lst.append(','.join(temp_key))
            # lst.append('123')
            # save_data(lst)

    except Exception as e:
        print(e)


def save_data(lst):
    print(lst)
    # 保存数据
    try:
        sql = 'insert into 资讯新闻(标题,对应企业,链接地址,发布日期,文章内容,关键词) values ("%s","%s","%s","%s","%s","%s")'
        cursor.execute(sql, lst)
        db.commit()
    except Exception as e:
        print(e)


def main():
    lst = []
    # 所有企业
    df = pd.read_excel('企业基础信息.xlsx')
    for k, v in df.iterrows():
        lst.append(v[0])
    for k in lst:
        for i in range(5):
            url = f'https://so.toutiao.com/search?dvpf=pc&source=pagination&keyword={k}&pd=information&action_type=pagination&page_num={i}&&from=news&cur_tab_title=news'
            data = requests.get(url, headers=h).text
            time.sleep(0.2)
            lxml = etree.HTML(data)
            titles = lxml.xpath(
                '//div[@class="s-result-list"]//div[@class="result-content"]//a[@class="text-ellipsis text-underline-hover"]')
            for j in titles:
                info = []
                title = j.xpath('.//text()')
                print(''.join(title))
                info.append(''.join(title))
                info.append(k)

                link = 'https://www.toutiao.com' + str(j.xpath('.//@href')[0])
                info.append(link)
                print(link)
                print('-----------------')
                id = re.findall(r'%2Fa(.+?)%2F', link)[0]
                parse(id, info)


if __name__ == '__main__':
    # 链接数据库
    db = pymysql.connect(
        user='root',
        password='root',
        database='龙智造企业数据',
        host='127.0.0.1',
        port=3306
    )
    cursor = db.cursor()
    # 创建表格
    try:
        sql = 'create table 资讯新闻(id int not null auto_increment primary key,标题 varchar(255),对应企业 varchar(255),链接地址 text,发布日期 varchar(255),文章内容 TEXT,关键词 varchar(255))'
        cursor.execute(sql)
    except Exception as e:
        print(e)
    main()
