"""
https://www.cls.cn/telegraph
"""

import requests
import execjs

cookies = {
    'HWWAFSESID': 'bcfab136c7c771b7911',
    'HWWAFSESTIME': '1730128889615',
    'Hm_lvt_fa5455bb5e9f0f260c32a1d45603ba3e': '1730128893',
    'Hm_lpvt_fa5455bb5e9f0f260c32a1d45603ba3e': '1730128893',
    'HMACCOUNT': '74E03469813A9187',
    'hasTelegraphNotification': 'on',
    'hasTelegraphRemind': 'on',
    'hasTelegraphSound': 'on',
    'vipNotificationState': 'on',
    'tfstk': 'fMTjtmfpj-2bQlmqA5hPATVpfAb6CdgUC519tCU46ZQYBRddUE7N3CB6fTdp0NlDuGQ6sKp1jjXNBO9w6nlr82RDiNbOCvuE8n_mDg8fBR7TbG53ivkE84ooDNejLKuXp_w5sTCAMPCtN_CG6NEYDdBR26CUHNpOWb_R_saYksCTyQCVeOQOWdd-QPuRafWXGbjinOmbW9OAFyOkPsQ3mIB7WPL78i6L8TaTWU1XasqgfyiNpHXVYg9-zr_6w19VUp3LPaIBxC56hqaAu3KkoZ8rdWjXCtSpPgg8F_TWTHCkNDGWNF6fvEI7_ybAo1pOf3DQ8s_2VMTXmf2JMpWXvZAaOxR5A3shwgF_DZ-eTFjpkqwhUMf63TJKJz_RXg7489GhqlN5xP15LbG7jlYsw74BTUXPGiClaJcSN-_8KPUZQbG7HhsAZ_liNbwfW',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=utf-8',
    # 'Cookie': 'HWWAFSESID=bcfab136c7c771b7911; HWWAFSESTIME=1730128889615; Hm_lvt_fa5455bb5e9f0f260c32a1d45603ba3e=1730128893; Hm_lpvt_fa5455bb5e9f0f260c32a1d45603ba3e=1730128893; HMACCOUNT=74E03469813A9187; hasTelegraphNotification=on; hasTelegraphRemind=on; hasTelegraphSound=on; vipNotificationState=on; tfstk=fMTjtmfpj-2bQlmqA5hPATVpfAb6CdgUC519tCU46ZQYBRddUE7N3CB6fTdp0NlDuGQ6sKp1jjXNBO9w6nlr82RDiNbOCvuE8n_mDg8fBR7TbG53ivkE84ooDNejLKuXp_w5sTCAMPCtN_CG6NEYDdBR26CUHNpOWb_R_saYksCTyQCVeOQOWdd-QPuRafWXGbjinOmbW9OAFyOkPsQ3mIB7WPL78i6L8TaTWU1XasqgfyiNpHXVYg9-zr_6w19VUp3LPaIBxC56hqaAu3KkoZ8rdWjXCtSpPgg8F_TWTHCkNDGWNF6fvEI7_ybAo1pOf3DQ8s_2VMTXmf2JMpWXvZAaOxR5A3shwgF_DZ-eTFjpkqwhUMf63TJKJz_RXg7489GhqlN5xP15LbG7jlYsw74BTUXPGiClaJcSN-_8KPUZQbG7HhsAZ_liNbwfW',
    'If-None-Match': 'W/"7b0-K8ESWoPoWaQBfdhHHoi3DYuY/l4"',
    'Referer': 'https://www.cls.cn/telegraph',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

js = execjs.compile(open('./loader.js').read())

sign = js.call('get_sign')
print(sign)

params = {
    'app': 'CailianpressWeb',
    'category': '',
    'hasFirstVipArticle': '0',
    'lastTime': '1730128713',
    'os': 'web',
    'rn': '20',
    'subscribedColumnIds': '',
    'sv': '7.7.5',
    'sign': sign
}

response = requests.get('https://www.cls.cn/nodeapi/updateTelegraphList', params=params, cookies=cookies,
                        headers=headers)

print(response.text)
