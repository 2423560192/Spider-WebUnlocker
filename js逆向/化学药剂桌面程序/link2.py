import re
import time

import requests

from lxml import etree

tt = str(int(time.time()))


def get_price(original_price):
    data = original_price
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': 'mage-banners-cache-storage={}; form_key=RTcxvemoy8lZGpv9; cdn_sec_tc=b7e6491d17332745897593678e97ddba7c06a647f37a8ca735bac0863d; acw_tc=ac11000117332745898568034e010e437c7a1536b3b1fe7ff1c3c51910b032; acw_sc__v2=674fabdd600966bd2f5d32793324a21a52aa8b53; Hm_lvt_8b1cb2df0051d3b34c13154f8e73ac6d=1733150603,1733196591,1733196902,1733274592; HMACCOUNT=74E03469813A9187; mage-cache-storage={}; mage-cache-storage-section-invalidation={}; mage-messages=; recently_viewed_product={}; recently_viewed_product_previous={}; recently_compared_product={}; recently_compared_product_previous={}; product_data_storage={}; form_key=RTcxvemoy8lZGpv9; PHPSESSID=v6bmt8gj7dgbqcbhfn0ckobk4b; mage-cache-sessid=true; private_content_version=b20c69c1af991d18517225e528f661b0; section_data_ids={%22payments%22:1733274598%2C%22company%22:1733274610}; ssxmod_itna=eqRxyWi=GQF8DXDnQGqq7KCT4jODDqFH5n42+PDsqoiDSxGKidDqxBenjeDtGIGFmDeNqfK+243ijYRj04IqMA+gNHDU4i8DCkwpbD4SKGwD0eG+DD4DWUx03DoxGABhx0+8Bn6LIQGRD0YDzqDgD7jVWqDEDG3D0b=QDOYcQqG0DDtDAk0QZqDADAf9DxDlDocGbD6PDYPcITL4VM0=27UxKi=DjqGgDBLeDKecRQBhxoXg0aHHahjx5eGuDG=PwwLqx0p99LU0CceoWOxoGBvPBx+e7xwxBhDoeEwu2Avt0Gv5BOZdKB1oG5IMCaB5KeWh0GFiDD==; ssxmod_itna2=eqRxyWi=GQF8DXDnQGqq7KCT4jODDqFH5n424ikEqsDl=mQDjRRuC4Ihmd2C2QqUQlquQQ0fZup2t5Otug4Hb/x8OcicC6BBT8KvIZSDfFHbLSW81dvzOHEi1F9A9eCvxD5nzxpntDySfDM3jmb7ELS8=XCTE5=SN4anrxVw63kT0RFCidEo2Kyej3qnutaSNK=6NK1hRWoPb7ZLF9b3L8vayLWwu116b8m6c+5ZueT=0QTpBG1UXTVO7=6z3RfUBoE=MAseHXXc8QE/M22I8UxklAHySAT5H8YkCme5sfXHVWD7jVD08DiQiYD=; tfstk=fG0nLaZVfDrBU-jgshzB4F6U0k-TR6a7QYQ8ezeybRy1p9QKazAoexu-9bhFrcDrCkeF24HTEA2svWrUYFSaGRHRyXHROcMxgw3pAzQuRzayHKLvkXhQPzSOQuFadfl_aFKQRhGIOz1614-8WX6o7p6xUzkz7lPLizWUYWRgbSFzzwrP8GWaCRyzzJrF_RP7TTyzL7Ri_RNzz8kdsaymzVgwpnE5DlzLCVV3bhhUQYDWwWqHoXeGzKugtTyqTRbPrJhrsGci9pbj6yGZnSHp7wDmGVMg_x8kIzMs4YPoQE68RmHIllc60NlT-Rr4gVRPu83nXjygo_8Esy2302EeoIMqsboYjVd2ly4UL0UIwsvKs2DKOVcRaGz3Jcqm-r8fL8nti4VoPLTinjgsI5k2rpSP3GS42n_7_Q3NVgZU152AAZZBGml6l4OMsitQY5NpHCAGVgZU152vsCjfdkP_9KC..; Hm_lpvt_8b1cb2df0051d3b34c13154f8e73ac6d=1733274616',
        'origin': 'https://www.aladdin-e.com',
        'priority': 'u=1, i',
        'referer': 'https://www.aladdin-e.com/zh_cn/e111964.html',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    response = requests.post('https://www.aladdin-e.com/zh_cn/catalogb/ajax/price/', cookies=cookies, headers=headers,
                             data=data)

    price_data = response.json()
    # 正则表达式匹配价格
    price_pattern = re.compile(r'¥([\d\.]+)')

    # 提取价格并存储在字典中
    prices = {}
    for key, html in price_data.items():
        match = price_pattern.search(html)
        if match:
            prices[key] = float(match.group(1))

    # 打印结果
    print(prices)
    return prices



