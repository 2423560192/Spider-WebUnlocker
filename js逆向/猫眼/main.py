import re

import requests
from util import extract_text_from_font
from lxml import etree

cookies = {
    'uuid_n_v': 'v1',
    'uuid': '42FBBF10DEE011EFB0FFD1C5F73602032B292B93BC954D4A8C9A063729ED8B91',
    '_lxsdk_cuid': '194b639b88bc8-006173c987528d-26011b51-190140-194b639b88bc8',
    '_lxsdk': '42FBBF10DEE011EFB0FFD1C5F73602032B292B93BC954D4A8C9A063729ED8B91',
    '_ga': 'GA1.1.599567701.1738224024',
    '_lx_utm': 'utm_source%3Dgoogle%26utm_medium%3Dorganic',
    '_csrf': '659fa2f168532ce62b817c0bf6e467c132365656334af32d44711541fb77a5e8',
    'Hm_lvt_e0bacf12e04a7bd88ddbd9c74ef2b533': '1738224024,1738294667,1738301687',
    'HMACCOUNT': '74E03469813A9187',
    '_ga_WN80P4PSY7': 'GS1.1.1738301687.4.1.1738301714.0.0.0',
    'Hm_lpvt_e0bacf12e04a7bd88ddbd9c74ef2b533': '1738301714',
    '__mta': '108952381.1738224024371.1738301712283.1738301714341.24',
    '_lxsdk_s': '194badac3d4-80e-8c9-ff2%7C%7C18',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'uuid_n_v=v1; uuid=42FBBF10DEE011EFB0FFD1C5F73602032B292B93BC954D4A8C9A063729ED8B91; _lxsdk_cuid=194b639b88bc8-006173c987528d-26011b51-190140-194b639b88bc8; _lxsdk=42FBBF10DEE011EFB0FFD1C5F73602032B292B93BC954D4A8C9A063729ED8B91; _ga=GA1.1.599567701.1738224024; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; _csrf=659fa2f168532ce62b817c0bf6e467c132365656334af32d44711541fb77a5e8; Hm_lvt_e0bacf12e04a7bd88ddbd9c74ef2b533=1738224024,1738294667,1738301687; HMACCOUNT=74E03469813A9187; _ga_WN80P4PSY7=GS1.1.1738301687.4.1.1738301714.0.0.0; Hm_lpvt_e0bacf12e04a7bd88ddbd9c74ef2b533=1738301714; __mta=108952381.1738224024371.1738301712283.1738301714341.24; _lxsdk_s=194badac3d4-80e-8c9-ff2%7C%7C18',
    'Pragma': 'no-cache',
    'Referer': 'https://www.maoyan.com/films',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

params = {
    'showType': '2',
}

response = requests.get('https://www.maoyan.com/films', params=params, cookies=cookies, headers=headers)
res_data = response.text

# print(response.text)

# 正则获取字体url

font_url = "https:" + re.search('embedded-opentype"\),url\("(.*?)"\)', response.text).group(1)

with open('font.woff', 'bw') as f:
    f.write(requests.get(font_url).content)

# 解析字体文件
font_dict = extract_text_from_font('font.woff')
print(font_dict)
font_dict['x'] = '.'

# 处理字体映射
for k, v in font_dict.items():
    k = k.replace('uni', '&#x')
    k = k.lower()
    # print(k + ';' , v)
    res_data = re.sub(k + ';', v, res_data)
# print(res_data)


# 获取数字
lxml = etree.HTML(res_data)
num_data = lxml.xpath("//span[@class='stonefont']/text()")
# print(num_data)

# 获取名字
name_data = lxml.xpath("//div[@class='channel-detail movie-item-title']//@title")
# print(name_data)

for name, num in zip(name_data, num_data):
    print(name, num + '人')
