import requests

from jsonpath import jsonpath

import re


def gey_palce_pid(place):
    cookies = {
        'SCF': 'AvuB9OoNvGiSkZKKE8r-4S3wnpPcVkiLu2jNdaMfqVNxQm0xyuWg09kh91m6pjuyUK6LtVpR-g-4u3PhLd2zwik.',
        'SUB': '_2A25KMCoZDeRhGeFG6VsY9SjEyTuIHXVpTCPRrDV6PUJbktAGLVaikW1NecI3Pgs46q6PGFs97yKiawQvqS4iPlTk',
        'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WhMwRFBIeo1xr8qcPPWo8aS5NHD95QN1hz41K-c1hzNWs4Dqcj-i--fi-z7iKysi--fi-iFiKn4SK-t',
        'ALF': '1734076235',
        '_T_WM': '25715491291',
        'WEIBOCN_FROM': '1110005030',
        'MLOGIN': '1',
        'XSRF-TOKEN': '867d7d',
        'M_WEIBOCN_PARAMS': 'luicode%3D10000011%26lfid%3D231583%26fid%3D100103type%253D9%2526q%253D%25E6%25AD%25A6%25E6%25B1%2589%26uicode%3D10000011',
        'mweibo_short_token': '3686d7867a',
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        # 'cookie': 'SCF=AvuB9OoNvGiSkZKKE8r-4S3wnpPcVkiLu2jNdaMfqVNxQm0xyuWg09kh91m6pjuyUK6LtVpR-g-4u3PhLd2zwik.; SUB=_2A25KMCoZDeRhGeFG6VsY9SjEyTuIHXVpTCPRrDV6PUJbktAGLVaikW1NecI3Pgs46q6PGFs97yKiawQvqS4iPlTk; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhMwRFBIeo1xr8qcPPWo8aS5NHD95QN1hz41K-c1hzNWs4Dqcj-i--fi-z7iKysi--fi-iFiKn4SK-t; ALF=1734076235; _T_WM=25715491291; WEIBOCN_FROM=1110005030; MLOGIN=1; XSRF-TOKEN=867d7d; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D231583%26fid%3D100103type%253D9%2526q%253D%25E6%25AD%25A6%25E6%25B1%2589%26uicode%3D10000011; mweibo_short_token=3686d7867a',
        'mweibo-pwa': '1',
        'priority': 'u=1, i',
        'referer': 'https://m.weibo.cn/p/index?containerid=100103type%3D9%26q%3D%E6%AD%A6%E6%B1%89&extparam=title%3D%E7%9B%B8%E5%85%B3%E5%9C%B0%E7%82%B9&luicode=10000011&lfid=231583',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'x-xsrf-token': '867d7d',
    }

    params = {
        'containerid': f'100103type=9&q={place}',
        'extparam': 'title=相关地点',
        'luicode': '10000011',
        'lfid': '231583',
    }

    response = requests.get('https://m.weibo.cn/api/container/getIndex', params=params, cookies=cookies,
                            headers=headers)

    data = response.json()

    url = jsonpath(data, '$..data..card_group..scheme')[0]

    return re.search(r'containerid=(.*?)&', url).group(1)