def get_data(text):
    lxml = etree.HTML(text)
    try:
        name = lxml.xpath("//*[@id='maincontent']/div[2]/div/div[2]/div[1]/h1/span/text()")[0]  # 名字
        CAS = lxml.xpath("//*[@id='maincontent']/div[2]/div/div[2]/div[5]/div/ul/li[1]/span/a/text()")[0]  # CAS
        molecular_weight = lxml.xpath('//*[@id="maincontent"]/div[2]/div/div[2]/div[5]/div/ul/li[3]/text()')[0]  # 分子量
        purity = lxml.xpath('//*[@id="maincontent"]/div[2]/div/div[2]/div[5]/ul/li/text()')[0]  # 纯度
    except IndexError:
        print("某些数据未找到！")
        return

    products = []
    rows = lxml.xpath('//table[@id="super-product-table"]/tbody/tr')
    price_lst = []
    for row in rows:
        sku = row.xpath('./td[@data-th="货号 (SKU) "]/text()')[0].strip()
        Spec = row.xpath('./td[@data-th="包装规格"]/text()')[0].strip()
        Storage = row.xpath('./td[contains(@class, "ajaxStock_")]/text()')[0].strip()
        original_price = row.xpath('./td[contains(@class, "ajaxPrice")]/@id')[0].strip()
        price_lst.append(original_price)
        dic = {
            'Name': name,
            'CAS': CAS,
            'Sku': sku,
            'Brand': '',

            'Molecular_weight': molecular_weight.strip(),
            'Purity': purity,
            'Price': '',
            'Spec': Spec,

            'Storage': Storage,
            'Source': ''
        }
        products.append(dic)
        print(dic)
    data = {

    }
    for i in price_lst:
        data[f"{i}"] = i
    print(data)
    price_data = get_price(data)

    for price , product in zip(price_data.values() , products):
        product['Price'] = price
        print(product)


