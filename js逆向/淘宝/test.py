import datetime
import json
import urllib.parse

import jsonpath
import requests
from jsonpath_ng import parse

headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "referer": "https://detail.m.tmall.com/",
    "sec-fetch-dest": "script",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
}
cookies = {
    "_samesite_flag_": "true",
    "cookie2": "175d2764148381a1480a760aca368ce0",
    "t": "52362914eedb2269b995a5e9344af16f",
    "_tb_token_": "e17351b38b196",
    "sn": "",
    "lgc": "tb256721506",
    "cancelledSubSites": "empty",
    "dnk": "tb256721506",
    "tracknick": "tb256721506",
    "_cc_": "UtASsssmfA%3D%3D",
    "wk_cookie2": "12dd50cb3a72f253d3b9664d2219ec6c",
    "wk_unb": "UUphzOV5nsYb%2Bf81eg%3D%3D",
    "cna": "KAJsH9kP0n4CAXuT+UD32lk5",
    "aui": "2206787696506",
    "sca": "edc108a1",
    "thw": "cn",
    "xlly_s": "1",
    "mtop_partitioned_detect": "1",
    "_m_h5_tk": "d5bbfd9f6d9b6578c1dbf5304670ad59_1747210780134",
    "_m_h5_tk_enc": "b8a6c497295284991a7b584f87da1384",
    "3PcFlag": "1747204242550",
    "unb": "2206787696506",
    "uc1": "cookie16=UIHiLt3xCS3yM2h4eKHS9lpEOw%3D%3D&existShop=false&pas=0&cookie15=Vq8l%2BKCLz3%2F65A%3D%3D&cookie21=W5iHLLyFeDV1cfTOQA%3D%3D&cookie14=UoYajLe8Vz4NeQ%3D%3D",
    "uc3": "vt3=F8dD2EXfIMKUPUT%2BOP4%3D&lg2=WqG3DMC9VAQiUQ%3D%3D&id2=UUphzOV5nsYb%2Bf81eg%3D%3D&nk2=F5RHpC2cIoejhjw%3D",
    "csg": "208cd87c",
    "cookie17": "UUphzOV5nsYb%2Bf81eg%3D%3D",
    "skt": "5ba1cbdf2feda41b",
    "existShop": "MTc0NzIwNDI0OA%3D%3D",
    "uc4": "nk4=0%40FY4MthPoY97ivHUhM%2Bk6Wu1Y2bhlYA%3D%3D&id4=0%40U2grF862PT9uTiwTjVJofiu3WzLSncoZ",
    "_l_g_": "Ug%3D%3D",
    "sg": "663",
    "_nk_": "tb256721506",
    "cookie1": "WvSbKUmIvCaSCoZwCZArCpjV9oN31apKdqCn1Be9FSM%3D",
    "sgcookie": "E100Y85BdKIpi4mkavfla9IZDWqK5HaBgGOM4g0yQ2OCHLns8R6n63jFd6DZNpDV1vTTdrHZyctP1lvPeR4EEd0cfq3wg%2B%2FR%2BassUm%2B%2FhsYfdV0%3D",
    "tfstk": "gyJrQvieCYHy4p7RZK6U_OF9cWXJt9usUp_CxHxhVablPHjhLEYI2atnyeJFoHdS26g8Yup27JwSybK3L96n5VMsC3K5p90_txmweuICxwquRwx0o9sEUqGbl3KRp9qb-fOD2k7O2S1hxwmVnMSP-9VlximVYG7hKaf3oSjGo9XhZJ4cmGSQK7buEm-ckMXh-efo0sbAxxMHqH2Vf_mIjlQ2w2osSw-luJ2HEvCA7-bRDgvVk_7GiNwhcKSPaNxyQye5nivX311bAfBDXITl0OkbZOx2tFRMJfNAUHAkJs8-kS7XiLKh-sZ3Qn-wqCXDdDqOgEjFs9f4xJxVeZYeFODguidDVBvJzkyh2L91TNCqxJCCnd1MsUrKXnXlxeC9dVeRrHx9BC6Zh7XM0BYwTg8QJiVzVpdz-W5lDi7s0m-_VbF1bg9PhWFdiOIV50s79WClDi7s0mPL9sjO0Ni5V",
    "isg": "BCgow-cX1O8lUPaqhm7nZb8m-RY6UYxby6zjNuJaQKO0Pc-njGKt6ik7NdXNDUQz"
}
url = "https://h5api.m.tmall.com/h5/mtop.tmall.detail.couponpage.newcouponpage/1.0/"

data = "{\"itemId\":\"879233717098\",\"promotionFloatingData\":\"{\\\"detailPromotionTimeDO\\\":{\\\"promotionType\\\":\\\"NLORMAL\\\"},\\\"calculateResult\\\":{\\\"quanHouPrice\\\":\\\"258\\\",\\\"discount\\\":\\\"21100\\\",\\\"skuId\\\":\\\"5721422685294\\\",\\\"usedPromotions\\\":[{\\\"promotionType\\\":\\\"501\\\",\\\"promotionUniqueId\\\":\\\"733cd29472b74de8accc603f7ddd6f18\\\",\\\"discount\\\":\\\"11000\\\"}]},\\\"promotionText\\\":\\\"新品促销￥368\\\",\\\"skuId\\\":\\\"5721422685294\\\",\\\"skuMoney\\\":{\\\"skuId\\\":\\\"5721422685294\\\",\\\"cent\\\":\\\"36800\\\"},\\\"buyEnable\\\":\\\"true\\\"}\"}"

params = {
    "jsv": "2.7.4",
    "appKey": "12574478",
    "t": "1747202183197",
    "sign": "00f6f43f9f8b59e721989c6407d994e7",
    "api": "mtop.tmall.detail.couponpage.newcouponpage",
    "v": "1.0",
    "ttid": "202012@taobao_h5_9.17.0",
    "type": "json",
    "dataType": "json",
    "timeout": "8000",
    "callback": "mtopjsonp7",
    "data": data
}

response = requests.get(url, headers=headers, cookies=cookies, params=params)

data = response.text
print(data)

# 工具函数：时间戳转日期
