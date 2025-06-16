import time

import requests
import json
from utils import AESCipherCBC


def get_data():
    """获取data"""
    tt = str(int(time.time() * 1000))
    ba = {
        "1": 1,
        "3": "2f8b80e5760eb5397963f7f134e8614656395da3",
        "4": 24,
        "5": "1920x1080",
        "6": "1920x1032",
        "7": ",",
        "8": "PDF%20Viewer,Chrome%20PDF%20Viewer,Chromium%20PDF%20Viewer,Microsoft%20Edge%20PDF%20Viewer,WebKit%20built-in%20PDF",
        "9": "Portable%20Document%20Format,Portable%20Document%20Format",
        "11": 1,
        "12": 1,
        "13": True,
        "14": -480,
        "15": "zh-CN",
        "16": "",
        "17": "1,0,1,1,1,0",
        "18": 1,
        "19": 16,
        "20": 0,
        "21": "",
        "22": "Gecko,20030107,Google Inc.,,Mozilla,Netscape,Win32",
        "23": "1,0,0",
        "24": 1,
        "25": "Google Inc. (NVIDIA),ANGLE (NVIDIA, NVIDIA GeForce RTX 3050 Laptop GPU (0x000025E2) Direct3D11 vs_5_0 ps_5_0, D3D11)",
        "27": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "28": "false,false",
        "29": "true,true,true",
        "30": 0,
        "31": 8,
        "32": 7565,
        "34": "Win32",
        "35": "false,true",
        "41": True,
        "42": 0,
        "43": None,
        "44": 1,
        "58": "",
        "60": "",
        "61": "",
        "62": "",
        "63": True,
        "64": False,
        "65": False,
        "69": 0,
        "70": 0,
        "71": "",
        "72": "zh-CN,zh",
        "73": "",
        "74": "",
        "76": 0,
        "78": "2b30b3f0f15b5ddf1728386b61a929cb76cf59fc_ffe3954226bc6b195b2ab6ddb9358bb67d4d41595902d1e2cb5de40f27b8af1e",
        "79": "0,0,0,0,0",
        "80": "0,0,0,0,0",
        "81": 1,
        "82": "1dbe165a7a53669b2984a8eec8c0bf6972f0b05f",
        "85": "ac169bd59b399e0eeb23fd268bb9c743bf7b6176",
        "101": "f7f346277c45f9ac1eee95f03ca7b36d639b0166",
        "103": tt,
        "106": 2055,
        "107": "3.11.3",
        "108": "https://haoma.baidu.com/appeal?pagef=topbanner&login_type=qzone&login_type=qzone",
        "109": "https://passport.baidu.com/",
        "112": "",
        "113": "",
        "114": "1234",
        "115": "",
        "116": "5b48f7ed5acdbd7ebd8c441221031ad8fcfc059d",
        "130": "[]",
        "136": "[]",
        "198": 33,
        "199": "",
        "200": 1,
        "300": "ed45136a",
        "301": "7ad000ae74724e20",
        "302": "$BAIDU$,B1,BCat,BCat_2055,BCat_2063,BMAP_ANCHOR_BOTTOM_LEFT,BMAP_ANCHOR_BOTTOM_RIGHT,BMAP_ANCHOR_TOP_RIGHT,BMAP_ANIMATION_BOUNCE,BMAP_ANIMATION_DROP,BMAP_API_VERSION,BMAP_CANVAS_DRAWER,BMAP_CONTEXT_MENU_ICON_ZOOMIN,BMAP_CONTEXT_MENU_ICON_ZOOMOUT,BMAP_COORD_BD09,BMAP_COORD_EPSG3857,BMAP_COORD_GCJ02,BMAP_COORD_GCJ02MERCATOR,BMAP_COORD_MERCATOR,BMAP_COORD_WGS84,BMAP_DRIVING_POLICY_AVOID_CONGESTION,BMAP_DRIVING_POLICY_AVOID_HIGHWAYS,BMAP_DRIVING_POLICY_FIRST_HIGHWAYS,BMAP_HIGHLIGHT_ROUTE,BMAP_HIGHLIGHT_STEP,BMAP_HYBRID_MAP,BMAP_INTERCITY_POLICY_CHEAP_PRICE,BMAP_INTERCITY_POLICY_EARLY_START,BMAP_LINE_TYPE_AIRPLANE,BMAP_LINE_TYPE_COACH",
        "402": ""
    }
    j_ba = json.dumps(ba, separators=(":", ','))

    aes = AESCipherCBC(key="E0C544117AAE4F63", iv="636014d173e04409")
    return aes.encrypt(j_ba)


