#测试python、文件 是不是能正常运行
print(123)
#爬去数据
#地址
#导入库
import requests
from lxml import etree
import time
import re
#设置请求头
headers={'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}

for i in range(0,250,25):
    print(i)
    url = f'https://movie.douban.com/top250?start={i}'
    #读取数据
    response = requests.get(url=url,headers=headers)
    #print(response.text)
    html=etree.HTML(response.text)
    divs=html.xpath('//*[@id="content"]/div/div[1]/ol/li')#这个属性里面有双引号，外面就用单引号
    for div in divs:
        title = div.xpath('./div/div[2]/div[1]/a/span[1]/text()')[0] # 获取电影名称
        num = div.xpath('./div/div[2]/div[2]/div/span[2]/text()')[0]  # 评分
        pj = div.xpath('./div/div[2]/div[2]/div/span[4]/text()')[0]  # 评价
        href = div.xpath('./div/div[2]/div[1]/a/@href')[0]  # 链接

        info_all = div.xpath('./div/div[2]/div[2]/p/text()')[0]  # 获取导演名称
        times = div.xpath('./div/div[2]/div[2]/p/text()')[1]  # 获取时间
        art = info_all.strip().split('\xa0\xa0\xa0')[0].replace('导演:','').strip()
        tt = times.strip().split('/')[0].strip()  # 时间
        country = times.strip().split('/')[1].strip().replace(' ','/')  # 国家
        category = times.strip().split('/')[2].strip().replace(' ','/')  # 类型
        # for i in info_all:
        #     print(i)
        print(title,art,category, country, tt, num,pj,href)
        time.sleep(0.5)
        with open(r"dbmovie.csv", "a", encoding="utf-8") as f:  # 使用with open（）新建对象f ，a 表示追加
            f.write("{},{},{},{},{},{},{},{}".format(title,art,category, country, tt, num,pj,href))  # 将列表中的数据循环写入到文本文件中
            f.write("\n")





