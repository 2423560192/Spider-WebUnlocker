import random
import re

import requests
import execjs
from lxml import etree

def get_ua():
    ua_pool = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:132.0) Gecko/20100101 Firefox/132.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:131.0) Gecko/20100101 Firefox/131.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 YaBrowser/24.10.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36 OPR/87.0.0.0"
    ]
    return random.choice(ua_pool)

def get_proxy():
    import requests

    # 提取代理API接口，获取1个代理IP
    api_url = "https://dps.kdlapi.com/api/getdps/?secret_id=o9ntciol602nhd4d0r8e&signature=nifj9hzd3kpty6umri0kwliwfhjl8fnb&num=1&pt=1&format=json&sep=1&dedup=1"

    # 获取API接口返回的代理IP
    proxy_ip = requests.get(api_url).json()
    proxy_ip = proxy_ip['data']['proxy_list'][0]
    # 用户名密码认证(私密代理/独享代理)
    username = "d2074621077"
    password = "nhrxmo0g"
    proxies = {
        "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip},
        "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip}
    }
    return proxies

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/json',
    # 'cookie': 'sensorsdata2015jssdkchannel=%7B%22prop%22%3A%7B%22_sa_channel_landing_url%22%3A%22%22%7D%7D; wz_uuid=X%2Fae6cde110aa799695890704e505233ff; ticket=eyJhbGciOiJIUzUxMiJ9.ZXlKNmFYQWlPaUpFUlVZaUxDSmhiR2NpT2lKa2FYSWlMQ0psYm1NaU9pSkJNVEk0UTBKRExVaFRNalUySW4wLi56M0U3MjVMdERTUzRid2xQVzByWFRBLjdGaHV3d29mV01EeVJsZjZycDdITVBHWHFwQnl0RjYxSTlEb1hneTBoZUpwekpLWEtMLS1LMHdjZkhlQW1wd0hFTjVaaVlnNVU2S3ZhUldsU3NLYl9MZFAtRmNSMThEVjdmSGpnRUM5NlJSeVlhTFRNc1B1emFnNDNfdC1HU0JBYThmc2NBc0JOa3BIcjg0N2FJekhxNmV0X0tsck82SnljNl9vSldZbERZcVFVZGNuMzd3Qjk1cUJ3TXFKNVdYZzAyOG1IbDhnRVlscUlJYVVTdzQwa01jYXk3X1RrNU1xX2c4WlM2MTRIU3MuZmw0dUNvVXMtTS1SOXdIc1pKMGxIUQ.WOJ7N5UvgZWjChbaZeLXZUHnqIpqTHkYoGQTkqSC_NHuTyzPJJGFePjWrJWos1CCAZcYK8fjf9zfKln4a4_IBQ; _g_t_=5e7c6aa676e6da9f49ca4f8f6a7c85db; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22777e5b3451b6493abdfd16dfa14204e3%22%2C%22first_id%22%3A%22193059cc926101-0d3d743c668a5c-26011951-2073600-193059cc92716f%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkzMDU5Y2M5MjYxMDEtMGQzZDc0M2M2NjhhNWMtMjYwMTE5NTEtMjA3MzYwMC0xOTMwNTljYzkyNzE2ZiIsIiRpZGVudGl0eV9sb2dpbl9pZCI6Ijc3N2U1YjM0NTFiNjQ5M2FiZGZkMTZkZmExNDIwNGUzIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22777e5b3451b6493abdfd16dfa14204e3%22%7D%2C%22%24device_id%22%3A%22193059cc926101-0d3d743c668a5c-26011951-2073600-193059cc92716f%22%7D; acw_tc=a6f7e577173255293358611744e9dfa667d3535418338859b55d6554899e3c; accessToken=; token=; x-web-ip=123.147.249.209, 47.121.110.203, 120.78.44.173, 100.121.99.240; Hm_lvt_9ea3e7293b7c088e0d2c88874b63e7dd=1732344208,1732532900,1732546998,1732553897; Hm_lpvt_9ea3e7293b7c088e0d2c88874b63e7dd=1732553897; HMACCOUNT=74E03469813A9187; SSO_SESSION_ID=MzBjNjFjNzUtN2VlMi00OGZjLWI3NTMtYWMxYmM1OTIzYWU2',
    'device-id': 'BI9MN3P8iAJDo4IeDfy+juaD/UD1mc20HnrbbzyhO1wVmaOVo5ic2L7Sx50LB/gTLr2vlDxBC9K/+A8GMj5dLnA==',
    'eagleeye-pappname': 'fyw9n1jhpf@07619cbd1f4e9df',
    'eagleeye-sessionid': 'eOm0I3d3x1n9eRue0u37bq7pavp6',
    'eagleeye-traceid': '81813c9b173255413209410324e9df',
    'origin': 'https://www.qizhidao.com',
    'referer': 'https://www.qizhidao.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'user-agent-web': 'X/ae6cde110aa799695890704e505233ff',
}

