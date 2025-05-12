import requests
import execjs

cookies = {
    '_xmLog': 'h5&ea8ef125-f290-4ecd-a4e0-b0ed5de9b697&2.4.18-alpha.0',
    'xm-page-viewid': 'ximalaya-web',
    'wfp': 'ACMxMGEzZmM1OWQwM2FiMjFlbVCQLr0mXn14bXdlYl93d3c',
    'Hm_lvt_4a7d8ec50cfd6af753c4f8aee3425070': '1738393240',
    'Hm_lpvt_4a7d8ec50cfd6af753c4f8aee3425070': '1738393240',
    'HMACCOUNT': '74E03469813A9187',
    'impl': 'www.ximalaya.com.login',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    # 'Cookie': '_xmLog=h5&ea8ef125-f290-4ecd-a4e0-b0ed5de9b697&2.4.18-alpha.0; xm-page-viewid=ximalaya-web; wfp=ACMxMGEzZmM1OWQwM2FiMjFlbVCQLr0mXn14bXdlYl93d3c; Hm_lvt_4a7d8ec50cfd6af753c4f8aee3425070=1738393240; Hm_lpvt_4a7d8ec50cfd6af753c4f8aee3425070=1738393240; HMACCOUNT=74E03469813A9187; impl=www.ximalaya.com.login',
    'Origin': 'https://www.ximalaya.com',
    'Pragma': 'no-cache',
    'Referer': 'https://www.ximalaya.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

uname = '17782200192'
pwd = '12345678'

# 获取加密pwd
pwd = execjs.compile(open('xmly.js', encoding='utf-8').read()).call('get_pwd', pwd)
print(pwd)

# 获取sign
data = {
    'account': uname,
    'nonce': '0-C959D35A2A182a00fb2e21381445c1637ee8401c54103d5053d910689cd41e',
    'password': pwd

}
sign = execjs.compile(open('xmly.js', encoding='utf-8').read()).call('get_sign', data)
print(sign)

json_data = {
    'account': uname,
    'password': pwd,
    'nonce': '0-C959D35A2A182a00fb2e21381445c1637ee8401c54103d5053d910689cd41e',
    'signature': sign,
    # 'fdsOtp': '{"captcha_id":"4f9ca589ee31bd384760d8d1cec5c675","lot_number":"ad13ce4a63054c8e9c0256b693301e47","pass_token":"6c4454ccc3d0db1cf018e2b99cc9093e6ce90152e0c0efce02dc912f994b08b8","gen_time":"1738393306","captcha_output":"djfZyC4bntN9qh97G0s4gqsSPB743lO5YPfnFpTic_LPP7z0T8L2EiN1od1rYClCXbHB3FIz60kDCJpTARdwHOwWAL4duFy2G6yU2kh52uGa3OwgTGdWK2_-iRe71nAacH5z3i3Z1OCZTI3ALlOkz9gExtzKGIl5OKRigtJQM1yWaqXypTTTQx1sM_hfGSG6qNNAuh9XI9cQbfPHCjFWE2SKE2OFLc-t43C_9mUBjDJktnbr45KMDeaIJpaZ5KSsVF1YrbztLMbs23O0C6nnCifpuPD-IcgNgG0Y0tbZUI-4iZ5NVbtu6OJRaGJtRvV0Gh2ybHLmB5eyPrl0Dy_KzenGe-JQZ_LFgqTQ7Nek_7uZYOFV5pNjc5XLhoIKiVf45OsRBDabtIW3edrq_6b0OgMQ7Wo3Z2MyPy5ZnaSfLicEOwxSM4p6YWHIR5UNe9GwIMvWV-OBjyPScPq5IZSSnbDgg4QuBRvn75O_0nYjsjWeOa8UCP8Pe3Urt54fDz-n"}',
    'rememberMe': False,
}

response = requests.post('https://passport.ximalaya.com/web/login/pwd/v1', cookies=cookies, headers=headers,
                         json=json_data)

print(response.json())
