import time

from lxml import etree
from DrissionPage import ChromiumPage, ChromiumOptions
import requests
from jsonpath import jsonpath


def save_data(conn, data):
    try:
        with conn.cursor() as cursor:
            insert_query = """
            INSERT INTO goods (goodsName, casIndexNo, goodsErpCode, goodsSpec, goodsStorePrice, goodsShowStorage, purity, molecularWeight, source)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            values = [(item['Name'], item['CAS'], item['Sku'], item['Spec'], item['Price'],
                       item['Storage'], item['Purity'], item['Molecular_weight'], item['Source']) for item in
                      data]

            cursor.executemany(insert_query, values)
            conn.commit()
            print(f"成功插入 {cursor.rowcount} 条记录.")
    except Exception as e:
        print(f"数据库操作失败: {e}")


def get_data(conn, data):
    name = jsonpath(data, '$..data..newGoodsBean..goodsAttributelist..goodsName')
    cas = jsonpath(data, '$..data..newGoodsBean..casNo')
    code = jsonpath(data, '$..data..newGoodsBean..goodsAttributelist..goodsErpCode')
    purtity = jsonpath(data, '$..data..newGoodsBean..goodsAttributelist..specName')
    spec = jsonpath(data, '$..data..newGoodsBean..goodsAttributelist..goodsSpec')
    goodsCostPrice = jsonpath(data, '$..data..newGoodsBean..goodsAttributelist..goodsCostPrice')
    Storage = jsonpath(data, '$..data..newGoodsBean..goodsAttributelist..goodsShowStorage')
    products = []
    print(name , cas , code , purtity , spec , goodsCostPrice , Storage)
    for n, c, s, p, sp, price, sg in zip(name, cas, code, purtity, spec, goodsCostPrice, Storage):
        product = {
            'Name': n,
            'CAS': c,
            'Sku': s.strip(),  # 去除SKU的多余空格
            'Molecular_weight': '',  # 如果有分子量数据可以填充
            'Purity': p,
            'Price': price,
            'Spec': sp,
            'Storage': sg,  # 如果有库存信息可以填充
            'Source': 'https://www.reagent.com.cn'
        }
        print(product)
        products.append(product)

    save_data(conn, products)

def get_resp(name ,page):
    import requests

    cookies = {
        'VERSION': '1',
        'Hm_lvt_09255577aaba19dc63f883f3d627e356': '1733023417,1733113093,1733314288,1733375194',
        'Hm_lpvt_09255577aaba19dc63f883f3d627e356': '1733375194',
        'HMACCOUNT': '74E03469813A9187',
        'urlTagCookie': '0',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        # 'Cookie': 'VERSION=1; Hm_lvt_09255577aaba19dc63f883f3d627e356=1733023417,1733113093,1733314288,1733375194; Hm_lpvt_09255577aaba19dc63f883f3d627e356=1733375194; HMACCOUNT=74E03469813A9187; urlTagCookie=0',
        'Referer': 'https://www.reagent.com.cn/ProductSearch/%E4%B9%99%E9%86%87',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'token': '461d48a5-0019-4335-ba31-53485f838932',
    }
    params = {
        'currentPage': page,
        'isAccurate': '0',
        'isRollup': '0',
        'keywords': name,
        'pageSize': '10',
        'timestringout': int(time.time() * 1000),
    }

    response = requests.get(
        'https://www.reagent.com.cn/reagent-front/goodsApi/getGoodsListNew',
        params=params,
        cookies=cookies,
        headers=headers,
    )
    data = response.json()
    return data


def link1_deep_main(name):
    import db
    conn = db.pool.connection()

    data = get_resp(name , 1)
    print(data)
    get_data(conn, data)
    # 总页数
    total_page = jsonpath(data , '$..data..pageCount')[0]
    print('link1总页数： ' , total_page)
    # 获取数据
    for i in range(2 , total_page + 1):
        try:
            new_data = get_resp(name, i)
            get_data(conn, new_data)
            time.sleep(3)
        except Exception as e:
            print(e)
    conn.close()