session = requests.session()

with open('aes.js', 'r', encoding='utf-8', errors='ignore') as f:
    exejs = f.read()
js = execjs.compile(exejs)

pwd = js.call('get_pwd', '5201314dongge')
print(pwd)

json_data = {
    'clientId': '9304622189680257',
    'username': '13008322620',
    'password': pwd,
}



response = session.post(
    'https://ips-sso.qizhidao.com/v1/security/login_password',
    headers=headers,
    json=json_data,
)
print(response.json())

# 请求其他数据

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'cookie': 'sensorsdata2015jssdkchannel=%7B%22prop%22%3A%7B%22_sa_channel_landing_url%22%3A%22%22%7D%7D; wz_uuid=X/a71194ec9872f2980878745cc94f65c6; acw_tc=2f6a1fa217325809069848896e4ac21d6949195ddd276267b355e21385003b; SSO_SESSION_ID=OTllN2ViYjctYzIzOS00YTEyLWJhOWEtNjYzOTczMzE2MWE2; ticket=eyJhbGciOiJIUzUxMiJ9.ZXlKNmFYQWlPaUpFUlVZaUxDSmhiR2NpT2lKa2FYSWlMQ0psYm1NaU9pSkJNVEk0UTBKRExVaFRNalUySW4wLi5ITzFwb00xU0Zoemx5MDg5ZW1LdkhnLm9VNUtzYUlkUjJYbnFJSTNKT2ZDQnpPakt2TWxhUEhkQ0VPNmc3UWh6RGJYeXkxRExIbjhFVGl2clp3UXZwVXF4dkxsbFNnNUNTSTAxV2xMQXBxRWNFbF9xYk5KWGpvd2JvOE4xcUEzaW9ydkkwNFhhbHlVWXVjeEEybGEydkRQWHVPb3RyYnhlY3ctbWJHYTR0TXJSeEdEVzFCVV9EdldXQnBPLTd4M3lhQmRobmhCdWpDWjNpLUJzRzBHejlneHI2VjNRSlE5emh4LW40RFpWazE0cVRzU3lwNVhsSnlpcmdFZkYwVVdIdVkubjZweUQweVNTa1lLdFd4Q3h6WjI5UQ.sE5EY37FMGCuhh2_Buh2Hp7fHHr75sPNn-XwSsjRyYthoNDMelyCOj84qKhjw1FNn05bHO2xM9bb9PesAuZUrA; tempCode=d0951ebab9cd40f89791d2e05bca15c6; _g_t_=619ba4f56f8138715e599f07809b3033; token=eyJhbGciOiJIUzUxMiJ9.ZXlKNmFYQWlPaUpFUlVZaUxDSmhiR2NpT2lKa2FYSWlMQ0psYm1NaU9pSkJNVEk0UTBKRExVaFRNalUySW4wLi5ITzFwb00xU0Zoemx5MDg5ZW1LdkhnLm9VNUtzYUlkUjJYbnFJSTNKT2ZDQnpPakt2TWxhUEhkQ0VPNmc3UWh6RGJYeXkxRExIbjhFVGl2clp3UXZwVXF4dkxsbFNnNUNTSTAxV2xMQXBxRWNFbF9xYk5KWGpvd2JvOE4xcUEzaW9ydkkwNFhhbHlVWXVjeEEybGEydkRQWHVPb3RyYnhlY3ctbWJHYTR0TXJSeEdEVzFCVV9EdldXQnBPLTd4M3lhQmRobmhCdWpDWjNpLUJzRzBHejlneHI2VjNRSlE5emh4LW40RFpWazE0cVRzU3lwNVhsSnlpcmdFZkYwVVdIdVkubjZweUQweVNTa1lLdFd4Q3h6WjI5UQ.sE5EY37FMGCuhh2_Buh2Hp7fHHr75sPNn-XwSsjRyYthoNDMelyCOj84qKhjw1FNn05bHO2xM9bb9PesAuZUrA; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22335ee09b2dc84f2884c080e0324a106b%22%2C%22first_id%22%3A%22193059b1bdb10cd-0c91bbdfb156bd-4c657b58-2073600-193059b1bdc2518%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkzMDU5YjFiZGIxMGNkLTBjOTFiYmRmYjE1NmJkLTRjNjU3YjU4LTIwNzM2MDAtMTkzMDU5YjFiZGMyNTE4IiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiMzM1ZWUwOWIyZGM4NGYyODg0YzA4MGUwMzI0YTEwNmIifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22335ee09b2dc84f2884c080e0324a106b%22%7D%2C%22%24device_id%22%3A%22193059b1bdb10cd-0c91bbdfb156bd-4c657b58-2073600-193059b1bdc2518%22%7D; accessToken=eyJhbGciOiJIUzUxMiJ9.ZXlKNmFYQWlPaUpFUlVZaUxDSmhiR2NpT2lKa2FYSWlMQ0psYm1NaU9pSkJNVEk0UTBKRExVaFRNalUySW4wLi5ITzFwb00xU0Zoemx5MDg5ZW1LdkhnLm9VNUtzYUlkUjJYbnFJSTNKT2ZDQnpPakt2TWxhUEhkQ0VPNmc3UWh6RGJYeXkxRExIbjhFVGl2clp3UXZwVXF4dkxsbFNnNUNTSTAxV2xMQXBxRWNFbF9xYk5KWGpvd2JvOE4xcUEzaW9ydkkwNFhhbHlVWXVjeEEybGEydkRQWHVPb3RyYnhlY3ctbWJHYTR0TXJSeEdEVzFCVV9EdldXQnBPLTd4M3lhQmRobmhCdWpDWjNpLUJzRzBHejlneHI2VjNRSlE5emh4LW40RFpWazE0cVRzU3lwNVhsSnlpcmdFZkYwVVdIdVkubjZweUQweVNTa1lLdFd4Q3h6WjI5UQ.sE5EY37FMGCuhh2_Buh2Hp7fHHr75sPNn-XwSsjRyYthoNDMelyCOj84qKhjw1FNn05bHO2xM9bb9PesAuZUrA; creditNo=%22%22; param_sign=26FBuj; x-web-ip=175.10.190.221, 47.121.110.186, 120.78.44.167, 100.121.99.174',
    'user-agent': get_ua(),
}

proxy = get_proxy()
print(proxy)
ip = proxy['http'].split('@')[-1].strip('/').split(':')[0]
print(ip)

headers['cookie'] = re.sub(r'x-web-ip=([\d.,\s]+)', f'x-web-ip={ip}', headers['cookie'])


response = requests.get(
    'http://qiye.qizhidao.com/lib/sc7bf76436c24e270d85f631a3837bbdd0/page-78/',
    # cookies=cookies,
    headers=headers,
    proxies=proxy
)

lxml = etree.HTML(response.text)
# print(response.text)

name = lxml.xpath('//span[@class="companyName"]//text()')

print(name)

