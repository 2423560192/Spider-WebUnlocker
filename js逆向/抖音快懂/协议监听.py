import requests
from CoreUtils.proxy import get_proxy

cookies = {
    'ttwid': '1|z9uF5Q8szJKaZ2uf8wUKzL8UDZvYW-6rEXX6sS9TDOo|1745647070|be686dd66bbb5ac571d893f57d3b673283050d24fda6b5ba8bf4055396805070',
    'ttwid_ss': '1|z9uF5Q8szJKaZ2uf8wUKzL8UDZvYW-6rEXX6sS9TDOo|1745647070|be686dd66bbb5ac571d893f57d3b673283050d24fda6b5ba8bf4055396805070',
    'passport_csrf_token': 'f2f73777c72bcfd77ed3e1621fc94b21',
    'passport_csrf_token_default': 'f2f73777c72bcfd77ed3e1621fc94b21',
    's_v_web_id': 'verify_m9xt7axs_Gzk4hqE2_A2h0_4E1F_ACrZ_OyHTAL8kjxfx',
    'is_hit_partitioned_cookie_canary_ss': 'true',
    'is_hit_partitioned_cookie_canary_ss': 'true',
    'is_staff_user': 'false',
    'is_hit_partitioned_cookie_canary': 'true',
    'is_hit_partitioned_cookie_canary': 'true',
    'is_novice_1797067853020256': '0',
    'is_novice_64234685734692': '0',
    'is_novice_240124284372747': '0',
    'first_screen_node_count': '5',
    'passport_mfa_token': 'Cjj9RtJyPtDhr6zORi8qStRx1XJ%2FLk6cDpl1UrJbPDYPoYo%2BcId1%2BUXTQsxEd2UzVY0U%2BCq9OUy6NBpKCjwAAAAAAAAAAAAATvWMmnrPA%2BM%2FWfMemCYCMvx7oSrsCprP3c4aD6y6fHol86trWU10IxzAZM2%2FUXScf3wQrcTwDRj2sdFsIAIiAQMHUmOM',
    'd_ticket': 'f2f820aee60be7fd3d5db96c23f20c434ca13',
    'odin_tt': '09fc3e38a2446795d5dfcf1ee8c85badbe4727f8cdee6512d1c923b6f8787d2a9530489f23dcfd122968987dc5fd206d42bb30220d9f91f6b89b313a969a6d16',
    'n_mh': 'QIuYCA8O2aWZzaMKKnIl7cPs_DWjo5qAwHizR0ugccU',
    'passport_auth_status': 'c268367f1ae422ec383ad25852a07597%2C2ab025a2c7f8cee2149fa80320d26c3a',
    'passport_auth_status_ss': 'c268367f1ae422ec383ad25852a07597%2C2ab025a2c7f8cee2149fa80320d26c3a',
    'sid_guard': 'acfbe256b4fb0500ea0d12d9fe816975%7C1746412863%7C5184000%7CFri%2C+04-Jul-2025+02%3A41%3A03+GMT',
    'uid_tt': '1233e149b98614b07aba3aba86c4e454',
    'uid_tt_ss': '1233e149b98614b07aba3aba86c4e454',
    'uid_tt_ss': '1233e149b98614b07aba3aba86c4e454',
    'sid_tt': 'acfbe256b4fb0500ea0d12d9fe816975',
    'sessionid': 'acfbe256b4fb0500ea0d12d9fe816975',
    'sessionid_ss': 'acfbe256b4fb0500ea0d12d9fe816975',
    'sessionid_ss': 'acfbe256b4fb0500ea0d12d9fe816975',
    'sid_ucp_v1': '1.0.0-KDE0NjBjNGQ2MDUzOWYwZjBjYWI5ZTg4ZWRlYTdmNjBlZjZiN2I0N2MKIAiTgKCojMzGBRC_yuDABhjuvxUgDDDCobGoBjgCQPEHGgJsZiIgYWNmYmUyNTZiNGZiMDUwMGVhMGQxMmQ5ZmU4MTY5NzU',
    'sid_ucp_v1': '1.0.0-KDE0NjBjNGQ2MDUzOWYwZjBjYWI5ZTg4ZWRlYTdmNjBlZjZiN2I0N2MKIAiTgKCojMzGBRC_yuDABhjuvxUgDDDCobGoBjgCQPEHGgJsZiIgYWNmYmUyNTZiNGZiMDUwMGVhMGQxMmQ5ZmU4MTY5NzU',
    'ssid_ucp_v1': '1.0.0-KDE0NjBjNGQ2MDUzOWYwZjBjYWI5ZTg4ZWRlYTdmNjBlZjZiN2I0N2MKIAiTgKCojMzGBRC_yuDABhjuvxUgDDDCobGoBjgCQPEHGgJsZiIgYWNmYmUyNTZiNGZiMDUwMGVhMGQxMmQ5ZmU4MTY5NzU',
    'ssid_ucp_v1': '1.0.0-KDE0NjBjNGQ2MDUzOWYwZjBjYWI5ZTg4ZWRlYTdmNjBlZjZiN2I0N2MKIAiTgKCojMzGBRC_yuDABhjuvxUgDDDCobGoBjgCQPEHGgJsZiIgYWNmYmUyNTZiNGZiMDUwMGVhMGQxMmQ5ZmU4MTY5NzU',
    'COOKIE_IS_LOGIN_FLAG': '1',
    'COOKIE_IS_LOGIN_FLAG': '1',
    'view_id': '20250505104110BE53EAFFBE801AF06555',
    'timestamp': '1746412870212',
    'is_novice_3125227668635667': '0',
}

