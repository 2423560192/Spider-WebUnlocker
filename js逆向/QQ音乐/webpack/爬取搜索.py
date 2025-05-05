import requests

cookies = {
    'RK': 'PBXIg8LHtZ',
    'ptcz': 'ff6697361f9324e3ba300f8e3c21d5e780c973aa3a4aa7725bf9f38d983b0ff5',
    'eas_sid': 'x1E713z4w768x0X535n0v5E3B3',
    '_hp2_id.1405110977': '%7B%22userId%22%3A%222763049916807354%22%2C%22pageviewId%22%3A%228882298188253671%22%2C%22sessionId%22%3A%225794041752150658%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D',
    'pac_uid': '0_s1ZfeFPzyYi0p',
    '_qimei_uuid42': '194010e221410081b013e717f1890c80f0a5bc7f77',
    '_qimei_fingerprint': '536620e8aa2389dcc7f31f32841cabf7',
    '_clck': '3964555594|1|fuv|0',
    'pgv_pvid': '8641081237',
    'fqm_pvqid': 'cb59cd21-6d64-474b-8f1d-277067dcf84a',
    'ts_refer': 'www.google.com/',
    'ts_uid': '1669148340',
    'tmeLoginType': '2',
    'wxunionid': '',
    'euin': 'owvFoev5NK6loc**',
    'qm_keyst': 'Q_H_L_63k3N1CX3T4QZSDXCC9MSzTPcBSaSnH0vkRByqSC30xBKlHKf9_HaTcr158U2XSRh0y1lkKBDTW_BR0bxomM_Q2M7ulE',
    'qqmusic_key': 'Q_H_L_63k3N1CX3T4QZSDXCC9MSzTPcBSaSnH0vkRByqSC30xBKlHKf9_HaTcr158U2XSRh0y1lkKBDTW_BR0bxomM_Q2M7ulE',
    'psrf_qqrefresh_token': '9E132B169C92A9D4DA70B261866D39AD',
    'psrf_qqunionid': '15E4BA095599F337E31FA36E4CECFABF',
    'wxopenid': '',
    'psrf_access_token_expiresAt': '1749463619',
    'uin': '2480419172',
    'wxrefresh_token': '',
    'psrf_qqopenid': 'CAD99577C54ACCFFA25A4CB454E5A9AA',
    'psrf_qqaccess_token': 'E60A57DB27A56140F7B989E92694CE9B',
    'psrf_musickey_createtime': '1744279619',
    'music_ignore_pskey': '202306271436Hn@vBj',
    'fqm_sessionid': '72ebdd06-c8ee-4199-b990-3c8c401b06a5',
    'pgv_info': 'ssid=s5083744',
    'ts_last': 'y.qq.com/n/ryqq/search',
}

headers = {
    'accept': 'application/json',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://y.qq.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://y.qq.com/',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    # 'cookie': 'RK=PBXIg8LHtZ; ptcz=ff6697361f9324e3ba300f8e3c21d5e780c973aa3a4aa7725bf9f38d983b0ff5; eas_sid=x1E713z4w768x0X535n0v5E3B3; _hp2_id.1405110977=%7B%22userId%22%3A%222763049916807354%22%2C%22pageviewId%22%3A%228882298188253671%22%2C%22sessionId%22%3A%225794041752150658%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; pac_uid=0_s1ZfeFPzyYi0p; _qimei_uuid42=194010e221410081b013e717f1890c80f0a5bc7f77; _qimei_fingerprint=536620e8aa2389dcc7f31f32841cabf7; _clck=3964555594|1|fuv|0; pgv_pvid=8641081237; fqm_pvqid=cb59cd21-6d64-474b-8f1d-277067dcf84a; ts_refer=www.google.com/; ts_uid=1669148340; tmeLoginType=2; wxunionid=; euin=owvFoev5NK6loc**; qm_keyst=Q_H_L_63k3N1CX3T4QZSDXCC9MSzTPcBSaSnH0vkRByqSC30xBKlHKf9_HaTcr158U2XSRh0y1lkKBDTW_BR0bxomM_Q2M7ulE; qqmusic_key=Q_H_L_63k3N1CX3T4QZSDXCC9MSzTPcBSaSnH0vkRByqSC30xBKlHKf9_HaTcr158U2XSRh0y1lkKBDTW_BR0bxomM_Q2M7ulE; psrf_qqrefresh_token=9E132B169C92A9D4DA70B261866D39AD; psrf_qqunionid=15E4BA095599F337E31FA36E4CECFABF; wxopenid=; psrf_access_token_expiresAt=1749463619; uin=2480419172; wxrefresh_token=; psrf_qqopenid=CAD99577C54ACCFFA25A4CB454E5A9AA; psrf_qqaccess_token=E60A57DB27A56140F7B989E92694CE9B; psrf_musickey_createtime=1744279619; music_ignore_pskey=202306271436Hn@vBj; fqm_sessionid=72ebdd06-c8ee-4199-b990-3c8c401b06a5; pgv_info=ssid=s5083744; ts_last=y.qq.com/n/ryqq/search',
}

params = {
    '_': '1744519918411',
    'sign': 'zzc10b12282glvjid1upsu3ct6indil5kwaem23188056',
}

data = '{"comm":{"cv":4747474,"ct":24,"format":"json","inCharset":"utf-8","outCharset":"utf-8","notice":0,"platform":"yqq.json","needNewCode":1,"uin":2480419172,"g_tk_new_20200303":717494401,"g_tk":717494401},"req_1":{"method":"DoSearchForQQMusicDesktop","module":"music.search.SearchCgiService","param":{"remoteplace":"txt.yqq.center","searchid":"67908058675856198","search_type":0,"query":"跳楼机","page_num":1,"num_per_page":10}}}'.encode()

response = requests.post('https://u6.y.qq.com/cgi-bin/musics.fcg', params=params, cookies=cookies, headers=headers, data=data)

print(response.json())