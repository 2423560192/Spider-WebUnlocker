"""
创建用户账号
"""
import requests

cookies = {
    'MSFPC': 'GUID=b510c18cab254891a29a319bfa4adbd1&HASH=b510&LV=202410&V=4&LU=1730359570024',
    'mkt': 'zh-CN',
    'MicrosoftApplicationsTelemetryDeviceId': '42fca622-0daa-4558-bfaf-5000673d0a22',
    'clrc': '{%2220192%22%3a[%22+VC+x0R6%22]}',
    '_pxvid': '92f90123-14de-11f0-9ab6-db8936916353',
    'MUID': '6eac1a87bc0f41c1a1a84dcdbe62ac83',
    'logonLatency': 'LGN01=638803242587198443',
    'fptctx2': 'taBcrIH61PuCVH7eNCyH0APzNoEiOrOqF4FbdtfiWWIQ7qj5RwjglYOtHErqVwVKJhsxJCj2%252bCjZ4JzMtXHYPMt5hiuSQOf4con1Zc2E4ToZrqrEEDUESZd4v%252bpjRzkymtiOADcTD%252bYw4Mp3X0SMP75MlclnhSgvi7l4u%252bsxSMN2oJNqK8aSkTqMQNCMmKiMyBqsIBd6WEdx%252bPs2pJtdsu4dRYviHyJDwM2jMlZ7yqtMWRx%252f97I%252bLRJ03%252fq5d%252fl5Q1Koq%252beF8jms64XkXG0abJGAk7kV%252fCv2Pnd6OCkZkNG8a4xF5EU3JqJlviHZr9PsZfxxck9mtCWQUA6jGBpAeQ%253d%253d',
    'mkt1': 'zh-CN',
    'amsc': 'lvbHbwjv8YSeO86QoWB2NSp8EVLydcRJ7smvZV/wdLU21h6Q6ziVpcN/ZwOIrD3arARVKOAEGREHUfsHK9zLaBoQC8vm8yoOFWY403KttFE2yameiXP0IHMn4NypzStagAHpG2lcnX3x1AQjzqqHUUc2EOPqLX75sjDJu3tFNWc+JoB+dj2CP5wQtnvihj9O/LYqZ2/TReGhhijGY/s1TWZJGpWKA9GWlQqhto0JgTPWWQxAC5iJ0kqV6O/cVBhvUmVK8ouqJZdnM3HcEr5+/Y0toRxwhrsGHR+/PsaO334=:2:3c',
    '_px3': '08f9c243427de83b7dec327af7322e9de52f5fa764aa829b6b568c905d9a1e1e:nIFIPBZXBYvUEOkiayD/kSBJJojjYpGehfBSjfSKoPaFH/sBKtLcPCRMPZSU4S7Ka6DbYBe/VClUUkOGQqVvOQ==:1000:/fcGkjaofIhu25SZdPLvo/Xz/7cbXSvYi5HILbis9FzsKrt0rtejC+xxOmErb8inz+ipM3K1aSjaIigBjPxV8g91J22QQiFZIxd9nZKTQRCS8GYvhmO4snQEYT5lPIzKv+lHWt6xyi++OjduYCfPZG2Ev1cG8IP1lmXb1mqz7xZOy2FpbQlFQrTMP4yez8T22y9mCzF8wMnSbQhQzIAXbG0m2Z37VouYiu6BU6TjU0Q=',
    '_pxde': '4e22436efa5ad083831eab6e846dc255891ba78ca4ab17e67f8139b8ede0aeed:eyJ0aW1lc3RhbXAiOjE3NDQ3Mjg1OTUxMDMsImZfa2IiOjB9',
    'ai_session': 'sUyEQPVaYMCCXEidiVbakx|1744728080582|1744728759141',
}

