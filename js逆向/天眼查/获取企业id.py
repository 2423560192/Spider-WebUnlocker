import json
import time

import requests
from lxml import etree
import re
from jsonpath import jsonpath

headers = {
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    # 'Cookie': 'TYCID=a204216008d511ee8872f36dec3eac0f; HWWAFSESID=089d922fd1cab19fc27; HWWAFSESTIME=1693801249028; csrfToken=Yjg9uZClFRSuHunctdETeNbd; jsid=SEO-BAIDU-ALL-SY-000001; bannerFlag=true; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1693801244; ssuid=4400449175; _ga=GA1.2.1939361491.1693801316; _gid=GA1.2.2047503171.1693801316; bdHomeCount=1; RTYCID=010ea12b1b084a939033c6296ea18583; searchSessionId=1693805211.83731828; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22264440066%22%2C%22first_id%22%3A%22188adc2ee8240a-0d2b437e7d6fbd8-26031d51-2073600-188adc2ee831159%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTg4YWRjMmVlODI0MGEtMGQyYjQzN2U3ZDZmYmQ4LTI2MDMxZDUxLTIwNzM2MDAtMTg4YWRjMmVlODMxMTU5IiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiMjY0NDQwMDY2In0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22264440066%22%7D%2C%22%24device_id%22%3A%22188adc2ee8240a-0d2b437e7d6fbd8-26031d51-2073600-188adc2ee831159%22%7D; tyc-user-info=%7B%22state%22%3A%223%22%2C%22vipManager%22%3A%220%22%2C%22mobile%22%3A%2215556999018%22%2C%22isExpired%22%3A%220%22%7D; tyc-user-info-save-time=1693805497338; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTU1Njk5OTAxOCIsImlhdCI6MTY5MzgwNTUwNCwiZXhwIjoxNjk2Mzk3NTA0fQ.WnzNJLAj0WOykxPYYqjAYRlDZQynhPBRQ2fnD3AkZfgqqO_YGaZzkSM1tk0-OmO-om-X7LjcrpouWaWh9mcsiw; cid=2321517909; ss_cidf=1; _gat_gtag_UA_123487620_1=1; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1693805906',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}


# 获取公司url
def get_company_url():
    url = 'https://www.tianyancha.com/advance/search/result'
    data = {
        'xyz': 'Yjg9uZClFRSuHunctdETeNbd',
        'establishTimeRangeSet': '1599148800000, 1693756800000',
        'pageNum': '249',
        'pageSize': '20',
        'resultTagList': '成立时间：2020 - 09 - 04 - 2023 - 09 - 04'
    }
    resp = requests.post(url, data=data, headers=headers)
    html = resp.text
    print(html)
    lxml = etree.HTML(html)
    company_links = lxml.xpath('//div[@class="header"]/a/@href')
    return company_links


# 获取公司id
def get_company_id(url):
    resp = requests.get(url, headers=headers)
    html = resp.text

    company_id = re.findall('<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html)[0]
    company_id = json.loads(company_id)
    print(company_id)
    comp_id = jsonpath(company_id, '$..graphId')[0]
    return comp_id


# 获取自身风险的所有信息
def get_company_content_id(id):
    url = 'https://www.tianyancha.com/risk/detail'
    params = {
        'watchType': '1',
        'cid': id,
        'source': 'company',
    }
    resp = requests.get(url, headers=headers,params=params)
    lxml = etree.HTML(resp.text)
    info_detail = {}
    # 板块信息
    all_content = lxml.xpath('//div[@class="risk-list-content"]//div[@class="risk-item-warp"]')
    for i in all_content:
        name = i.xpath('.//div[@class="risk-item-title"]//span[@class="title-inner"]/text()')[0]
        data_id = i.xpath('.//div[2]//div[@class="riskbox watch-block"]/@data-id')
        info_detail[name] = data_id
    return info_detail




# 获取具体信息
def get_company_detail(info_detail, watchGid):
    content = list(info_detail.items())[0]
    print(content)

    # 自身风险
    url = 'https://www.tianyancha.com/risk/riskDetailNew.html'
    params = {
        'id': content[1][0],
        'ps': '5',
        'pn': '1',
        # 'companyId': company_id,
        'type': '54',
        'watchGid': watchGid,
        '_': time.time(),
    }
    resp = requests.get(url, params=params, headers=headers)
    # print(resp.text)
    lxml = etree.HTML(resp.text)
    print(lxml.xpath('//tr//text()'))
    # com_date = lxml.xpath('//tr/td[2]/text()')[0]  # 列入日期
    # com_place = lxml.xpath('//tr/td[@class="left-col"][1]/text()')[0]  # 做出决定机关
    # com_reason = lxml.xpath('//tr//td[@class="left-col"]//div/div/text()')[0]  # 列入经营异常名录原因
    # print('列入日期:', com_date)
    # print('做出决定机关:', com_place)
    # print('列入经营异常名录原因:', com_reason)


if __name__ == '__main__':
    company_list = get_company_url()
    for i in company_list:
        print(i)
        watchGid = str(i).split('/')[-1]
        info_detail = get_company_content_id(watchGid)
        print(info_detail)
        # comp_id = get_company_id(i)
        # comp_id = get_company_id('https://www.tianyancha.com/company/4677041846')
        try:
            get_company_detail(info_detail, watchGid)
        except:
            print('该公司没有风险')
        time.sleep(3)
