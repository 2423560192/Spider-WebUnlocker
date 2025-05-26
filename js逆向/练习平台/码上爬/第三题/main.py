import time

import requests
from CoreUtils.ua import get_random_ua
from CoreUtils.proxy import get_proxy

res = []
for i in range(1, 21):
    ua = get_random_ua()
    tt = str(int(time.time() * 1000))
    cookies = {
        'sessionid': 'xlu3qj58yo5zkjm328fr831ps08oid66',
        'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183': '1745931531,1746426452',
        'HMACCOUNT': '74E03469813A9187',
        'Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183': tt,
    }

    headers = {
        'Host': 'www.mashangpa.com',
        # 'Cookie': 'sessionid=xlu3qj58yo5zkjm328fr831ps08oid66; Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183=1745931531,1746426452; HMACCOUNT=74E03469813A9187; Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183=1746428109',
        'sec-ch-ua-platform': '"Windows"',
        'user-agent': ua,
        'sec-ch-ua-mobile': '?0',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.mashangpa.com/problem-detail/3/',
        'accept-language': 'zh-CN,zh;q=0.9',
        'priority': 'u=1, i',
    }

    params = {
        'page': str(i),
    }

    response = requests.get('https://www.mashangpa.com/api/problem-detail/3/data/', params=params, cookies=cookies,
                            headers=headers)
    data = response.json()
    print(data)
    nums = data['current_array']
    print(nums)
    res.extend(nums)
    # time.sleep(1)
print(sum(res))
