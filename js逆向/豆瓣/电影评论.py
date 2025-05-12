"""
2023-6-2
"""
import ast
import random
import re
import time

import requests
from lxml import etree
from openpyxl import workbook

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'll="108309"; bid=nZ9tVZENctw; __yadk_uid=1nSIr9phi268homevjW57fXqKDCrbcHL; _vwo_uuid_v2=DC4D8B8EFFBBA4B07BDC97E8CA256F966|f608440ddaeb028a54e2328600becfe8; _ga=GA1.1.55163723.1682575274; _ga_RXNMP372GL=GS1.1.1682589496.1.1.1682589521.35.0.0; viewed="36229551"; __utmc=30149280; __utmz=30149280.1685675962.4.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmc=223695111; __utmz=223695111.1685675965.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ap_v=0,6.0; __gads=ID=0af400154519835d-2227fd41bbdf002d:T=1682575298:RT=1685690307:S=ALNI_MZOT_2OghY1zgkEg8uZQoZLEZAtcA; __gpi=UID=00000bfe166db3df:T=1682575298:RT=1685690307:S=ALNI_MY_B_CT7h6ycAyxcJo1xGGeLx0qHA; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1685694930%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DjrFGtG6qQAB4CW3EsUt-qUE5HuxbZqEs88ZtUyuipuoLhRtwMVeib2kLRJdDCyRM%26wd%3D%26eqid%3D8eaaebf500002a2c0000000664795fb6%22%5D; __utma=30149280.55163723.1682575274.1685690302.1685694930.6; __utma=223695111.665308278.1682589057.1685690302.1685694930.4; __utmb=223695111.0.10.1685694930; dbcl2="271094965:i0UrGpT73Cs"; ck=bu37; push_noty_num=0; push_doumail_num=0; _pk_ses.100001.4cf6=*; frodotk_db="28b327b576bab5147a19772064301f3c"; __utmt=1; __utmv=30149280.27109; __utmb=30149280.4.10.1685694930; _pk_id.100001.4cf6=02ce258b5ba242af.1682589057..1685696213.undefined.',
    'Referer': 'https://movie.douban.com/subject/34938015/?from=showing',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
}
ws = workbook.Workbook()
wb = ws.active
wb.append(['电影名', '评论总数', '好评数', '一般数', '差评数'])
ws.save('豆瓣电影评论.xlsx')

sign = True


def get_data(url, p):
    try:

        html_data = requests.get(url, headers=headers, params=p)
        time.sleep(1)
        if html_data.status_code == 200:
            data = html_data.text
            parse_data(data)
    except:
        get_data(url, p)


def parse_data(data):
    global sign
    lxml = etree.HTML(data)
    if sign:
        all_comments = lxml.xpath('//*[@id="content"]/div/div[1]/div[1]/ul/li[1]/span/text()')[0]  # 评论数
        all_comment = re.findall(r'\((\d+)\)', str(all_comments))[0]
        good = str(lxml.xpath('//*[@id="content"]/div/div[1]/div[3]/label[2]/span[2]/text()')[0]).replace('%', '')  # 好评
        hai = str(lxml.xpath('//*[@id="content"]/div/div[1]/div[3]/label[3]/span[2]/text()')[0]).replace('%', '')  # 一般
        bad = str(lxml.xpath('//*[@id="content"]/div/div[1]/div[3]/label[4]/span[2]/text()')[0]).replace('%', '')  # 差评
        movie = str(lxml.xpath('//*[@id="content"]/h1/text()')[0]).split(' ')[0]  # 差评
        print(movie)
        wb.append([movie, all_comment, int(all_comment) * int(good) // 100, int(all_comment) * int(hai) // 100,
                   int(all_comment) * int(bad) // 100])

        wb.append(['用户', '内容', '时间', '城市', '点赞数'])
        ws.save('豆瓣电影评论.xlsx')
        sign = False
    times = lxml.xpath('//div[@class="comment-item "]//span[@class="comment-time "]/text()')  # 时间
    content = lxml.xpath('//div[@class="comment-item "]//span[@class="short"]/text()')  # 内容
    people = lxml.xpath('//div[@class="comment-item "]//span[@class="comment-info"]/a/text()')  # 用户
    citys = lxml.xpath('//div[@class="comment-item "]//span[@class="comment-location"]/text()')  # 城市
    likes = lxml.xpath('//div[@class="comment-item "]//span[@class="votes vote-count"]/text()')  # 点赞数
    print(times)
    print(citys)
    print(content)
    print(likes)
    print(people)
    for t, c, l, co, p in zip(times, citys, likes, content, people):
        t = t.replace('\n', '').rstrip()
        wb.append([p, co, t, c, l])
        ws.save('豆瓣电影评论.xlsx')


if __name__ == '__main__':
    url = 'https://movie.douban.com/subject/35622911/comments'
    p = {
        'start': None,
        'limit': '20',
        'status': 'P',
        'sort': 'new_score'
    }
    i = 0
    try:
        while True:
            p['start'] = i * 20
            get_data(url, p)
            i += 1
    except:
        print('所有评论已爬取完毕!')
