# """
# 2023-5-30
# """
import ast
import json
import random
import time

import requests
from jsonpath import jsonpath
import pandas as pd
from openpyxl import workbook
import urllib3
from multiprocessing import Pool
from lxml import etree
from selenium import webdriver  # # 驱动浏览器
from selenium.webdriver.common.by import By  # 选择器

urllib3.disable_warnings()
import threading

res = []
import json


# # 提取数据
df = pd.read_excel('上下游企业数据-终.xlsx')
lst = []
for index, rows in df.iterrows():
    lst.append(rows[0])
print(lst)
cookies = [
    'arms_uid=34de0031-5b6f-4567-8a77-b3dd28bc4a41; cna=hFmlHOLVInoCAX1SeRZobwyo; xlly_s=1; account=oauth_k1%3AwnXaaW3blywVOjX0%2F7Po29q2pl7cUdUJ7D3WdtMvC40gk6g%2FK8J9LsBmy59fbsWoi6eImp7ELVr7Z4Y8%2Btd64mu3ahSLWDPpBm%2FGyPnaDfg%3D; deviceid=dad47dd1bf0342e8a5aa558cad972baf; pub_uid=1Tn4R6fToK22KVSaGmegHQ%3D%3D; isg=BImJ5jNBCUBfk_W5UMRE8PbqmLXj1n0IlYmPtCv-TXCvcqmEcyIx2HKjsNZEKhVA; l=fBIgMkbnN1suSeEKBOfwPurza77txIRAguPzaNbMi9fP935H5ihdW1aTkuLMCnGVFsOBR3l39SNMBeYBqQd-nxv9pEcBudMmnmOk-Wf..; tfstk=c4GOBJNeIHxiSLt0T5phursA66LlZPBT0trfMfUOQtTyEo1AizcowZSkurqzXeC..',
    'arms_uid=2fd88250-4668-45cb-aed7-36a2fd83569e; dd_home_locale=zh-cn; arms_uid=39deeb24-6cf8-4e32-86f0-cf22e08be015; l=fB_QzCJeN1Rx5nBEBOfaFurza77OSIRYYuPzaNbMi9fPOI5B5_TfW1asKUL6C3GVF65yR35uBOxyBeYBq3xonxv9pH6aVuMmndLHR35..; isg=BDo6UZE0CswGpoYszHTRK5-Ai2Bc677FyrBKvEQz5k2YN9pxLHsO1QBFh8PrvDZd'
    'arms_uid=5746a23f-dbeb-407f-add1-fae732760556; cna=03+4HPCyY2ICAbfm3/gsLYHN; xlly_s=1; tfstk=cQmCBvakJ6fQK1-lxW9Zca-JB7qPZt54FLPIdI9FqYaB5SMCi3s4GtWuX1rzeR1..; l=fBjL99keN1uZxEzEKOfaFurza77OSIRYjuPzaNbMi9fPOk5p5WgVW1asTTL9C3GVFsWpR3o-P8F6BeYBqIDvUg4tlu3ZIADmnmOk-Wf..; isg=BCQkkUwjHO7NyGiuHNKKNvs09SIWvUgnU_CfTT5FsO-y6cSzZs0Yt1pLrUFxCoB_'
    'cna=hFmlHOLVInoCAX1SeRZobwyo; _m_h5_tk=99f9aafcae78eb8401f5476a30b0b2c9_1685624682713; _m_h5_tk_enc=e369836b33e0c9e163493731537bfef8; xlly_s=1; _samesite_flag_=true; cookie2=1ffc347a3bbe7ced4a287b020177203c; t=7fb76e2e12bf263303ab8b86750d63d6; _tb_token_=31334ee56eee9; sgcookie=E1009Kh2YpYyxGH2ypdmwST0HERhnWZsZ5rS0OO2vqgX9COs%2FVCfxkN5OqHsNgY4iEN3YKRpcYv6J7bCgC0uDSWDJXEWpU385UH6iW4kw98o0rE%3D; unb=2206787696506; uc1=pas=0&cookie21=Vq8l%2BKCLj6Hk37282g%3D%3D&cookie16=U%2BGCWk%2F74Mx5tgzv3dWpnhjPaQ%3D%3D&existShop=false&cookie14=Uoe8j2Fp1KfpPg%3D%3D&cookie15=W5iHLLyFOGW7aA%3D%3D; uc3=nk2=F5RHpC2cIoejhjw%3D&lg2=UIHiLt3xD8xYTw%3D%3D&vt3=F8dCsf50HSE7cq95Idk%3D&id2=UUphzOV5nsYb%2Bf81eg%3D%3D; csg=6188fe50; lgc=tb256721506; cancelledSubSites=empty; cookie17=UUphzOV5nsYb%2Bf81eg%3D%3D; dnk=tb256721506; skt=5905e6b25a0b51b7; existShop=MTY4NTYxNjQ0Ng%3D%3D; uc4=id4=0%40U2grF862PT9uTiwTjVJofx730Mw%2FQeJF&nk4=0%40FY4MthPoY97ivHUhM%2Bj5ABKeA4yUPQ%3D%3D; tracknick=tb256721506; _cc_=U%2BGCWk%2F7og%3D%3D; _l_g_=Ug%3D%3D; sg=663; _nk_=tb256721506; cookie1=WvSbKUmIvCaSCoZwCZArCpjV9oN31apKdqCn1Be9FSM%3D; isg=BODgX_NAkFtulyxQRB9InkcIse6y6cSzFI42n1rxrPuOVYB_AvmUQ7Zn7f1VfnyL; XSRF-TOKEN=e7835175-53dc-48cc-b0a9-0e7d5c772616',
    'arms_uid=f65e07a8-af2d-4ab7-9685-992899c36d0a; cna=496hG0y95AQCAX1RE2enVAIV; xlly_s=1; isg=BKGhnCm3YQlsTs39sAEFBPYVsG27ThVAxR3BgQN2nagHasE8S54lEM-ozJ5sua14; l=fBElJgC7NwsWxsKQBOfaFurza77OSIRYYuPzaNbMi9fPOLCB5pUNW1a17ZT6C3GVF6PpR35uBOxyBeYBqQAonxvOEAexDmHmndLHR35..; tfstk=dYdvruYal0mD7V3tiiHu7citAduotIL2zn8QsGj0C3KJRercCcJDBlLeX1fD5m-96gT9oCvm3dKJ5H3VSmRM27dhRKg_1qCPzMALhKMsC7BysMp41qH1z7C2ZKVGmm595HftxDcntE8VQ1inxpIWuE-4vJMqtXY2u15sxDcnbfsFztcAHb8dVI_a4YpPyEs86ERRlte2lgF_1QFhHOoptBHEjkjdS-g-yRyNhaPUkWB1.'
]


