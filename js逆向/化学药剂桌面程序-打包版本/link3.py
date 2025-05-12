import random
import traceback

from lxml import etree
from DrissionPage import ChromiumPage, ChromiumOptions
import requests
from jsonpath import jsonpath


def get_sku_info(uid, cookies):
    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        # 'cookie': 'language=zh; country=CN; GUID=111b2126-ac20-4740-af2c-88609317deb6|NULL|1732257972194; isBlueErpIntegrationEnabled=true; kndctr_C8A44C9154C09E3B0A4C98A5_AdobeOrg_identity=CiY1MDk1MzYyNzQ4NjcyMjU4NzI1MDU0MDk5NjU1MzE1NTA4MDIzOFIRCI37_JS1MhgBKgRKUE4zMAHwAY37_JS1Mg==; BVBRANDID=a943ca91-f3b3-467d-a151-662d5be4ed08; accessToken=d4337b21-ad4f-11ef-9262-635cba2e3c0b; dtCookie=v_4_srv_4_sn_6CF1BE01B018EE7EBE9EEF601BF773F9_perc_100000_ol_0_mul_1_app-3Afe65591685aff23e_1; bm_mi=CC4F18608B435E4FAA68338DE5A6C4A5~YAAQFQWK3tYf312TAQAA3xudlBqeD6QUa2XVViF1jbG5/clHRQUkBwllLpppga2Z9rBZK11p9FGyMPL33jq4yELa5mFeDpTPzd0ekEUeJOiSv0jHpTS0L0DDaKVT4RDsAKUl08srtE2ive1VLqfJm+XHwZH8wvnkD8MEyY6ymE/nq/+Np+uWddghYQDBvJ6pJuTweB56tytFqrprmOQMbxKMtqE74mBAkU4WMBajfZTErWipsUQ/D3W/GdQkFa9PHuAtjeDIFt1FpWHAWBy6FmT39CAKAVlTDAWPTrWD94Gm8PjD3gZlx0rmJsFIooGKFYhELpq04acbd2wolxa7wn+IKidL4CIVb6qYueUMQxZM1g==~1; rxVisitor=1733365144112PA3RILNSU23O731EFBIPL6KKMG3GHTTM; userErpType=ANONYMOUS; Hm_lvt_60b4048dfc756a0d9fe376b76ef23198=1733144958,1733216026,1733320218,1733365146; HMACCOUNT=74E03469813A9187; ak_bmsc=FFA2994483E8549FD2472F87E7638232~000000000000000000000000000000~YAAQFQWK3gwg312TAQAABSedlBo3N1WbKXz7d9ngZvqF12LqqTgWfnCRydsIrgiTS92axVLydy+76v3MR2RthFc1E5+8qaV12IK7/pEoTH7GvJ9hVeqxcdQ+pK1+XdLHTG8gj0lTha/k8s52U05BkKSVc25H1iK+KoC0bOBvSUNcC+eUS6TO+TOWmf7laB6El//FTXtOTibzuD3KHhjR0W57IGSE++CPzWyPqmgsuKc2z6p+qccLKn5ExWYOVM7nFr8zxbs9JgnnMpKBvPhLlrV4Kb5QtrkGo0/ErujDm+D40Lvneo/FA0IsUDvLX/LCQDCL10MhBAKI5x9I/UoiuuA5fyriVbW6QLq4zOZnl460AZb7t0WH6QJWyZtP+rZ0yuqZlYZBHkxui+rib8AHB0DN+gV3kXL9Njx+2B3usepSYZUjocspWTinG4NphMrd0CzAdC9T6S7avMjLxZx2xGR+8asBaf8Ry2EZ4zGAXUha+DKobOvhGL7IJxaLHaJbhc6PYIUEspc3r0qhTLlzCFkzlCyHl+yt9JOoDhJASMcV3ZKof8H4yiqDnrQP2ndPgPfYjqtlfATdwyNuO9UtCisPdUa/q8iZaGiiJMVrXOGjAitfg+AiiRPMUIm5Pg==; BVBRANDSID=41ea4440-8e7f-4ed4-b669-23542a42f6a6; Hm_lpvt_60b4048dfc756a0d9fe376b76ef23198=1733368857; bm_sv=8219AF96A3D44B811DDFC7A7C80CC1DD~YAAQVAWK3odTQoSTAQAA5tHVlBrlJ+gqP0S6rzU5MAotA98wJoHqBfGDvE5WwB5pMnVZLEKzac8H5QvJ6sQmCsBwFoq6BrW3y60qIMC9DB5XiRqFV3gUBvPVo8KWWydW7TRTcAr9ZR+2kDYn83ob9PttK+XJ2dZzjNF7jz9eylGap9EqvpbNMsafCnDZ9/p8tyXKnvldd7mjpxb/m7zJXEPakyQwa6/kclCR6fhtfuXbwsZG7kN1KXzYRnAlM2SXWihwSca6~1; rxvt=1733370663771|1733368265153; dtPC=4$568855908_398h12vCFDQMLNVNCOKAVRJKHCIFQCKARUMRMCI-0e0',
        'origin': 'https://www.sigmaaldrich.cn',
        'priority': 'u=1, i',
        'referer': 'https://www.sigmaaldrich.cn/CN/zh/search/%E4%B9%99%E9%86%87?focus=products&page=1&perpage=30&sort=relevance&term=%E4%B9%99%E9%86%87&type=product',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'x-dtpc': '4$568855908_398h12vCFDQMLNVNCOKAVRJKHCIFQCKARUMRMCI-0e0',
        'x-gql-access-token': 'd4337b21-ad4f-11ef-9262-635cba2e3c0b',
        'x-gql-blue-erp-enabled': 'true',
        'x-gql-country': 'CN',
        'x-gql-language': 'zh',
        'x-gql-operation-name': 'PricingAndAvailability',
        'x-gql-user-erp-type': 'ANONYMOUS',
    }

    params = {
        'operation': 'PricingAndAvailability',
    }

    json_data = {
        'operationName': 'PricingAndAvailability',
        'variables': {
            'displaySDS': False,
            'productNumber': uid,
            'quantity': 1,
            'catalogType': 'sial',
            'orgId': None,
            'checkForPb': False,
            'dealerId': '',
            'checkBuyNow': True,
            'productKey': uid.replace('.', '') if '.' in uid else uid,
            'cachedPriceOnly': False,
        },
        'query': 'query PricingAndAvailability($productNumber: String!, $brand: String, $quantity: Int!, $catalogType: CatalogType, $checkForPb: Boolean, $orgId: String, $materialIds: [String!], $displaySDS: Boolean = false, $dealerId: String, $checkBuyNow: Boolean, $productKey: String, $erp_type: [String!], $cachedPriceOnly: Boolean) {\n  getPricingForProduct(input: {productNumber: $productNumber, brand: $brand, quantity: $quantity, catalogType: $catalogType, checkForPb: $checkForPb, orgId: $orgId, materialIds: $materialIds, dealerId: $dealerId, checkBuyNow: $checkBuyNow, productKey: $productKey, erp_type: $erp_type, cachedPriceOnly: $cachedPriceOnly}) {\n    ...ProductPricingDetail\n    __typename\n  }\n}\n\nfragment ProductPricingDetail on ProductPricing {\n  dealerId\n  productNumber\n  country\n  materialPricing {\n    ...ValidMaterialPricingDetail\n    __typename\n  }\n  discontinuedPricingInfo {\n    ...DiscontinuedMaterialPricingDetail\n    __typename\n  }\n  dchainMessage\n  productInfo {\n    ...ProductInfoMessageDetail\n    __typename\n  }\n  __typename\n}\n\nfragment ValidMaterialPricingDetail on ValidMaterialPricing {\n  brand\n  type\n  currency\n  dealerId\n  listPriceCurrency\n  listPrice\n  shipsToday\n  freeFreight\n  catalogType\n  marketplaceOfferId\n  marketplaceSellerId\n  materialDescription\n  materialNumber\n  materialId\n  netPrice\n  packageSize\n  packageType\n  price\n  isBuyNow\n  product\n  productGroupSBU\n  productHierarchy\n  quantity\n  isPBAvailable\n  vendorSKU\n  isBlockedProduct\n  hidePriceMessageKey\n  expirationDate\n  availableQtyInStock\n  availabilities {\n    ...Availabilities\n    __typename\n  }\n  additionalInfo {\n    ...AdditionalInfo\n    __typename\n  }\n  promotionalMessage {\n    ...PromotionalMessage\n    __typename\n  }\n  ... @include(if: $displaySDS) {\n    sdsLanguages\n    __typename\n  }\n  minOrderQuantity\n  __typename\n}\n\nfragment Availabilities on MaterialAvailability {\n  date\n  key\n  plantLoc\n  quantity\n  displayFromLink\n  displayInquireLink\n  messageType\n  contactInfo {\n    contactPhone\n    contactEmail\n    __typename\n  }\n  availabilityOverwriteMessage {\n    messageKey\n    messageValue\n    messageVariable1\n    messageVariable2\n    messageVariable3\n    __typename\n  }\n  supplementaryMessage {\n    messageKey\n    messageValue\n    messageVariable1\n    messageVariable2\n    messageVariable3\n    __typename\n  }\n  __typename\n}\n\nfragment AdditionalInfo on CartAdditionalInfo {\n  carrierRestriction\n  unNumber\n  tariff\n  casNumber\n  jfcCode\n  pdcCode\n  __typename\n}\n\nfragment PromotionalMessage on PromotionalMessage {\n  messageKey\n  messageValue\n  messageVariable1\n  messageVariable2\n  messageVariable3\n  __typename\n}\n\nfragment DiscontinuedMaterialPricingDetail on DiscontinuedMaterialPricing {\n  errorMsg\n  paramList\n  hideReplacementProductLink\n  displaySimilarProductLabel\n  hideTechnicalServiceLink\n  replacementProducts {\n    ...ReplacementProductDetail\n    __typename\n  }\n  alternateMaterials {\n    ...AlternateMaterialDetail\n    __typename\n  }\n  __typename\n}\n\nfragment ReplacementProductDetail on Product {\n  productNumber\n  name\n  description\n  sdsLanguages\n  images {\n    mediumUrl\n    altText\n    __typename\n  }\n  brand {\n    key\n    erpKey\n    name\n    logo {\n      smallUrl\n      altText\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment AlternateMaterialDetail on Material {\n  number\n  __typename\n}\n\nfragment ProductInfoMessageDetail on ProductInfoMessage {\n  productNumber\n  messageType\n  message\n  __typename\n}\n',
    }

    response = requests.post('https://www.sigmaaldrich.cn/api', params=params, cookies=cookies, headers=headers,
                             json=json_data)

    resp_data = response.json()

    try:
        # 获取数据
        skus = jsonpath(resp_data, '$..data..materialPricing..materialNumber')
        specs = jsonpath(resp_data, '$..data..materialPricing..packageSize')
        # storages = jsonpath(resp_data, '$..data..materialPricing..shipsToday')  # 是否今日发货
        prices = jsonpath(resp_data, '$..data..materialPricing..listPrice')  # 价格

        lst = []

        for sku, spec, price in zip(skus, specs, prices):
            dic = {
                'Name': '',
                'CAS': '',
                'Sku': sku.strip(),
                'Brand': '',
                'Molecular_weight': '',
                'Purity': '',
                'Price': price,
                'Spec': spec,
                'Storage': '',
                'Source': 'https://www.sigmaaldrich.cn/'
            }
            lst.append(dic)
        return lst
    except:
        return None


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