headers = {
    'accept': 'application/json',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'canary': 'bgZm0m0rJzTycBkUiy6QYt/+Y5LDakScKcuGUL+vtozWZtoSZA8sWq9JxC8P0lsFPJr1c7yq3yi6HElKiUdrUo5+T1vqZi+qaaJlP+eX9jNXsYA9D8VdVaR/q/E27lJbuWq92lm5BTas1nyty+hxkTLfKl/ITAZy/jFaCNk9qrgunF5i2SEGnLnWV2/wlLJSVwwWeJSX0ORSjrGbwHzmZLLMSGa+VWYZY6rEIzIRYUXQMa8J9Q5R7x+9S2Sh1uu0:2:3c',
    'client-request-id': 'c409e4f02cda4d9280353e765fcffd05',
    'content-type': 'application/json; charset=utf-8',
    'correlationid': 'c409e4f02cda4d9280353e765fcffd05',
    'hpgact': '0',
    'hpgid': '200225',
    'origin': 'https://signup.live.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://signup.live.com/signup?cobrandid=ab0455a0-8d03-46b9-b18b-df2f57b9e44c&id=292841&contextid=BCF056238CAA000D&opid=BABE0618217B5809&bk=1744727459&sru=https://login.live.com/login.srf%3fcobrandid%3dab0455a0-8d03-46b9-b18b-df2f57b9e44c%26id%3d292841%26cobrandid%3dab0455a0-8d03-46b9-b18b-df2f57b9e44c%26id%3d292841%26contextid%3dBCF056238CAA000D%26opid%3dBABE0618217B5809%26mkt%3dZH-CN%26lc%3d2052%26bk%3d1744727459%26uaid%3dc409e4f02cda4d9280353e765fcffd05&lw=dob,flname,wld&fl=1&uiflavor=web&lic=1&mkt=ZH-CN&lc=2052&uaid=c409e4f02cda4d9280353e765fcffd05',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    # 'cookie': 'MSFPC=GUID=b510c18cab254891a29a319bfa4adbd1&HASH=b510&LV=202410&V=4&LU=1730359570024; mkt=zh-CN; MicrosoftApplicationsTelemetryDeviceId=42fca622-0daa-4558-bfaf-5000673d0a22; clrc={%2220192%22%3a[%22+VC+x0R6%22]}; _pxvid=92f90123-14de-11f0-9ab6-db8936916353; MUID=6eac1a87bc0f41c1a1a84dcdbe62ac83; logonLatency=LGN01=638803242587198443; fptctx2=taBcrIH61PuCVH7eNCyH0APzNoEiOrOqF4FbdtfiWWIQ7qj5RwjglYOtHErqVwVKJhsxJCj2%252bCjZ4JzMtXHYPMt5hiuSQOf4con1Zc2E4ToZrqrEEDUESZd4v%252bpjRzkymtiOADcTD%252bYw4Mp3X0SMP75MlclnhSgvi7l4u%252bsxSMN2oJNqK8aSkTqMQNCMmKiMyBqsIBd6WEdx%252bPs2pJtdsu4dRYviHyJDwM2jMlZ7yqtMWRx%252f97I%252bLRJ03%252fq5d%252fl5Q1Koq%252beF8jms64XkXG0abJGAk7kV%252fCv2Pnd6OCkZkNG8a4xF5EU3JqJlviHZr9PsZfxxck9mtCWQUA6jGBpAeQ%253d%253d; mkt1=zh-CN; amsc=lvbHbwjv8YSeO86QoWB2NSp8EVLydcRJ7smvZV/wdLU21h6Q6ziVpcN/ZwOIrD3arARVKOAEGREHUfsHK9zLaBoQC8vm8yoOFWY403KttFE2yameiXP0IHMn4NypzStagAHpG2lcnX3x1AQjzqqHUUc2EOPqLX75sjDJu3tFNWc+JoB+dj2CP5wQtnvihj9O/LYqZ2/TReGhhijGY/s1TWZJGpWKA9GWlQqhto0JgTPWWQxAC5iJ0kqV6O/cVBhvUmVK8ouqJZdnM3HcEr5+/Y0toRxwhrsGHR+/PsaO334=:2:3c; _px3=08f9c243427de83b7dec327af7322e9de52f5fa764aa829b6b568c905d9a1e1e:nIFIPBZXBYvUEOkiayD/kSBJJojjYpGehfBSjfSKoPaFH/sBKtLcPCRMPZSU4S7Ka6DbYBe/VClUUkOGQqVvOQ==:1000:/fcGkjaofIhu25SZdPLvo/Xz/7cbXSvYi5HILbis9FzsKrt0rtejC+xxOmErb8inz+ipM3K1aSjaIigBjPxV8g91J22QQiFZIxd9nZKTQRCS8GYvhmO4snQEYT5lPIzKv+lHWt6xyi++OjduYCfPZG2Ev1cG8IP1lmXb1mqz7xZOy2FpbQlFQrTMP4yez8T22y9mCzF8wMnSbQhQzIAXbG0m2Z37VouYiu6BU6TjU0Q=; _pxde=4e22436efa5ad083831eab6e846dc255891ba78ca4ab17e67f8139b8ede0aeed:eyJ0aW1lc3RhbXAiOjE3NDQ3Mjg1OTUxMDMsImZfa2IiOjB9; ai_session=sUyEQPVaYMCCXEidiVbakx|1744728080582|1744728759141',
}