class Spider:
    def __init__(self):
        # 保存数据
        self.ws = workbook.Workbook()
        self.wb = self.ws.active
        self.pc_USE_AGENT = [
            'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3451.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:57.0) Gecko/20100101 Firefox/57.0',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2999.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.70 Safari/537.36',
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.4; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.1.4322; MS-RTC LM 8; InfoPath.2; Tablet PC 2.0)',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36 OPR/55.0.2994.61',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.814.0 Safari/535.1',
            'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/418.9.1 (KHTML, like Gecko) Safari/419.3',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0; Touch; MASMJS)',
            'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1041.0 Safari/535.21',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3451.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:57.0) Gecko/20100101 Firefox/57.0',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2999.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.70 Safari/537.36',
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.4; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.1.4322; MS-RTC LM 8; InfoPath.2; Tablet PC 2.0)',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36 OPR/55.0.2994.61',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.814.0 Safari/535.1',
            'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/418.9.1 (KHTML, like Gecko) Safari/419.3',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0; Touch; MASMJS)',
            'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1041.0 Safari/535.21',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4093.3 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko; compatible; Swurl) Chrome/77.0.3865.120 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4086.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:75.0) Gecko/20100101 Firefox/75.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/91.0.146 Chrome/85.0.4183.146 Safari/537.36',
            'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 VivoBrowser/8.4.72.0 Chrome/62.0.3202.84',
            'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:83.0) Gecko/20100101 Firefox/83.0',
            'Mozilla/5.0 (X11; CrOS x86_64 13505.63.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 OPR/72.0.3815.400',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
        ]
        self.h = {
            'content-type': 'application/json',
            'origin': 'https://www.dingtalk.com',
            'referer': 'https://www.dingtalk.com/',
            'user-agent': random.choice(self.pc_USE_AGENT),
            'cookie': random.choice(cookies)
        }
        # 行政处罚
        self.url6 = 'https://holmes.taobao.com/web/detail/companyDetailCardBatch'
        self.p6 = {"dataModuleIds":[520,463,464,466,467,511,510,514,509,515,697,469,465],"type":"web","pageNo":1,"pageSize":10,"params":[{"key":"onecomp_id","value":"1180716064576480902"}]}
        # 行政处罚
        self.wb = self.ws.active
        self.wb.append(['统一社会信用代码', '决定文书号', '行政处罚种类', '决定机关', '决定日期'])
        self.ws.save('行政处罚.xlsx')

        self.driver = webdriver.Chrome()
        # 数据字段
        self.infomation_zheng = []  # 行政处罚

    # 抓取基本信息
    def base_data(self, k):
        global res
        proxies = random.choice(res)
        url = f'https://www.dingtalk.com/qidian/search/{k}'
        self.driver.get(url)
        id = self.driver.find_element('//div[@class="title-wrapper"]/h2/@id')
        print(id)

        # self.p6["params"][0]['value'] = 1180716055524203958
        #
        # self.parse_xingzheng_data(self.url6, self.p6)
        #
        # # 数据字段
        # self.infomation_zheng.clear()

    # 行政处罚
    def parse_xingzheng_data(self, url, p):
        global res
        proxies = random.choice(res)
        re = requests.post(url=url, headers=self.h, data=json.dumps(p), proxies=proxies).json()
        re2 = re['data'][1]
        try:
            pages = re2['total'] // 10 if re2['total'] % 10 == 0 else re2['total'] // 10 + 1
            company = []
            if pages != 0:
                for page in range(1, pages + 1):
                    p['pageNo'] = page
                    re = requests.post(url=url, headers=self.h, data=json.dumps(p)).json()
                    print(re)
                    re2 = re['data'][1]
                    for i in re2['rows']:
                        result = {}
                        result['企业统一社会信用代码'] = self.infomation_base['统一社会信用代码']
                        result['决定文书号'] = i[1]
                        result['行政处罚种类'] = i[2]
                        result['决定机关'] = i[3]
                        result['决定日期'] = i[4]
                        self.infomation_zheng.append(result)
            else:
                result = {}
                result['企业统一社会信用代码'] = self.infomation_base['统一社会信用代码']
                result['决定文书号'] = '-'
                result['行政处罚种类'] = '-'
                result['决定机关'] = '-'
                result['决定日期'] = '-'
                self.infomation_zheng.append(result)
            self.save_data()
        except:
            pass

    def save_data(self):
        for i in self.infomation_zheng:
            self.wb.append(
                [str(i['企业统一社会信用代码']), i['决定文书号'], i['行政处罚种类'], i['决定机关']
                    , i['决定日期']])
            self.ws.save('企业上下游数据.xlsx')

    def main(self):
        # 打开表格，获取里面的信息
        for k in lst:
            print('当前id: ', k)
            self.base_data(k)
            break


if __name__ == '__main__':
    spider = Spider()
    spider.main()
