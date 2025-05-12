import requests

import util
from jsonpath import jsonpath

cookies = {
    'ttwid': '1%7CQyIhjQ4tbKjxsQc_BtLELfe2JMlCStflR7T3jbQtbPw%7C1738317079%7Cc8627a7557b9ead869e59a8c4e92447519e9527f6fee305dcd911e835c1c9b53',
    'tt_webid': '7466014851694904856',
    'tt_web_version': 'new',
    'is_dev': 'false',
    'is_boe': 'false',
    'Hm_lvt_3e79ab9e4da287b5752d8048743b95e6': '1738317077',
    'Hm_lpvt_3e79ab9e4da287b5752d8048743b95e6': '1738317077',
    'HMACCOUNT': '74E03469813A9187',
    'x-web-secsdk-uid': 'c73b74e3-57c3-4167-ad77-a632078d79d6',
    '_ga': 'GA1.2.812958040.1738317078',
    '_gid': 'GA1.2.1741985904.1738317078',
    's_v_web_id': 'verify_m6kl3tuy_zeEGsEF7_DxlM_4tHq_9mLu_TcMJ9sw2Sm8C',
    'city_name': '%E9%87%8D%E5%BA%86',
    '_ga_YB3EWSDTGF': 'GS1.1.1738317077.1.1.1738317286.60.0.0',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    # 'cookie': 'ttwid=1%7CQyIhjQ4tbKjxsQc_BtLELfe2JMlCStflR7T3jbQtbPw%7C1738317079%7Cc8627a7557b9ead869e59a8c4e92447519e9527f6fee305dcd911e835c1c9b53; tt_webid=7466014851694904856; tt_web_version=new; is_dev=false; is_boe=false; Hm_lvt_3e79ab9e4da287b5752d8048743b95e6=1738317077; Hm_lpvt_3e79ab9e4da287b5752d8048743b95e6=1738317077; HMACCOUNT=74E03469813A9187; x-web-secsdk-uid=c73b74e3-57c3-4167-ad77-a632078d79d6; _ga=GA1.2.812958040.1738317078; _gid=GA1.2.1741985904.1738317078; s_v_web_id=verify_m6kl3tuy_zeEGsEF7_DxlM_4tHq_9mLu_TcMJ9sw2Sm8C; city_name=%E9%87%8D%E5%BA%86; _ga_YB3EWSDTGF=GS1.1.1738317077.1.1.1738317286.60.0.0',
    'origin': 'https://www.dongchedi.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.dongchedi.com/usedcar/x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'x-forwarded-for': '',
}

params = {
    'aid': '1839',
    'app_name': 'auto_web_pc',
}

data = '&sh_city_name=全国&page=3&limit=20'.encode()

response = requests.post(
    'https://www.dongchedi.com/motor/pc/sh/sh_sku_list',
    params=params,
    cookies=cookies,
    headers=headers,
    data=data,
)
#

data = response.json()

# 构建字体
font_dict = util.extract_text_from_font('96fc7b50b772f52.woff2')

# 获取值
sub_titles = jsonpath(data, '$..sub_title')
print(sub_titles)
for title in sub_titles:
    s = ''
    for i in title:
        try:
            s += font_dict[ord(i)]
        except:
            pass
    print(s)