def get_resp(data , sign):
    """获取返回内容"""
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://haoma.baidu.com",
        "Referer": "https://haoma.baidu.com/appeal?pagef=topbanner&login_type=qzone",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    cookies = {
        "BAIDUID_BFESS": "25F79B021EE5E037BEBE57DF46D4170C:FG=1",
        "BAIDU_WISE_UID": "wapp_1723812611607_6",
        "BIDUPSID": "25F79B021EE5E037BEBE57DF46D4170C",
        "PSTM": "1726279009",
        "ZFY": "31G71aVgcVU9UCkoaJ2vq9gbTPABdlLSGIVE7GSp0Bc:C",
        "H_PS_PSSID": "60853_60617_60885_60875",
        "BDUSS": "BRSGNTMVdsVUJrN241bFpKclR-aGtJTXd0enI0c0JIYjFGTGZlZkRSLUtoVjVvSVFBQUFBJCQAAAAAAAAAAAEAAAC6fKeDtqvAxzUyMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIr4NmiK-DZoSj",
        "BDUSS_BFESS": "BRSGNTMVdsVUJrN241bFpKclR-aGtJTXd0enI0c0JIYjFGTGZlZkRSLUtoVjVvSVFBQUFBJCQAAAAAAAAAAAEAAAC6fKeDtqvAxzUyMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIr4NmiK-DZoSj",
        "__sec_t_key": "b3d93211-371f-49d2-9f58-7e7ae87b1969",
        "Hm_lvt_71927aaa06a0dc9d2d16f927f1f6937f": "1749737677",
        "Hm_lpvt_71927aaa06a0dc9d2d16f927f1f6937f": "1749737677",
        "HMACCOUNT": "41D5A6B7364EA1F9",
        "__bid_n": "197647e25e0977633943b5",
        "ab_sr": "1.0.1_Yjc1NDYxZmY5YWI5NzViNzAyZDIyZWM4M2JkYzgwYTU5OTk0MTAyNmZiMTdjODFhN2RlODExYTE4ZmM1YzU3MDkzZTZmNTE2ZDQwYmZkNmFiYmE4MGZjYTYwYzE3YjcyZWJlZTUyMWVkYTJiYmNmMzBmNTliZmMwNjdjNjA3NDk1NjY0OTlmMTNkOTUyZGJhYzY4ODU1NDJlNjNkM2U2OQ=="
    }

    url = "https://haoma.baidu.com/api/v1/appeal/search"
    data = {
        "data": data,
        "key_id": "47",
        "sign": sign,
        "search": "13008322620"
    }

    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, cookies=cookies, data=data)

    print(response.json())


