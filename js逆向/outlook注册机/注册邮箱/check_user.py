"""
检查用户名是否存在
"""
import requests

cookies = {
    # 'MSFPC': 'GUID=b510c18cab254891a29a319bfa4adbd1&HASH=b510&LV=202410&V=4&LU=1730359570024',
    'mkt': 'zh-CN',
    # 'MicrosoftApplicationsTelemetryDeviceId': '42fca622-0daa-4558-bfaf-5000673d0a22',
    # 'clrc': '{%2220192%22%3a[%22+VC+x0R6%22]}',
    # '_pxvid': '92f90123-14de-11f0-9ab6-db8936916353',
    # 'MUID': '6eac1a87bc0f41c1a1a84dcdbe62ac83',
    # 'logonLatency': 'LGN01=638803242587198443',
    # 'fptctx2': 'taBcrIH61PuCVH7eNCyH0APzNoEiOrOqF4FbdtfiWWIQ7qj5RwjglYOtHErqVwVKJhsxJCj2%252bCjZ4JzMtXHYPMt5hiuSQOf4con1Zc2E4ToZrqrEEDUESZd4v%252bpjRzkymtiOADcTD%252bYw4Mp3X0SMP75MlclnhSgvi7l4u%252bsxSMN2oJNqK8aSkTqMQNCMmKiMyBqsIBd6WEdx%252bPs2pJtdsu4dRYviHyJDwM2jMlZ7yqtMWRx%252f97I%252bLRJ03%252fq5d%252fl5Q1Koq%252beF8jms64XkXG0abJGAk7kV%252fCv2Pnd6OCkZkNG8a4xF5EU3JqJlviHZr9PsZfxxck9mtCWQUA6jGBpAeQ%253d%253d',
    'mkt1': 'zh-CN',
    'amsc': 'lvbHbwjv8YSeO86QoWB2NSp8EVLydcRJ7smvZV/wdLU21h6Q6ziVpcN/ZwOIrD3arARVKOAEGREHUfsHK9zLaBoQC8vm8yoOFWY403KttFE2yameiXP0IHMn4NypzStagAHpG2lcnX3x1AQjzqqHUUc2EOPqLX75sjDJu3tFNWc+JoB+dj2CP5wQtnvihj9O/LYqZ2/TReGhhijGY/s1TWZJGpWKA9GWlQqhto0JgTPWWQxAC5iJ0kqV6O/cVBhvUmVK8ouqJZdnM3HcEr5+/Y0toRxwhrsGHR+/PsaO334=:2:3c',
    # 'ai_session': 'sUyEQPVaYMCCXEidiVbakx|1744728080582|1744728080582',
    # '_px3': '2bbb7ea4f4e288001924f54de3747e035104f08fe13160dca7414c1e1663dd1a:gJTOFLP0AyUfBdT0tKgfCJK9mqYufZsGdo87A/pREazBEBBNLwT9jda/pE0gClx8IMXfH/m/jtIBCp7c7WkShQ==:1000:tdt0ZKDgybIscOArYNBTYAp9GNogw90iWltU/8RnG+4QF7UI6Ph50qEB3Lz5Q6NrY30qHny524N94H+9OzEEjsPtdyds5b53Zu7SnH34tCWMlSXZPE9YyMA4hDGwipgbuwnmVcCfKvPBf79X+4E0v4Ty868tQzHYOhBSln45rmQhV/Qzu2SzJrC5RGTj2IpegJSDNsw3QGcyW2xwEwe70/UPG/qw69gDzwMQfCDorNY=',
    # '_pxde': 'b22b3670c7572016160bf0ff920ca1bc72b9b093bb4328a06d643c70aea3a419:eyJ0aW1lc3RhbXAiOjE3NDQ3MjgwODU0MDksImZfa2IiOjAsImluY19pZCI6WyI1ZWM0OTYwMDlkYTVlNjNmYzFjODQxYWU4NDFiNTk3YiIsIjdkYzVjZGNmOTYyNmE1MmM5ZGI0ZGRiMDMyYjdkNDZkIl19',
}

headers = {
    'accept': 'application/json',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'canary': 'Vt71shXQ9Edwp50cgyhgFJrrtw5NtyAgL77eNUqFbYrolO04jxsfKaA+V3CXj+Ei74wYt2yKWG/yRODzFOQndrTScfxBZqxicg1l8VYwSvMEKmzGBGh2+jDTfgfVSiIr7ssdRS0H6jYuSd6jBF/0k0qHK0b6p6l5Z+c/rqY0ZyDuFMNUXWZTZ8XCFiIy8NFByCM320eo5H2rgG/Y2P0IVRMgWA/c8yEbUD5qIfjzRBB6M1dzPmEx0nIONinm4KKe:2:3c',
    # 'client-request-id': 'c409e4f02cda4d9280353e765fcffd05',
    'content-type': 'application/json; charset=utf-8',
    # 'correlationid': 'c409e4f02cda4d9280353e765fcffd05',
    # 'hpgact': '0',
    # 'hpgid': '200225',
    'origin': 'https://signup.live.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://signup.live.com/signup?cobrandid=ab0455a0-8d03-46b9-b18b-df2f57b9e44c&id=292841&contextid=BCF056238CAA000D&opid=BABE0618217B5809&bk=1744727459&sru=https://login.live.com/login.srf%3fcobrandid%3dab0455a0-8d03-46b9-b18b-df2f57b9e44c%26id%3d292841%26cobrandid%3dab0455a0-8d03-46b9-b18b-df2f57b9e44c%26id%3d292841%26contextid%3dBCF056238CAA000D%26opid%3dBABE0618217B5809%26mkt%3dZH-CN%26lc%3d2052%26bk%3d1744727459%26uaid%3dc409e4f02cda4d9280353e765fcffd05&lw=dob,flname,wld&fl=1&uiflavor=web&lic=1&mkt=ZH-CN&lc=2052&uaid=c409e4f02cda4d9280353e765fcffd05',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
}

json_data = {
    'includeSuggestions': True,
    'signInName': 'ahhh31234@outlook.com',
    'uiflvr': 1001,
    'scid': 100118,
    # 'uaid': 'c409e4f02cda4d9280353e765fcffd05',
    'hpgid': 200225,
}

url = 'https://signup.live.com/API/CheckAvailableSigninNames'

params = {
    # 'cobrandid': 'ab0455a0-8d03-46b9-b18b-df2f57b9e44c',
    'id': '292841',
    # 'contextid': 'BCF056238CAA000D',
    # 'opid': 'BABE0618217B5809',
    'bk': '1744727459',
    # 'sru': 'https://login.live.com/login.srf?cobrandid=ab0455a0-8d03-46b9-b18b-df2f57b9e44c&id=292841&cobrandid=ab0455a0-8d03-46b9-b18b-df2f57b9e44c&id=292841&contextid=BCF056238CAA000D&opid=BABE0618217B5809&mkt=ZH-CN&lc=2052&bk=1744727459&uaid=c409e4f02cda4d9280353e765fcffd05',
    'lw': 'dob,flname,wld',
    'fl': '1',
    'uiflavor': 'web',
    'lic': '1',
    'mkt': 'ZH-CN',
    'lc': '2052',
    # 'uaid': 'c409e4f02cda4d9280353e765fcffd05'
}

response = requests.post(
    url,
    cookies=cookies,
    headers=headers,
    params=params,
    json=json_data,
)

print(response.json())
