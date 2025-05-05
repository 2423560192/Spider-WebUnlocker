import requests

headers = {
    'Host': 'api.smallschoolbag.com',
    'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTE2Mjk2LCJpYXQiOjE3NDMwODk0MjIuMTYwMDg2NiwidGltZW91dCI6MjU5MjAwMCwidHlwZSI6MX0.TAJ1VEgtyEWIjri0yxVUXfeQVtqNObSQZ-WYGspB5lY',
    'xweb_xhr': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c33)XWEB/11581',
    'app': '100000',
    'phone_system_type': 'applets',
    'Content-type': 'application/json;charset=UTF-8',
    'accept': '*/*',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://servicewechat.com/wxbea389fff6410981/15/page-frame.html',
    'accept-language': 'zh-CN,zh;q=0.9',
}

json_data = {
    'data': 'dba6c4bac060441e3a16c0b384c8e2e9065cd528733fbbddb7ccd72405817e2b3261eafe575b445bedb773776687c62c2f5d296c538abab1c72a01e6514d070443984ea815b00573d545d134a0fe3bd1a4cd9f8468aa18a1b80aa46273657edad11608a2942a5e5b066f3d3141a22c00796bee0f99f3eb08245c0b5151130f7b768ebbea3b9d9965d183e9a71ae2378efae579f5d8c89c6a40224ea7c214b3a20f6004b1e91364770a1f89d5ec7fd2a3415fe4b1cba0aedbf4f6ef6251a0c19f',
}

response = requests.post('https://api.smallschoolbag.com/a12/book/xml_json/', headers=headers, json=json_data , verify=False)

print(response.json()['data'])
# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"data":"dba6c4bac060441e3a16c0b384c8e2e9065cd528733fbbddb7ccd72405817e2b3261eafe575b445bedb773776687c62c2f5d296c538abab1c72a01e6514d070443984ea815b00573d545d134a0fe3bd1a4cd9f8468aa18a1b80aa46273657edad11608a2942a5e5b066f3d3141a22c00796bee0f99f3eb08245c0b5151130f7b768ebbea3b9d9965d183e9a71ae2378efae579f5d8c89c6a40224ea7c214b3a20f6004b1e91364770a1f89d5ec7fd2a3415fe4b1cba0aedbf4f6ef6251a0c19f"}'
#response = requests.post('https://api.smallschoolbag.com/a12/book/xml_json/', headers=headers, data=data)