def get_data_sign():
    """获取data和sign"""
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "text/plain;charset=UTF-8",
        "Origin": "https://haoma.baidu.com",
        "Pragma": "no-cache",
        "Referer": "https://haoma.baidu.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    cookies = {
        "BAIDUID_BFESS": "0325527AE5170058C3B7C2A912D0513E:FG=1",
        "__bid_n": "197549149c4494419c1d2a",
        "ab_jid": "2c3755366cb811b665a9fd9ec45ad1e0a92f",
        "ab_jid_BFESS": "2c3755366cb811b665a9fd9ec45ad1e0a92f",
        "ppfuid": "FOCoIC3q5fKa8fgJnwzbE67EJ49BGJeplOzf+4l4EOvDuu2RXBRv6R3A1AZMa49I27C0gDDLrJyxcIIeAeEhD8JYsoLTpBiaCXhLqvzbzmvy3SeAW17tKgNq/Xx+RgOdb8TWCFe62MVrDTY6lMf2GrfqL8c87KLF2qFER3obJGki/e1Zm6tUqYUFmnCPoM8gGEimjy3MrXEpSuItnI4KD7Sp1Q56DZEyadKwtshSrk5LY4n5ZbWgIc+KEO26XuvAXqmsx43d0RT3qZWbLzdUShJsVwXkGdF24AsEQ3K5XBbh9EHAWDOg2T1ejpq0s2eFy9ar/j566XqWDobGoNNfmfpaEhZpob9le2b5QIEdiQcF+6iOKqU/r67N8lf+wxW6FCMUN0p4SXVVUMsKNJv2T2Q0Rs14gDuqHJ3rxHJuOGO4LkPV+7TROLMG0V6r0A++zkWOdjFiy1eD/0R8HcRWYo64YZQejZKa7nFsdjKdPqCp+HBavJhpxl858h16cMtKQmxzisHOxsE/KMoDNYYE7ucLE22Bi0Ojbor7y6SXfVj7+B4iuZO+f7FUDWABtt/WWQqHKVfXMaw5WUmKnfSR5wwQa+N01amx6X+p+x97kkGmoNOSwxWgGvuezNFuiJQdt51yrWaL9Re9fZveXFsIu/gzGjL50VLcWv2NICayyI8BE9m62pdBPySuv4pVqQ9Sl1uTC//wIcO7QL9nm+0N6JgtCkSAWOZCh7Lr0XP6QztjlyD3bkwYJ4FTiNanaDaDeWOT2lhFudb3TK6R013c2eTSiFFJGunWN7gFja+ZJpdh0GvEV9dnyTGKy8XFjCQiSGk66HDxtjKMU4HPNa0dthF7UsHf7NW9eE+gwuTQSa7GLWfOy9+ap4iFBQsmjpefgOF89jAHLbnVUejtrqqvdVSQ/4gzJOb0DGzeEZ5GeyNvbqM4i3mtFsQVtaGF/hTyXlV3f0HZXSpuSxTnDK9hXEsgCUuTOiLZISfR5YGEG7jgBRkDPTwtXjYtgzmW74m0fDU2MZaxpBZZF8YurfocYcmDdcxFKeoIFQmVqAoAU+3YcXQt2xKThZZyV1v3sCvnzidUZtKM9cRRUfRWBtQSb50APM+gs/408xg7KHCB8AOKpZpfIpPhQ0RJhew8GR0aQSrA+avoKMisIiuIyvlqUS1+J9aSd42+X78fDIZgkPh3epzLLvwRmnAbs5z/V+jl6PTOgyr/lI/hqUSvwiH5QWdHYAw7i4QhrXdzc77isXg7iz4pR3pYop7hrU9sO/nmkIl81Iase/C16XVPKOj9XA==",
        "BDUSS": "y9EVkdFY2ZGSmNoWVFCaDBoQlMyd1hsUGRVK2lIbDBSNkJha29uK2MwNlBJM05vQUFBQUFBPT0AAAAAAAAAAKKaIpuksY~2Y3MyNDgwNDE5MTcyAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAI-WS2hbpxvzR",
        "bdrtk": "17497842078ELkSDhlBuH_vfijhUQSPIST-31Eb-6rlM-i-q5-8YM-l2aHH7xEMO9k9CgoHGF_QeE_ugSSSJw8qVP9SgHND9rAow3gTZc3t4eyJHv4D0I%3D",
        "BDUSS_BFESS": "y9EVkdFY2ZGSmNoWVFCaDBoQlMyd1hsUGRVK2lIbDBSNkJha29uK2MwNlBJM05vQUFBQUFBPT0AAAAAAAAAAKKaIpuksY~2Y3MyNDgwNDE5MTcyAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAI-WS2hbpxvzR",
        "ab_bid": "5c3d73bf18bd6cb104a5cb61d8e7b036626d",
        "ab_sr": "1.0.1_MGY5ZjU1NzlhNTEzODRmMGIwNjIzN2Q5ZDI5NTVkYWMwMzgxNWU1ZTZlYjZlYWJhMjU3ZjM0M2NhZTcwYTI3Mzc2NWE4OTE1ZGMyNjI4ZjM3ZTg2YTE0ZjU0OTZlOTVmNGJlYWZhZGRkNjg5MTg4MWY0ZGMwNTA4NWQ3ZmU5Zjc3YzBkNjFiNzcwNjdmNWU5MGM1MmM5MjBkYmU2YTliMw=="
    }
    url = "https://miao.baidu.com/abdr"
    params = {
        "_o": "https://haoma.baidu.com"
    }

    data = get_data()
    data = {
        "data": "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",
        "key_id": "f9a98d46d41c44cd",
        "enc": 2
    }
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, cookies=cookies, params=params, data=data)

    data = response.json()
    return data['data'], data['sign']


def main():
    # 获取data和sign
    data, sign = get_data_sign()
    get_resp(data, sign)


if __name__ == '__main__':
    main()
