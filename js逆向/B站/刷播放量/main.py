"""
B站跑播放量的请求接口
"""
import time

import requests
import execjs

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://www.bilibili.com/video/BV14bNEeeE9F/?spm_id_from=333.1007.tianma.1-2-2.click&vd_source=967471fc7bbde57606bbc84b37affe1d',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
}


# 获取buvid3
def get_buvid3():
    import requests
    params = {
        'spm_id_from': '333.1007.tianma.1-2-2.click',
        'vd_source': '967471fc7bbde57606bbc84b37affe1d',
    }

    response = requests.get('https://www.bilibili.com/video/BV14bNEeeE9F/', params=params, headers=headers)

    return response.cookies['buvid3']


print(get_buvid3())


# 获取_uuid
def get_uuid():
    uuid = execjs.compile(open('bz.js', encoding='utf-8').read()).call('uuid')
    return uuid


print('uuid---', get_uuid())


# 获取b_lsid
def get_b_lsid():
    b_lsid = execjs.compile(open('bz.js', encoding='utf-8').read()).call('get_b_lsid')
    return b_lsid


print('b_lsid---', get_b_lsid())


# 获取sid
def get_sid():
    import requests

    cookies = {
        'buvid3': 'AD1E8193-DF09-1643-BCBB-4F0EAC3B467799964infoc',
        'b_nut': '1739519699',
        'b_lsid': '862252DC_19503742B3C',
        '_uuid': '86854110C-3B10B-CF84-1058F-3210B24C3815899780infoc',
        'CURRENT_FNVAL': '4048',
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'origin': 'https://www.bilibili.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.bilibili.com/video/BV14bNEeeE9F/?spm_id_from=333.1007.tianma.1-2-2.click&vd_source=967471fc7bbde57606bbc84b37affe1d',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        # 'cookie': 'buvid3=AD1E8193-DF09-1643-BCBB-4F0EAC3B467799964infoc; b_nut=1739519699; b_lsid=862252DC_19503742B3C; _uuid=86854110C-3B10B-CF84-1058F-3210B24C3815899780infoc; CURRENT_FNVAL=4048',
    }

    response = requests.get(
        'https://api.bilibili.com/x/player/wbi/v2?aid=113954575618947&cid=28237235002&isGaiaAvoided=false&web_location=1315873&dm_img_list=[]&dm_img_str=V2ViR0wgMS4wIChPcGVuR0wgRVMgMi4wIENocm9taXVtKQ&dm_cover_img_str=QU5HTEUgKE5WSURJQSwgTlZJRElBIEdlRm9yY2UgUlRYIDMwNTAgTGFwdG9wIEdQVSAoMHgwMDAwMjVFMikgRGlyZWN0M0QxMSB2c181XzAgcHNfNV8wLCBEM0QxMSlHb29nbGUgSW5jLiAoTlZJRElBKQ&dm_img_inter=%7B%22ds%22:[],%22wh%22:[3868,6621,8],%22of%22:[226,452,226]%7D&w_rid=f0a28f3761ec52b2041d8304736bf824&wts=1739519700',
        cookies=cookies,
        headers=headers,
    )
    return response.cookies['sid']


print('sid---', get_sid())

cookies = {
    'buvid3': str(get_buvid3()),
    'b_nut': str(int(time.time() * 1000)),
    'buvid4': 'DF556D7D-5402-DE53-C86A-7ED9AA53B92D06564-025021407-ggWcjJQfNNEQvhDCH87rBg%3D%3D',
    'b_lsid': get_b_lsid(),
    '_uuid': str(get_uuid()),
    'CURRENT_FNVAL': '4048',
    'bili_ticket': 'eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Mzk3NzgzMTUsImlhdCI6MTczOTUxOTA1NSwicGx0IjotMX0.1pnS8Gf8moYHkZK42SL-P0F8QM5BohGslZDneVChikw',
    'bili_ticket_expires': '1739778255',
    'buvid_fp': 'fc15f58fe0d4e9b23623b5ff0c0b4303',
    'sid': str(get_sid()),
}

print(cookies)

response = requests.get('https://api.bilibili.com/x/click-interface/click/now', cookies=cookies, headers=headers)

print(response.json())

# h5请求
params = {
    'w_aid': '113954575618947',
    'w_part': '1',
    'w_ftime': '1739543135',
    'w_stime': '1739543136',
    'w_type': '3',
    'web_location': '1315873',
    'w_rid': 'e0e33d4f60d553c8264b339cd4a69d64',
    'wts': '1739543136',
}

data = {
    'aid': '113954575618947',
    'cid': '28237235002',
    'part': '1',
    'lv': '0',
    'ftime': '1739543135',
    'stime': '1739543136',
    'type': '3',
    'sub_type': '0',
    'refer_url': '',
    'outer': '0',
    'statistics': '{"appId":100,"platform":5,"abtest":"","version":""}',
    'mobi_app': 'web',
    'device': 'web',
    'platform': 'web',
    'spmid': '333.788.0.0',
    'from_spmid': '333.1007.tianma.1-2-2.click',
    'session': 'cb04990587992f350fdfac32cee9bce5',
    'csrf': '',
}

response = requests.post(
    'https://api.bilibili.com/x/click-interface/click/web/h5',
    params=params,
    cookies=cookies,
    headers=headers,
    data=data,
)
print(response.json())