def get_data(conn, cp, url):
    # 请求页面
    try:
        cp.get(url, retry=3, interval=2, timeout=15)
    except:
        print('link3爬取错误')
        return


    cookies_list = cp.cookies()
    # 转换为 requests 使用的 cookie 格式
    cookies = {cookie['name']: cookie['value'] for cookie in cookies_list}

    print(cookies_list)
    # 点击所有的展开
    shows = cp.eles('tag:button@data-testid=show-more')

    for show in shows:
        show.click()

    # 获取页面源代码
    page_source = cp.html

    # 使用 lxml 解析页面源代码
    tree = etree.HTML(page_source)

    # 获取每一块信息
    infos = tree.xpath('//div[@data-testid="srp-substance-group"]')

    end_lst = []

    for info in infos:
        # 获取基础数据
        name = info.xpath('.//h2[@id="substance-name"]//text()')[0] if info.xpath(
            './/h2[@id="substance-name"]//text()') else ''

        # 获取 CAS 和分子量数据
        csa = "".join(map(str , info.xpath('./div[1]/div[2]//dl/dd[1]//text()'))) if info.xpath(
            './div[1]/div[2]//dl/dd[1]//text()') else ''


        molecular_weight = info.xpath('.//div[2]/div[2]/dl/dd[2]//text()')[0] if info.xpath(
            './/div[2]/div[2]/dl/dd[2]//text()') else ''

        # 打印基础数据
        # print('基础数据:')
        # print(f'名称: {name}')
        # print(f'CAS: {csa}')
        # print(f'分子量: {molecular_weight}')

        # 获取skus
        skus = info.xpath('.//ul//li')

        for i in skus:

            try:
                purity = "".join(map(str , i.xpath('.//p//text()')))
            except:
                purity = ''

            try:
                sku = i.xpath('./h3//text()')[0]
                # 请求sku
                lst = get_sku_info(sku, cookies)
                if lst:
                    for j in lst:
                        j['Name'] = name
                        j['CAS'] = csa
                        j['Molecular_weight'] = molecular_weight
                        j['Purity'] = purity
                        end_lst.append(j)
                        print(j)
            except:
                pass




    save_data(conn, end_lst)


def link3_main(name):
    import db
    conn = db.pool.connection()

    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
    ]

    headers = random.choice(USER_AGENTS)

    co = ChromiumOptions()
    co.auto_port()
    co.incognito(True)
    co.set_argument("--disable-gpu")
    co.set_user_agent(headers)
    co.headless(True)

    cp = ChromiumPage(co)


    url = f'https://www.sigmaaldrich.cn/CN/zh/search/{name}?focus=products&page=1&perpage=30&sort=relevance&term={name}&type=product'
    try:
        # 获取数据
        get_data(conn, cp, url)
    except Exception as e:
        print(e)
        traceback.print_exc()
        print('link3出错....')
    finally:
        conn.close()
        cp.close()