json_data = {
    'BirthDate': '02:02:1908',
    'CheckAvailStateMap': [
        'ahhh3123@outlook.com:false',
    ],
    'Country': 'JP',
    'EvictionWarningShown': [],
    'FirstName': 'CC',
    'IsRDM': False,
    'IsOptOutEmailDefault': True,
    'IsOptOutEmailShown': 1,
    'IsOptOutEmail': True,
    'IsUserConsentedToChinaPIPL': True,
    'LastName': 'Cs',
    'LW': 1,
    'MemberName': 'ahhh3123@outlook.com',
    'RequestTimeStamp': '2025-04-15T14:52:56.374Z',
    'ReturnUrl': '',
    'SignupReturnUrl': 'https://login.live.com/login.srf%3fcobrandid%3dab0455a0-8d03-46b9-b18b-df2f57b9e44c%26id%3d292841%26cobrandid%3dab0455a0-8d03-46b9-b18b-df2f57b9e44c%26id%3d292841%26contextid%3dBCF056238CAA000D%26opid%3dBABE0618217B5809%26mkt%3dZH-CN%26lc%3d2052%26bk%3d1744727459%26uaid%3dc409e4f02cda4d9280353e765fcffd05',
    'SuggestedAccountType': 'EASI',
    'SiteId': '292841',
    'VerificationCodeSlt': '',
    'PrivateAccessToken': '',
    'WReply': '',
    'MemberNameChangeCount': 1,
    'MemberNameAvailableCount': 1,
    'MemberNameUnavailableCount': 0,
    'Password': '5201314dongge',
    'uiflvr': 1001,
    'scid': 100118,
    'uaid': 'c409e4f02cda4d9280353e765fcffd05',
    'hpgid': 200225,
}

response = requests.post(
    'https://signup.live.com/API/CreateAccount?cobrandid=ab0455a0-8d03-46b9-b18b-df2f57b9e44c&id=292841&contextid=BCF056238CAA000D&opid=BABE0618217B5809&bk=1744727459&sru=https://login.live.com/login.srf%3fcobrandid%3dab0455a0-8d03-46b9-b18b-df2f57b9e44c%26id%3d292841%26cobrandid%3dab0455a0-8d03-46b9-b18b-df2f57b9e44c%26id%3d292841%26contextid%3dBCF056238CAA000D%26opid%3dBABE0618217B5809%26mkt%3dZH-CN%26lc%3d2052%26bk%3d1744727459%26uaid%3dc409e4f02cda4d9280353e765fcffd05&lw=dob,flname,wld&fl=1&uiflavor=web&lic=1&mkt=ZH-CN&lc=2052&uaid=c409e4f02cda4d9280353e765fcffd05',
    cookies=cookies,
    headers=headers,
    json=json_data,
)

print(response.json())
