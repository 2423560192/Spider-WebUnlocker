"""
https://www.kixdutyfree.jp/cn/search/?cgid=root&prefn1=badges&prefv1=Duty+Free+Exclusive&utm_source=social&utm_medium=social_media&utm_campaign=Wechat_OA_LimtiedProduct&utm_id=unpaid&utm_content=toppage
"""

import requests

cookies = {
    'dwanonymous_e0a9409e1bd811897775aeb492f77e2c': 'adzfGbwaRNlgaKLGXex0N0tdF6',
    '_gcl_au': '1.1.731657069.1731309392',
    '_fbp': 'fb.1.1731309393304.574881231908637634',
    'krt.vis': '_iZ_VZBzLZ49VMB',
    '_gid': 'GA1.2.1063004799.1731309416',
    '_fwb': '206n8zuVStHs5x4LlASQOVm.1731309415519',
    'FPID': 'FPID2.2.LbYjdio8EcAt0Cy%2FPbIpRjsrRFIxX9wnJyOzjhV8N5s%3D.1731309415',
    'FPLC': 'u02HQFxztEWjHh9X9XjhDchbL2GdK7GYoZemGWnoV1Spdhh9xnpwx2FIoipWE6lBL5gOeDWLugvNoKoL5pkRQ0qX85cr1W5QOfmlK%2BIh3jRnfnufqSiH%2BBzUqbj1cg%3D%3D',
    '_clck': 'ezoo24%7C2%7Cfqs%7C0%7C1776',
    'OptanonAlertBoxClosed': '2024-11-11T07:21:00.392Z',
    '__cq_uuid': 'adzfGbwaRNlgaKLGXex0N0tdF6',
    '__cq_seg': '0~0.00!1~0.00!2~0.00!3~0.00!4~0.00!5~0.00!6~0.00!7~0.00!8~0.00!9~0.00',
    'dwac_c20516f8aecd74e412a4a5b033': 'fAf1MDfHWtboVeLnAmWvBNzlQ3xV0t4T1hI%3D|dw-only|||JPY|false|Asia%2FTokyo|true',
    'cqcid': 'adzfGbwaRNlgaKLGXex0N0tdF6',
    'cquid': '||',
    'sid': 'fAf1MDfHWtboVeLnAmWvBNzlQ3xV0t4T1hI',
    '__cq_dnt': '0',
    'dw_dnt': '0',
    'dwsid': 'cgSm46UqihBi65yAxwQ7tNLmEK_HPw7VXKx7EfWtlCyDy157Zvf1rHYcpsEu6__d7r50U3cGsw25kgartdf0gg==',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Mon+Nov+11+2024+19%3A02%3A06+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202312.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=8b93d0f2-44d4-47e1-85f8-25f3aea43fa5&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=JP%3B',
    'Hm_lvt_04a603cd26f966a4716905eb105252a0': '1731309415,1731322020,1731322927',
    'Hm_lpvt_04a603cd26f966a4716905eb105252a0': '1731322927',
    'HMACCOUNT': '74E03469813A9187',
    '_gat_UA-279574-41': '1',
    'wcs_bt': 's_ce2d83f1c17:1731322926',
    '_ga': 'GA1.1.1240241658.1731309415',
    '_clsk': '1wbq4gf%7C1731322928746%7C3%7C1%7Ct.clarity.ms%2Fcollect',
    '_ga_541MNS4D2L': 'GS1.1.1731322021.2.1.1731322935.0.0.454449903',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    # 'cookie': 'dwanonymous_e0a9409e1bd811897775aeb492f77e2c=adzfGbwaRNlgaKLGXex0N0tdF6; _gcl_au=1.1.731657069.1731309392; _fbp=fb.1.1731309393304.574881231908637634; krt.vis=_iZ_VZBzLZ49VMB; _gid=GA1.2.1063004799.1731309416; _fwb=206n8zuVStHs5x4LlASQOVm.1731309415519; FPID=FPID2.2.LbYjdio8EcAt0Cy%2FPbIpRjsrRFIxX9wnJyOzjhV8N5s%3D.1731309415; FPLC=u02HQFxztEWjHh9X9XjhDchbL2GdK7GYoZemGWnoV1Spdhh9xnpwx2FIoipWE6lBL5gOeDWLugvNoKoL5pkRQ0qX85cr1W5QOfmlK%2BIh3jRnfnufqSiH%2BBzUqbj1cg%3D%3D; _clck=ezoo24%7C2%7Cfqs%7C0%7C1776; OptanonAlertBoxClosed=2024-11-11T07:21:00.392Z; __cq_uuid=adzfGbwaRNlgaKLGXex0N0tdF6; __cq_seg=0~0.00!1~0.00!2~0.00!3~0.00!4~0.00!5~0.00!6~0.00!7~0.00!8~0.00!9~0.00; dwac_c20516f8aecd74e412a4a5b033=fAf1MDfHWtboVeLnAmWvBNzlQ3xV0t4T1hI%3D|dw-only|||JPY|false|Asia%2FTokyo|true; cqcid=adzfGbwaRNlgaKLGXex0N0tdF6; cquid=||; sid=fAf1MDfHWtboVeLnAmWvBNzlQ3xV0t4T1hI; __cq_dnt=0; dw_dnt=0; dwsid=cgSm46UqihBi65yAxwQ7tNLmEK_HPw7VXKx7EfWtlCyDy157Zvf1rHYcpsEu6__d7r50U3cGsw25kgartdf0gg==; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Nov+11+2024+19%3A02%3A06+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202312.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=8b93d0f2-44d4-47e1-85f8-25f3aea43fa5&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=JP%3B; Hm_lvt_04a603cd26f966a4716905eb105252a0=1731309415,1731322020,1731322927; Hm_lpvt_04a603cd26f966a4716905eb105252a0=1731322927; HMACCOUNT=74E03469813A9187; _gat_UA-279574-41=1; wcs_bt=s_ce2d83f1c17:1731322926; _ga=GA1.1.1240241658.1731309415; _clsk=1wbq4gf%7C1731322928746%7C3%7C1%7Ct.clarity.ms%2Fcollect; _ga_541MNS4D2L=GS1.1.1731322021.2.1.1731322935.0.0.454449903',
    'priority': 'u=1, i',
    'referer': 'https://www.kixdutyfree.jp/cn/search/?cgid=root&prefn1=badges&prefv1=Duty+Free+Exclusive&utm_source=social&utm_medium=social_media&utm_campaign=Wechat_OA_LimtiedProduct&utm_id=unpaid&utm_content=toppage',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

params = {
    'cgid': 'root',
    'prefn1': 'badges',
    'prefv1': 'Duty Free Exclusive',
    'srule': 'new-arrivals',
    'start': '0',
    'sz': '24',
    'selectedUrl': 'https://www.kixdutyfree.jp/on/demandware.store/Sites-KixDutyFree-Site/zh_CN/Search-UpdateGrid?cgid=root&prefn1=badges&prefv1=Duty%20Free%20Exclusive&srule=new-arrivals&start=0&sz=24',
}

response = requests.get(
    'https://www.kixdutyfree.jp/on/demandware.store/Sites-KixDutyFree-Site/zh_CN/Search-UpdateGrid',
    params=params,
    cookies=cookies,
    headers=headers,
)

print(response.text)
