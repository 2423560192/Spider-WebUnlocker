import json
import re
import subprocess
import time
from hashlib import sha256

import requests

timer = int(time.time() * 1000)


def get_h5st(p):
    json_data = json.dumps(p)
    print(json_data)
    # 调用Node.js文件并传递JSON字符串
    # 确保JSON字符串中的双引号不被错误地解释，使用单引号将整个字符串包裹
    # 使用 subprocess 调用 JavaScript 文件，并传递 JSON 字符串作为参数
    ret = subprocess.run(['node', 'h5st.js', json_data], capture_output=True, text=True)

    print(ret.stdout)
    return re.search(":::(?P<h5st>.*?):::", ret.stdout).group("h5st")


cookies = {
    '__jdu': '1577350656',
    'shshshfpa': 'c3c26087-6b48-5d13-3362-0ea94634ef56-1726398226',
    'shshshfpx': 'c3c26087-6b48-5d13-3362-0ea94634ef56-1726398226',
    'jcap_dvzw_fp': 'BwaintpSXSKIzHlfN4bWG23phMBfycsOZ3wOxzdm47eh8p7_wkw_IhYhiKA8K1-9FaMsEg3Jc2Bw7Fe9-ncXhw==',
    'b_webp': '1',
    'b_avif': '1',
    'TrackID': '1GNXP2k-tjiEn7NPNMqY913-7YdR3aB9jICI78Pe9sFZuzTn1LB5s9EP-u8zdBy8-Dh8Zrq75L0POWAcZf0LB5Gbtp30ZArAiY-PiQtzaxJ0',
    'light_key': 'AASBKE7rOxgWQziEhC_QY6yawm3EEFjpnlCiugD4X64cGC9LFibCnNsiY3CkJG9RBYucuD6f',
    'b_dw': '1691',
    'b_dpr': '1.5',
    'b_dh': '825',
    '__jdv': '95931165|www.google.com|-|referral|-|1739010811709',
    '_pst': 'jd_4e26ef37d3e66',
    '_tp': 'OM%2B%2FkF9HD7oeDl0wn3a41brED%2FBqfQVpKAXgTtrMIIw%3D',
    'areaId': '4',
    'ipLoc-djd': '4-113-0-0',
    'PCSYCityID': 'CN_500000_500100_0',
    'umc_count': '1',
    'thor': '1F6D0E5E5CAB08A035D887A38CC36D0A9DDDD7E16440EDFF1168647F1FF754EDC54E107AA7324C6CB2A46D94689253FF3753B4FF064FC3A0798F559C069E2F5E3CCD66DBDA5176EBD3A856EAD8F4F4B6F96CDD70DE0E3D20F462C055D35CFAA9F9DAD5C4C3144D71E5C0EDB97791318E3BBE6F6B090DE6E0942F5E7B2C3D93DB72360EF784047151991E8F36D7501CD9A776D8A8E06D5FCB8DD07B1B6485ED02',
    '__jdc': '29846306',
    'jsavif': '1',
    '__jda': '29846306.1577350656.1726398224.1739103400.1739106200.40',
    '__jdb': '29846306.2.1577350656|40.1739106200',
    'flash': '3_KH7eY9n40T5TPL7XGRmW5Z6HdH4xaOfFwYntWvnqjR5mkXtXYGSfQzVemU80wyl2ITN5JO9iIDjFmUJdsgnYJbLS6UMynCH61q6RF61ApropCRG0_5R9blRgpmFQyQDovAY7LIXto2j_IuQZeIIG3uTdiE1tE3lCHUIJPPCjWTN*',
    '3AB9D23F7A4B3CSS': 'jdd034GSXQX5W6TIK7GXUKHCN6NOTUDNVCOXCBNXVOKGDE54B65V6UWDRDVYIYUZL4NXH5NMGGD42C2JGXVAHZ2JQUXZKAUAAAAMU5LHM3XQAAAAACIP7EVJXOOIP2EX',
    '_gia_d': '1',
    'shshshfpb': 'BApXSkFjG6fFANM6XmQ-zp4GrZ9798l6MBmR4hQkS9xJ1Mq-E-4C2',
    '3AB9D23F7A4B3C9B': '4GSXQX5W6TIK7GXUKHCN6NOTUDNVCOXCBNXVOKGDE54B65V6UWDRDVYIYUZL4NXH5NMGGD42C2JGXVAHZ2JQUXZKAU',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    # 'cookie': '__jdu=1577350656; shshshfpa=c3c26087-6b48-5d13-3362-0ea94634ef56-1726398226; shshshfpx=c3c26087-6b48-5d13-3362-0ea94634ef56-1726398226; jcap_dvzw_fp=BwaintpSXSKIzHlfN4bWG23phMBfycsOZ3wOxzdm47eh8p7_wkw_IhYhiKA8K1-9FaMsEg3Jc2Bw7Fe9-ncXhw==; b_webp=1; b_avif=1; TrackID=1GNXP2k-tjiEn7NPNMqY913-7YdR3aB9jICI78Pe9sFZuzTn1LB5s9EP-u8zdBy8-Dh8Zrq75L0POWAcZf0LB5Gbtp30ZArAiY-PiQtzaxJ0; light_key=AASBKE7rOxgWQziEhC_QY6yawm3EEFjpnlCiugD4X64cGC9LFibCnNsiY3CkJG9RBYucuD6f; b_dw=1691; b_dpr=1.5; b_dh=825; __jdv=95931165|www.google.com|-|referral|-|1739010811709; _pst=jd_4e26ef37d3e66; _tp=OM%2B%2FkF9HD7oeDl0wn3a41brED%2FBqfQVpKAXgTtrMIIw%3D; areaId=4; ipLoc-djd=4-113-0-0; PCSYCityID=CN_500000_500100_0; umc_count=1; thor=1F6D0E5E5CAB08A035D887A38CC36D0A9DDDD7E16440EDFF1168647F1FF754EDC54E107AA7324C6CB2A46D94689253FF3753B4FF064FC3A0798F559C069E2F5E3CCD66DBDA5176EBD3A856EAD8F4F4B6F96CDD70DE0E3D20F462C055D35CFAA9F9DAD5C4C3144D71E5C0EDB97791318E3BBE6F6B090DE6E0942F5E7B2C3D93DB72360EF784047151991E8F36D7501CD9A776D8A8E06D5FCB8DD07B1B6485ED02; __jdc=29846306; jsavif=1; __jda=29846306.1577350656.1726398224.1739103400.1739106200.40; __jdb=29846306.2.1577350656|40.1739106200; flash=3_KH7eY9n40T5TPL7XGRmW5Z6HdH4xaOfFwYntWvnqjR5mkXtXYGSfQzVemU80wyl2ITN5JO9iIDjFmUJdsgnYJbLS6UMynCH61q6RF61ApropCRG0_5R9blRgpmFQyQDovAY7LIXto2j_IuQZeIIG3uTdiE1tE3lCHUIJPPCjWTN*; 3AB9D23F7A4B3CSS=jdd034GSXQX5W6TIK7GXUKHCN6NOTUDNVCOXCBNXVOKGDE54B65V6UWDRDVYIYUZL4NXH5NMGGD42C2JGXVAHZ2JQUXZKAUAAAAMU5LHM3XQAAAAACIP7EVJXOOIP2EX; _gia_d=1; shshshfpb=BApXSkFjG6fFANM6XmQ-zp4GrZ9798l6MBmR4hQkS9xJ1Mq-E-4C2; 3AB9D23F7A4B3C9B=4GSXQX5W6TIK7GXUKHCN6NOTUDNVCOXCBNXVOKGDE54B65V6UWDRDVYIYUZL4NXH5NMGGD42C2JGXVAHZ2JQUXZKAU',
    'origin': 'https://list.jd.com',
    'priority': 'u=1, i',
    'referer': 'https://list.jd.com/',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'x-referer-page': 'https://list.jd.com/list.html',
    'x-rp-client': 'h5_1.0.0',
}

