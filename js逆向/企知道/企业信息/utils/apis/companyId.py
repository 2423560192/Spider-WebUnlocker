from lxml import etree

import requests

from ..extends import change_ip_cookie


def get_company_id(url):
    """
    获取每一页企业的ID
    :return:
    """
    proxies, cookie, ua = change_ip_cookie()

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',

        'user-agent': ua,
        'cookie': cookie
    }
    # 进入详情页并抓取基础信息
    print('cookie: ', cookie)

    response = requests.get(
        url,
        headers=headers
    )
    resp = response.text
    lxml = etree.HTML(resp)
    # 获取id
    # ids = lxml.xpath('//div[@class="lib-list"][1]//div[@class="companyNameInfo"]/div/span/h2/a/@href')
    ids = lxml.xpath('//div[@class="companyNameInfo"]/div/span/h2/a/@href')

    return ids


def get_company_name(url):
    """
    获取每一页企业的ID
    :return:
    """
    proxies, cookie, ua = change_ip_cookie()
    print(proxies)
    print(cookie)
    print(ua)

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        # 'cookie': 'smidV2=20241107155300e56215c18df006f220796b6484a02e210048cfb7335218630; sensorsdata2015jssdkchannel=%7B%22prop%22%3A%7B%22_sa_channel_landing_url%22%3A%22%22%7D%7D; _bl_uid=wgmat3s77RU0avgO4b6Rrkd8n7kX; wz_uuid=X%2Fae6cde110aa799695890704e505233ff; token=eyJhbGciOiJIUzUxMiJ9.ZXlKNmFYQWlPaUpFUlVZaUxDSmhiR2NpT2lKa2FYSWlMQ0psYm1NaU9pSkJNVEk0UTBKRExVaFRNalUySW4wLi5ZWlpVMmRRNlFzNkZ6MFp3VkVSNGV3LmJSRmx0bWN4eHVEOFhBbWpLMHFfVFZPeWF0V0xXd1JNYmNsTDA2aW91NnlZdl8zam9xZnZLTHlSdUhaUy0xOUIyYktqMURXbGJJaXR2dy1HcmhxWnZqVnd2ZW1oeE1UdUJseXlPOWVnTkR2UzlsbkM0dWZsNEZGclhfc0lSVGV6a0s2VTdybDZrV2pDTXVNS0ZIMlM2WFRwdjZBUkliN2JFS19IZG54VVRVYVY1YkZKaUJrSl9ZaVJuTkhFQ1h2NXVyaEZYdl9kUlhJVWFvS1AtTlQ4dzFUYWJFT0I5VEZsNEZfSDVxOG5IN1EuelNuYlRwZHdtZGs3WG9TWW90em0tdw.X-HChNbl2qCWlQdZxXkL_Vg3fqb-MQ3NcpwjHWe9oDn3Mnrv7emB_mYbgiq7yDjqSFfXY0Ksv0A4HlPsnI1NYw; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22777e5b3451b6493abdfd16dfa14204e3%22%2C%22first_id%22%3A%22193059cc926101-0d3d743c668a5c-26011951-2073600-193059cc92716f%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkzMDU5Y2M5MjYxMDEtMGQzZDc0M2M2NjhhNWMtMjYwMTE5NTEtMjA3MzYwMC0xOTMwNTljYzkyNzE2ZiIsIiRpZGVudGl0eV9sb2dpbl9pZCI6Ijc3N2U1YjM0NTFiNjQ5M2FiZGZkMTZkZmExNDIwNGUzIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22777e5b3451b6493abdfd16dfa14204e3%22%7D%2C%22%24device_id%22%3A%22193059cc926101-0d3d743c668a5c-26011951-2073600-193059cc92716f%22%7D; accessToken=eyJhbGciOiJIUzUxMiJ9.ZXlKNmFYQWlPaUpFUlVZaUxDSmhiR2NpT2lKa2FYSWlMQ0psYm1NaU9pSkJNVEk0UTBKRExVaFRNalUySW4wLi5ZWlpVMmRRNlFzNkZ6MFp3VkVSNGV3LmJSRmx0bWN4eHVEOFhBbWpLMHFfVFZPeWF0V0xXd1JNYmNsTDA2aW91NnlZdl8zam9xZnZLTHlSdUhaUy0xOUIyYktqMURXbGJJaXR2dy1HcmhxWnZqVnd2ZW1oeE1UdUJseXlPOWVnTkR2UzlsbkM0dWZsNEZGclhfc0lSVGV6a0s2VTdybDZrV2pDTXVNS0ZIMlM2WFRwdjZBUkliN2JFS19IZG54VVRVYVY1YkZKaUJrSl9ZaVJuTkhFQ1h2NXVyaEZYdl9kUlhJVWFvS1AtTlQ4dzFUYWJFT0I5VEZsNEZfSDVxOG5IN1EuelNuYlRwZHdtZGs3WG9TWW90em0tdw.X-HChNbl2qCWlQdZxXkL_Vg3fqb-MQ3NcpwjHWe9oDn3Mnrv7emB_mYbgiq7yDjqSFfXY0Ksv0A4HlPsnI1NYw; Hm_lvt_9ea3e7293b7c088e0d2c88874b63e7dd=1732159030,1732201329,1732344208,1732532900; .thumbcache_de0d870e3139ba2368b2e7ea8f11063c=jY1T1OpjJo3V8VXl0qfBPLknBv2RJfWowHxrTctJXIcVFgqsYHksS6eApqCiHIupxjtmHjt1w5QDM3m/PXV22g%3D%3D; Hm_lvt_8b5ea374777742fd73d0561bd1dfca6d=1732344687,1732419877,1732522419,1732545616; Hm_lpvt_8b5ea374777742fd73d0561bd1dfca6d=1732545616; HMACCOUNT=74E03469813A9187; creditNo=%22%22',
        'user-agent': ua,
        'cookie': cookie,
    }
    # 进入详情页并抓取基础信息

    response = requests.get(
        url,
        headers=headers,
        proxies = proxies
    )
    resp = response.text
    lxml = etree.HTML(resp)

    name = lxml.xpath('//span[@class="companyName"]//text()')

    return name
