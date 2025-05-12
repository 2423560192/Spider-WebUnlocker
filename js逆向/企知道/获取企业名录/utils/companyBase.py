import requests
from lxml import etree


def get_company_base(session, page, token, proxy, cookies):
    """
    获取企业名/id/链接
    :return:
    """

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'accesstoken': token,
        'content-type': 'application/json',
        # 'cookie': 'sensorsdata2015jssdkchannel=%7B%22prop%22%3A%7B%22_sa_channel_landing_url%22%3A%22%22%7D%7D; wz_uuid=X%2Fae6cde110aa799695890704e505233ff; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22777e5b3451b6493abdfd16dfa14204e3%22%2C%22first_id%22%3A%22193059cc926101-0d3d743c668a5c-26011951-2073600-193059cc92716f%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkzMDU5Y2M5MjYxMDEtMGQzZDc0M2M2NjhhNWMtMjYwMTE5NTEtMjA3MzYwMC0xOTMwNTljYzkyNzE2ZiIsIiRpZGVudGl0eV9sb2dpbl9pZCI6Ijc3N2U1YjM0NTFiNjQ5M2FiZGZkMTZkZmExNDIwNGUzIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22777e5b3451b6493abdfd16dfa14204e3%22%7D%2C%22%24device_id%22%3A%22193059cc926101-0d3d743c668a5c-26011951-2073600-193059cc92716f%22%7D; Hm_lvt_9ea3e7293b7c088e0d2c88874b63e7dd=1732532900,1732546998,1732553897,1732608150; HMACCOUNT=74E03469813A9187; SSO_SESSION_ID=MTQyYmExMmQtMWQxYS00NjliLWJjNjUtNDY4ZjM4MjJiYTZi; ticket=eyJhbGciOiJIUzUxMiJ9.ZXlKNmFYQWlPaUpFUlVZaUxDSmhiR2NpT2lKa2FYSWlMQ0psYm1NaU9pSkJNVEk0UTBKRExVaFRNalUySW4wLi5sSl9BclRKNTVtNEhRLTNkWVNZVjZRLm9GRTFaeWNKcjRiZFRsQm1HcEo3UTROcEpOS25ONWZ6VlY1ODYwQ0RlUE01a01aOHlva1dETTFSVGgxSDdKeUF5Ykh4QVhUUXAzNWVoX0FSWjEtWUwxdEZxb2ZZUkZaYzM1VXl5bzZDZGt0cDh4YmlJcjhnc3pDeVZnRFAtS29HQ1F1dnRpY0tlcEd1NUwyeDl2OVRFakpkN19JYjEweFVFcHItYldnVWRmOUtMMU9xMmwxZkJRQmVaajVod2FyMzAyUkpKVjRsM2JidXFUTWRzbDFEZzNpeV9ackNLODRrcGZhRWFCT2tKOWMuc3lISUdhWkE3T1ZKTUtvTEtEMVFFQQ.F5QzUtNQm-ipdIhayHg90yJKKFcaMUgbaJ7-q69yFx-HqYPLXY82rPaxSlZEDiDD290s5oe0URWEDnLjEsoXmw; _g_t_=e187fcf4d8c3c4f00308cf153525c1fa; token=eyJhbGciOiJIUzUxMiJ9.ZXlKNmFYQWlPaUpFUlVZaUxDSmhiR2NpT2lKa2FYSWlMQ0psYm1NaU9pSkJNVEk0UTBKRExVaFRNalUySW4wLi5sSl9BclRKNTVtNEhRLTNkWVNZVjZRLm9GRTFaeWNKcjRiZFRsQm1HcEo3UTROcEpOS25ONWZ6VlY1ODYwQ0RlUE01a01aOHlva1dETTFSVGgxSDdKeUF5Ykh4QVhUUXAzNWVoX0FSWjEtWUwxdEZxb2ZZUkZaYzM1VXl5bzZDZGt0cDh4YmlJcjhnc3pDeVZnRFAtS29HQ1F1dnRpY0tlcEd1NUwyeDl2OVRFakpkN19JYjEweFVFcHItYldnVWRmOUtMMU9xMmwxZkJRQmVaajVod2FyMzAyUkpKVjRsM2JidXFUTWRzbDFEZzNpeV9ackNLODRrcGZhRWFCT2tKOWMuc3lISUdhWkE3T1ZKTUtvTEtEMVFFQQ.F5QzUtNQm-ipdIhayHg90yJKKFcaMUgbaJ7-q69yFx-HqYPLXY82rPaxSlZEDiDD290s5oe0URWEDnLjEsoXmw; accessToken=eyJhbGciOiJIUzUxMiJ9.ZXlKNmFYQWlPaUpFUlVZaUxDSmhiR2NpT2lKa2FYSWlMQ0psYm1NaU9pSkJNVEk0UTBKRExVaFRNalUySW4wLi5sSl9BclRKNTVtNEhRLTNkWVNZVjZRLm9GRTFaeWNKcjRiZFRsQm1HcEo3UTROcEpOS25ONWZ6VlY1ODYwQ0RlUE01a01aOHlva1dETTFSVGgxSDdKeUF5Ykh4QVhUUXAzNWVoX0FSWjEtWUwxdEZxb2ZZUkZaYzM1VXl5bzZDZGt0cDh4YmlJcjhnc3pDeVZnRFAtS29HQ1F1dnRpY0tlcEd1NUwyeDl2OVRFakpkN19JYjEweFVFcHItYldnVWRmOUtMMU9xMmwxZkJRQmVaajVod2FyMzAyUkpKVjRsM2JidXFUTWRzbDFEZzNpeV9ackNLODRrcGZhRWFCT2tKOWMuc3lISUdhWkE3T1ZKTUtvTEtEMVFFQQ.F5QzUtNQm-ipdIhayHg90yJKKFcaMUgbaJ7-q69yFx-HqYPLXY82rPaxSlZEDiDD290s5oe0URWEDnLjEsoXmw; creditNo=%22%22; param_sign=1NuSG5; Hm_lpvt_9ea3e7293b7c088e0d2c88874b63e7dd=1732608612; s_webp=s; x-web-ip=123.147.251.222, 47.121.110.162, 120.78.44.156, 100.121.99.190; acw_tc=c616dcb9173261311298710303481b4bf91d43837a433f0db92942c93bcb45',
        # 'device-id': 'BC1ydMVzGBnsaajOOPcuT479E5e2axiRkkoVV0g54Sf4omdzwjAXW2C0upA5MVJOC965YTq/fA2GaIBNJ+0kAWQ==',
        'h5version': 'v1.0.0',
        'origin': 'https://qiye.qizhidao.com',
        'priority': 'u=1, i',
        'referer': 'https://qiye.qizhidao.com/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'signature': '2e0101a5240565ab227e391c26418f6c.3Pgebm',
        'token': token,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'user-agent-web': 'X/ae6cde110aa799695890704e505233ff',
    }

    json_data = {
        'keyword': '',
        'keyword_type': [],
        'patent_product_words': [],
        'zone_id': [],
        'zone_name': [],
        'areaEchoData': [
            [
                500000,
                500101,
            ],
        ],
        'industryEchoData': [],
        'industry_name_1': [],
        'industry_name_2': [],
        'industry_name_3': [],
        'new_industry_code_1': [],
        'new_industry_code_2': [],
        'new_industry_code_3': [],
        'address_code_prov': [],
        'address_code_city': [],
        'address_code_dist': [
            500101,
        ],
        'current': page,
        'pageSize': 100,
        'sortCode': 0,
    }

    response = session.post(
        'https://app.qizhidao.com/qzd-bff-enterprise/qzd/v6/es/phasevi/pc/pageQueryHighLevelSearchBase',
        cookies=cookies,
        headers=headers,
        json=json_data,
        proxies=proxy,
    )
    data = response.json()
    return data