headers = {
    'accept': 'application/json,*/*;q=0.8',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://www.baike.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.baike.com/task_center/hotTask?subPage=hot_doc_optimize',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'tcs-signature': 'null',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    'x-build-version': '1.0.2.2583',
    'x-url-key': 'maahpxn81jh5',
    'x-view-id': '20250505104105A69E0B3C47D23C82A209',
    # 'cookie': 'ttwid=1|z9uF5Q8szJKaZ2uf8wUKzL8UDZvYW-6rEXX6sS9TDOo|1745647070|be686dd66bbb5ac571d893f57d3b673283050d24fda6b5ba8bf4055396805070; ttwid_ss=1|z9uF5Q8szJKaZ2uf8wUKzL8UDZvYW-6rEXX6sS9TDOo|1745647070|be686dd66bbb5ac571d893f57d3b673283050d24fda6b5ba8bf4055396805070; passport_csrf_token=f2f73777c72bcfd77ed3e1621fc94b21; passport_csrf_token_default=f2f73777c72bcfd77ed3e1621fc94b21; s_v_web_id=verify_m9xt7axs_Gzk4hqE2_A2h0_4E1F_ACrZ_OyHTAL8kjxfx; is_hit_partitioned_cookie_canary_ss=true; is_hit_partitioned_cookie_canary_ss=true; is_staff_user=false; is_hit_partitioned_cookie_canary=true; is_hit_partitioned_cookie_canary=true; is_novice_1797067853020256=0; is_novice_64234685734692=0; is_novice_240124284372747=0; first_screen_node_count=5; passport_mfa_token=Cjj9RtJyPtDhr6zORi8qStRx1XJ%2FLk6cDpl1UrJbPDYPoYo%2BcId1%2BUXTQsxEd2UzVY0U%2BCq9OUy6NBpKCjwAAAAAAAAAAAAATvWMmnrPA%2BM%2FWfMemCYCMvx7oSrsCprP3c4aD6y6fHol86trWU10IxzAZM2%2FUXScf3wQrcTwDRj2sdFsIAIiAQMHUmOM; d_ticket=f2f820aee60be7fd3d5db96c23f20c434ca13; odin_tt=09fc3e38a2446795d5dfcf1ee8c85badbe4727f8cdee6512d1c923b6f8787d2a9530489f23dcfd122968987dc5fd206d42bb30220d9f91f6b89b313a969a6d16; n_mh=QIuYCA8O2aWZzaMKKnIl7cPs_DWjo5qAwHizR0ugccU; passport_auth_status=c268367f1ae422ec383ad25852a07597%2C2ab025a2c7f8cee2149fa80320d26c3a; passport_auth_status_ss=c268367f1ae422ec383ad25852a07597%2C2ab025a2c7f8cee2149fa80320d26c3a; sid_guard=acfbe256b4fb0500ea0d12d9fe816975%7C1746412863%7C5184000%7CFri%2C+04-Jul-2025+02%3A41%3A03+GMT; uid_tt=1233e149b98614b07aba3aba86c4e454; uid_tt_ss=1233e149b98614b07aba3aba86c4e454; uid_tt_ss=1233e149b98614b07aba3aba86c4e454; sid_tt=acfbe256b4fb0500ea0d12d9fe816975; sessionid=acfbe256b4fb0500ea0d12d9fe816975; sessionid_ss=acfbe256b4fb0500ea0d12d9fe816975; sessionid_ss=acfbe256b4fb0500ea0d12d9fe816975; sid_ucp_v1=1.0.0-KDE0NjBjNGQ2MDUzOWYwZjBjYWI5ZTg4ZWRlYTdmNjBlZjZiN2I0N2MKIAiTgKCojMzGBRC_yuDABhjuvxUgDDDCobGoBjgCQPEHGgJsZiIgYWNmYmUyNTZiNGZiMDUwMGVhMGQxMmQ5ZmU4MTY5NzU; sid_ucp_v1=1.0.0-KDE0NjBjNGQ2MDUzOWYwZjBjYWI5ZTg4ZWRlYTdmNjBlZjZiN2I0N2MKIAiTgKCojMzGBRC_yuDABhjuvxUgDDDCobGoBjgCQPEHGgJsZiIgYWNmYmUyNTZiNGZiMDUwMGVhMGQxMmQ5ZmU4MTY5NzU; ssid_ucp_v1=1.0.0-KDE0NjBjNGQ2MDUzOWYwZjBjYWI5ZTg4ZWRlYTdmNjBlZjZiN2I0N2MKIAiTgKCojMzGBRC_yuDABhjuvxUgDDDCobGoBjgCQPEHGgJsZiIgYWNmYmUyNTZiNGZiMDUwMGVhMGQxMmQ5ZmU4MTY5NzU; ssid_ucp_v1=1.0.0-KDE0NjBjNGQ2MDUzOWYwZjBjYWI5ZTg4ZWRlYTdmNjBlZjZiN2I0N2MKIAiTgKCojMzGBRC_yuDABhjuvxUgDDDCobGoBjgCQPEHGgJsZiIgYWNmYmUyNTZiNGZiMDUwMGVhMGQxMmQ5ZmU4MTY5NzU; COOKIE_IS_LOGIN_FLAG=1; COOKIE_IS_LOGIN_FLAG=1; view_id=20250505104110BE53EAFFBE801AF06555; timestamp=1746412870212; is_novice_3125227668635667=0',
}

params = {
    'msToken': '30SB4hutdjGcOwTWKWUmpINxv4fArlOTZJXWUC3dE-rPBqcrOnA3bCPS_8esaGnkoCw-3ztF6_P8gv6kTJuAkLnVJyyXwRSYpr3m4dQy9fSCYH9V8NGg5rqYVOm-ORNE',
    # 'a_bogus': 'xvBOkcg2Msm1k9kRD7kz9HNeamm0YW-qgZENXpO1wto4',
}

json_data = {
    'args': [
        {
            'FullUpdateType': 2,
            'Offset': 0,
            'Limit': 18,
            'NeedTotalCount': True,
        },
    ],
}

proxies = get_proxy()

response = requests.post(
    'https://www.baike.com/api/v2/task_center/queryHotDocFullUpdateTask',
    params=params,
    cookies=cookies,
    headers=headers,
    json=json_data,
    # proxies=proxies
)

data = response.text

print(data)