params = {
    'appid': 'search-pc-java',
    'functionId': 'pc_search_s_new',
    'client': 'pc',
    'clientVersion': '1.0.0',
    't': timer,
    'body': '{"cat":"670,671","isList":1,"page":"3","s":"61","click":"0","log_id":"1739106225343.9369","show_items":""}',
    'loginType': '3',
    'uuid': '29846306.1577350656.1726398224.1739103400.1739106200.40',
    'area': '4_113_0_0',
    'h5st': '20250209210343077;rwss9xcdpasraa35;f06cc;tk03w96841b9718nF67xShTjPaC1jPLJmtotusTl0h6Pc5bJqNT9KV6BADsD2v2SfyX1E27l-hM9-mzknXfolbBkPI-Y;e01e62cf4c7c94672353e71acfee59a2ff569389113ab57bab3d09db6760f750;5.0;1739106223077;XRJ6PRHMmVDBnMCBpIjBh0m9m8y93Z3L3ZyA3ZXRPp3MoZ3L3hjB2QXR5xZO3FGBpNWMo5WNiZGNz0GL1IGL1UTLj9WM1QjM30GNgFTN3Z3L3ZyIt8zB08yR5Z3XtRHNkRTL0UGLhFTMzETMiFDLz8GLhJWNn9GBkBGBpFjMzQXRfRn94Ay_4MzR5Z3XtR3MrZ2OkBiC0oD-zcEMxQXRfR383ZXRPp3RTE1-3UFJRUi-3M2-3Z3L3lj_1gDBnQXR5xZO3RmNr0jE3Z3L3BT93ZXRPpH65Z3XkZ3L3ZGNkQzR5ZXR5xZOpZ3L35G83QXR5ZXRPpXN5x2RiFyB3ZXR5Z3XtBmN5x2RjFyB3ZXR5Z3XtZWRfRHMkQzR5ZXR5xZOpZ3L3JG83QXR5ZXRPpHMmZ3L3NG83QXR5ZXRPpXN5x2RnFyB3ZXR5Z3XtR3MrV2OpRXRfRHNkQzR5ZXR5xZOpZ3L3tj83ZXR5Z3XtFWRfRn9tQXR5ZXRPpXN5x2RtQXR5ZXRPpXN5x2R18yR5ZXR5xp75x2R1gDAl4CA3ZXRPpH6eY3L3ZS93ZXRPp3RlBW75tWMjhD-CYnLphXNoZXELYn9icTAr0jE3Z3L3VD8mQXR5xp7;6863855ef6c5bd18276ff7113055e68968c29f09df576abac0d84a1c86075c83',
    'x-api-eid-token': 'jdd034GSXQX5W6TIK7GXUKHCN6NOTUDNVCOXCBNXVOKGDE54B65V6UWDRDVYIYUZL4NXH5NMGGD42C2JGXVAHZ2JQUXZKAUAAAAMU5LHM3XQAAAAACIP7EVJXOOIP2EX',
}

s = sha256()
s.update(params["body"].encode())

body = s.hexdigest()

params2 = {
    "appid": "search-pc-java",
    "functionId": "pc_search_s_new",
    "client": "pc",
    "clientVersion": "1.0.0",
    "t": timer,
    "body": body
}

h5st = get_h5st(params2)
# print("h5st", h5st)


params["h5st"] = h5st

print(params)

response = requests.get('https://api.m.jd.com/', params=params, cookies=cookies, headers=headers)

print(response.text)
