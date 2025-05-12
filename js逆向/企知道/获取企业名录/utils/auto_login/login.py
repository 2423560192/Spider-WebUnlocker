import execjs
import requests

def login_now():

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

    with open('utils/auto_login/aes.js', 'r', encoding='utf-8', errors='ignore') as f:
        exejs = f.read()
    js = execjs.compile(exejs)

    pwd = js.call('get_pwd', '5201314dongge')
    # print(pwd)

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

    print(session.cookies)

    print(response.json())
    token = response.json()['data']['ticket']
    return session , token