if __name__ == '__main__':
    cookies = {
        'mage-banners-cache-storage': '{}',
        'form_key': 'RTcxvemoy8lZGpv9',
        'cdn_sec_tc': 'b7e6491d17332745897593678e97ddba7c06a647f37a8ca735bac0863d',
        'acw_tc': 'ac11000117332745898568034e010e437c7a1536b3b1fe7ff1c3c51910b032',
        'acw_sc__v2': '674fabdd600966bd2f5d32793324a21a52aa8b53',
        'Hm_lvt_8b1cb2df0051d3b34c13154f8e73ac6d': '1733150603,1733196591,1733196902,1733274592',
        'HMACCOUNT': '74E03469813A9187',
        'mage-cache-storage': '{}',
        'mage-cache-storage-section-invalidation': '{}',
        'mage-messages': '',
        'recently_viewed_product': '{}',
        'recently_viewed_product_previous': '{}',
        'recently_compared_product': '{}',
        'recently_compared_product_previous': '{}',
        'product_data_storage': '{}',
        'form_key': 'RTcxvemoy8lZGpv9',
        'PHPSESSID': 'v6bmt8gj7dgbqcbhfn0ckobk4b',
        'mage-cache-sessid': 'true',
        'Hm_lpvt_8b1cb2df0051d3b34c13154f8e73ac6d': '1733274607',
        'private_content_version': 'b20c69c1af991d18517225e528f661b0',
        'tfstk': 'f7uiLKqPAcr638j3tHz60e6a4l-L51abLxQYHre2YJyCBOQtgrAmHYux6jhNoDDqdleNDqHLnv2IX5rabeSUNJHAkfHA1DM-aN39frQ05ra2eLLJyfh_lrSdLoFUCXlQgeK_5HGs1r1BOq-YJf6m8d_-3rk48kPTMrWab5R3Y7F4uNrV7MWUdJy4uRrNTJPb_ty4QSRnTJN4u-kNnZyou2geB3Ef2kz452VgbHhaLZPI-5qgUfuGuZ57sl2r_JJ5pRb4YjZmls_0QfoSh7kNQLEsgDD3srYdbzln0YVI7UBgOchEwJllGZGaS00u7cvCAPHi8yuZqs7qtP2_mWqCIp2r5Xu78kLyZXuIBfgnMs849YeE1VzDzQag7Rz3OqpC7-mE0VE_lOJ8fjonK54P4CSF4oK5lWRx8isbbWN3eG_7fQirOUgXtBjWflPQ6LdHtisbbWN3eBAhVOZaO5pR.',
        'section_data_ids': '{%22payments%22:1733274598%2C%22company%22:1733274610}',
        'ssxmod_itna': 'eqRxyWi=GQF8DXDnQGqq7KCT4jODDqFHvPDtdFDl=mDxA5D8D6DQeGTiubIGidGFmDmoqfK+24xGjY4+cRvqMASENHDU4i8DCkwpbD4SKGwD0eG+DD4DWUx03DoxGABhx0+8Bn6LIQGRD0YDzqDgD7jVWqDEDG3D0b=QDOYcQqG0DDtDAk0QZqDADAf9DxDlDocGbD6PDYPcITL4VM0=27UxKi=DjqGgDBLeDKecRQBhxoXg0aHHahjx5eGuDG=PwwLqx0p99LU0CZ5oWOxoG0vPQx+e7xwxQhDoeEwu2Gvt00m5QOZdKB1oDPbBCa05KeWh0GFiDD==',
        'ssxmod_itna2': 'eqRxyWi=GQF8DXDnQGqq7KCT4jODDqFHvPDtdD6ptlx0y4YY03bb7c7IeUnD6j79GzuD3mA2PY5WqohwV4tQSQiYp+eyn+7V2CL2h/7K/SQpwdIBjLnExL1gryBWbaQOjUM091iMC=5O2gIe4f9Q7nFzjZqhqtHi/GwaWxArF=OrIQT4RoImS2YzPPvHrKY7s67rKb3IjIK8BBwxoKMf/xaEA/Fj+RMLxpoOgt8kKSqs1nImLx3Xev8kl=KTQsf0y8mNU9CL5SLU8q90sHF9V9vu==zjNtZ1BUdjEMUMEkNwH9arLfNBUm2l5ZSvjR4Z7+nnm+m5DTTpYAfb7+bxDKu3D7=DYKYeD===',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        # 'cookie': 'mage-banners-cache-storage={}; form_key=RTcxvemoy8lZGpv9; cdn_sec_tc=b7e6491d17332745897593678e97ddba7c06a647f37a8ca735bac0863d; acw_tc=ac11000117332745898568034e010e437c7a1536b3b1fe7ff1c3c51910b032; acw_sc__v2=674fabdd600966bd2f5d32793324a21a52aa8b53; Hm_lvt_8b1cb2df0051d3b34c13154f8e73ac6d=1733150603,1733196591,1733196902,1733274592; HMACCOUNT=74E03469813A9187; mage-cache-storage={}; mage-cache-storage-section-invalidation={}; mage-messages=; recently_viewed_product={}; recently_viewed_product_previous={}; recently_compared_product={}; recently_compared_product_previous={}; product_data_storage={}; form_key=RTcxvemoy8lZGpv9; PHPSESSID=v6bmt8gj7dgbqcbhfn0ckobk4b; mage-cache-sessid=true; Hm_lpvt_8b1cb2df0051d3b34c13154f8e73ac6d=1733274607; private_content_version=b20c69c1af991d18517225e528f661b0; tfstk=f7uiLKqPAcr638j3tHz60e6a4l-L51abLxQYHre2YJyCBOQtgrAmHYux6jhNoDDqdleNDqHLnv2IX5rabeSUNJHAkfHA1DM-aN39frQ05ra2eLLJyfh_lrSdLoFUCXlQgeK_5HGs1r1BOq-YJf6m8d_-3rk48kPTMrWab5R3Y7F4uNrV7MWUdJy4uRrNTJPb_ty4QSRnTJN4u-kNnZyou2geB3Ef2kz452VgbHhaLZPI-5qgUfuGuZ57sl2r_JJ5pRb4YjZmls_0QfoSh7kNQLEsgDD3srYdbzln0YVI7UBgOchEwJllGZGaS00u7cvCAPHi8yuZqs7qtP2_mWqCIp2r5Xu78kLyZXuIBfgnMs849YeE1VzDzQag7Rz3OqpC7-mE0VE_lOJ8fjonK54P4CSF4oK5lWRx8isbbWN3eG_7fQirOUgXtBjWflPQ6LdHtisbbWN3eBAhVOZaO5pR.; section_data_ids={%22payments%22:1733274598%2C%22company%22:1733274610}; ssxmod_itna=eqRxyWi=GQF8DXDnQGqq7KCT4jODDqFHvPDtdFDl=mDxA5D8D6DQeGTiubIGidGFmDmoqfK+24xGjY4+cRvqMASENHDU4i8DCkwpbD4SKGwD0eG+DD4DWUx03DoxGABhx0+8Bn6LIQGRD0YDzqDgD7jVWqDEDG3D0b=QDOYcQqG0DDtDAk0QZqDADAf9DxDlDocGbD6PDYPcITL4VM0=27UxKi=DjqGgDBLeDKecRQBhxoXg0aHHahjx5eGuDG=PwwLqx0p99LU0CZ5oWOxoG0vPQx+e7xwxQhDoeEwu2Gvt00m5QOZdKB1oDPbBCa05KeWh0GFiDD==; ssxmod_itna2=eqRxyWi=GQF8DXDnQGqq7KCT4jODDqFHvPDtdD6ptlx0y4YY03bb7c7IeUnD6j79GzuD3mA2PY5WqohwV4tQSQiYp+eyn+7V2CL2h/7K/SQpwdIBjLnExL1gryBWbaQOjUM091iMC=5O2gIe4f9Q7nFzjZqhqtHi/GwaWxArF=OrIQT4RoImS2YzPPvHrKY7s67rKb3IjIK8BBwxoKMf/xaEA/Fj+RMLxpoOgt8kKSqs1nImLx3Xev8kl=KTQsf0y8mNU9CL5SLU8q90sHF9V9vu==zjNtZ1BUdjEMUMEkNwH9arLfNBUm2l5ZSvjR4Z7+nnm+m5DTTpYAfb7+bxDKu3D7=DYKYeD===',
        'priority': 'u=0, i',
        'referer': 'https://www.aladdin-e.com/zh_cn/catalogsearch/result/index/?q=%E4%B9%99%E9%86%87&product_list_mode=grid',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    url = 'https://www.aladdin-e.com/zh_cn/e111964.html'

    text = requests.get(url, cookies=cookies, headers=headers).text
    get_data(text)
    time.sleep(3)
