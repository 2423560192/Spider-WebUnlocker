import requests


cookies = {
    'sessionid': 'xlu3qj58yo5zkjm328fr831ps08oid66',
    'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183': '1745931531,1746426452',
    'HMACCOUNT': '74E03469813A9187',
    'Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183': '1746426516',
}



headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.mashangpa.com/problem-detail/1/',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    # 'cookie': 'sessionid=xlu3qj58yo5zkjm328fr831ps08oid66; Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183=1745931531,1746426452; HMACCOUNT=74E03469813A9187; Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183=1746426516',
}
res = []
for i in range(1, 21):
    params = {
        'page': str(i),
    }

    response = requests.get('https://www.mashangpa.com/api/problem-detail/1/data/', params=params, cookies=cookies,
                            headers=headers)
    data = response.json()
    nums = data['current_array']
    print(nums)
    res.extend(nums)
print(sum(res))
