#--*encoding=UTF-8*--
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from urllib.parse import urljoin
from openpyxl import workbook
"""
['\n', '中华中医药学刊', '.\n          ', '北大核心', '\n']
['麦冬抗肿瘤作用机制研究进展', '\n']
['（录用定稿）网络首发时间：2023-08-25 18:09:36']
['\n', '高剑坤', '1,2,3', '梁雪兰', '1,2,3', '江洪波', '1,2,3', '林秋霞', '1,2,3', '夏清', '1,2,3', '153655003@qq.com', '\n']
['\n', '1. 四川中医药高等专科学校药学院', '2. 川西北中药资源研究与开发利用实验室', '3. 绵阳市中药资源开发与利用重点实验室', '\n']
['麦冬是我国的传统中药，具有养阴生津、润肺清心的功效。越来越多的研究发现，麦冬除了传统功效外还具有对多种肿瘤的抑制作用。麦冬可通过抑制肿瘤细胞增殖、诱导肿瘤细胞凋亡、坏死性凋亡、铁死亡、焦亡、自噬、细胞周期阻滞、抑制肿瘤细胞转移和血管生成以及逆转肿瘤细胞耐药性等多种机制发挥抗肿瘤作用。本文对近年来麦冬块根提取物及其活性单体的抗肿瘤作用研究进展进行综述，为麦冬抗肿瘤的深入研究和对麦冬的进一步开发利用提供可借鉴的思路和方向。']
['\n', '麦冬;\n                      ', '抗肿瘤;\n                      ', '作用机制;\n                      ', '研究进展;\n                      ', '\n']
['四川省中医药科技产业创新团队专项课题麦冬大健康产品开发创新团队（2022C002）；\n                                                四川省中医药重点学科中药化学建设项目；\n                                                ']
['医药卫生科技']
['\n', '分类号：', '\n', 'R285', '\n']
"""

# top = ['摘要：', '关键词：', '基金资助：', '专辑：', '专题：', '分类号：']
# top2 = ['麦冬是我国的传统中药，具有养阴生津、润肺清心的功效。越来越多的研究发现，麦冬除了传统功效外还具有对多种肿瘤的抑制作用。麦冬可通过抑制肿瘤细胞增殖、诱导肿瘤细胞凋亡、坏死性凋亡、铁死亡、焦亡、自噬、细胞周期阻滞、抑制肿瘤细胞转移和血管生成以及逆转肿瘤细胞耐药性等多种机制发挥抗肿瘤作用。本文对近年来麦冬块根提取物及其活性单体的抗肿瘤作用研究进展进行综述，为麦冬抗肿瘤的深入研究和对麦冬的进一步开发利用提供可借鉴的思路和方向。', '\n', '麦冬;\n                      ', '抗肿瘤;\n                      ', '作用机制;\n                      ', '研究进展;\n                      ', '\n', '四川省中医药科技产业创新团队专项课题麦冬大健康产品开发创新团队（2022C002）；\n                                                四川省中医药重点学科中药化学建设项目；\n                                                ', '医药卫生科技', '中药学', 'R285', '\n', '中国知网独家网络首发，未经许可，禁止转载、摘编。\n                                        ']
# dic = {}
#
# for k,v in zip(top,top2):
#     dic[k] = v
#     print(k,v.strip())
#
# if dic['牛魔']:
#     print(123)
# else:
#     print(456)

url = 'https://kns.cnki.net/kcms2/article/abstract?v=3uoqIhG8C45S0n9fL2suRadTyEVl2pW9UrhTDCdPD67eKH-tlDDwBhwwACiu45O59I2R6ANf5dg8pJHTWSjL4tziWaIX4Viw&uniplatform=NZKPT'
option = webdriver.ChromeOptions()
# option.add_argument('headless')
option.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=option)
driver.get(url)
lxml = etree.HTML(driver.page_source)
# top = lxml.xpath('//div[@class="top-tip"]//text()')  # 顶部
# top = ['\n', '高分子学报', '.\n          ', '北大核心', 'SCI', 'CSCD', '\n']
# lst = []
# for i in top:
#     if '\n' not in i:
#         lst.append(i)
# print(';'.join(lst))
place = driver.find_elements(By.XPATH,'/html/body/div[2]/div[1]/div[3]/div/div[1]/div[3]/div[1]/h3[2]')  # 发表地
lst = [i.text for i in place]
print(lst)
# print(''.join([i.replace('.','') for i in top]))


# print(';'.join([''.join(top[i:i+2]) for i in range(1, len(top)-2, 2)]))



