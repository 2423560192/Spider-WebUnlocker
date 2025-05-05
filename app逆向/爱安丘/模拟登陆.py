import requests

from app逆向.utils import encrypt_data

cookies = {
    'redirectToken': '0d0d29467fff459f857525b29f70ce11-139146799',
    'redirect': '',
}

headers = {
    'encrypt': '1',
    'version': '1.0.5',
    'orgid': '137',
    'User-Agent': 'null chuangqi.o.137.com.iqilu.app137/1.0.5',
    'platform': 'android',
    'CQ-AGENT': '{"os":"android","brand":"google","imei":"5d19300ca4103d48","osversion":"11","network":"unknown","version":"1.0.5","core":"2.2.1.1"}',
    'Content-type': 'application/json;charset=UTF-8;charset=UTF-8; charset=UTF-8',
    'Host': 'app-auth.iqilu.com',
    # 'Cookie': 'redirectToken=0d0d29467fff459f857525b29f70ce11-139146799; redirect=',
}

params = {
    'e': '1',
}

json_data = {
    'codeKey': '',
    'password': encrypt_data('5201314'),
    'code': '',
    'phone': '17782200192',
    'key': '',
}

response = requests.post('https://app-auth.iqilu.com/member/login', params=params, cookies=cookies, headers=headers,
                         json=json_data)

print(response.json())
