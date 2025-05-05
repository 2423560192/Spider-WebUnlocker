import json

import jsonpath
import requests
from DrissionPage import Chromium

import time


def get_resp(task_id):
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
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'tcs-signature': 'null',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'x-build-version': '1.0.2.2583',
        'x-url-key': 'ma67hekb1cbk',
        'x-view-id': '20250502105822A6AC8490D03E8385199B',
        # 'cookie': 'ttwid=1|z9uF5Q8szJKaZ2uf8wUKzL8UDZvYW-6rEXX6sS9TDOo|1745647070|be686dd66bbb5ac571d893f57d3b673283050d24fda6b5ba8bf4055396805070; ttwid_ss=1|z9uF5Q8szJKaZ2uf8wUKzL8UDZvYW-6rEXX6sS9TDOo|1745647070|be686dd66bbb5ac571d893f57d3b673283050d24fda6b5ba8bf4055396805070; passport_csrf_token=f2f73777c72bcfd77ed3e1621fc94b21; passport_csrf_token_default=f2f73777c72bcfd77ed3e1621fc94b21; s_v_web_id=verify_m9xt7axs_Gzk4hqE2_A2h0_4E1F_ACrZ_OyHTAL8kjxfx; is_hit_partitioned_cookie_canary_ss=true; is_hit_partitioned_cookie_canary_ss=true; is_staff_user=false; is_hit_partitioned_cookie_canary=true; is_hit_partitioned_cookie_canary=true; is_novice_898716661456987=1; is_novice_1797067853020256=0; is_novice_64234685734692=0; first_screen_node_count=5; passport_mfa_token=CjcqeqwEjE2i2kATpk%2BoQncXBn3pjharn6KHMYXALmEOVwZDU6iddqOc3tEnkkny%2BXsJV28guRwVGkoKPAAAAAAAAAAAAABO8rX%2F9f98JwgHDHBTNRpXLJXuRfU%2Fuzw%2BrNIgZcw5Pxc6qNLiXdotEUVePaEBK4Mh1xCCo%2FANGPax0WwgAiIBA2%2BCXjM%3D; d_ticket=7f96d4294d1811eff9013e249bb8d6754ca13; odin_tt=ee9adf7cf36f905520394ed5e438d07c4bf59ded90fab18d61021554069c2454806a3c7347e66e950be8daca92a3fa208520e6ca234489264755e0e35df9b069; n_mh=lqlXEPcEZVh98FSesQG2V7LvO3_tyg86rpRiSZijZFg; passport_auth_status=0fa14174cb69be8ba207d778118c05ca%2C9a3d063325015d9f1c8633c599ef3aa9; passport_auth_status_ss=0fa14174cb69be8ba207d778118c05ca%2C9a3d063325015d9f1c8633c599ef3aa9; sid_guard=31b3e93860f9cb2eeb357e488d97c752%7C1746154700%7C5184000%7CTue%2C+01-Jul-2025+02%3A58%3A20+GMT; uid_tt=0ebe172e0416c720829569152c8bcf67; uid_tt_ss=0ebe172e0416c720829569152c8bcf67; uid_tt_ss=0ebe172e0416c720829569152c8bcf67; sid_tt=31b3e93860f9cb2eeb357e488d97c752; sessionid=31b3e93860f9cb2eeb357e488d97c752; sessionid_ss=31b3e93860f9cb2eeb357e488d97c752; sessionid_ss=31b3e93860f9cb2eeb357e488d97c752; sid_ucp_v1=1.0.0-KDEzOWQ1NzIzNTk5Y2VhNTk2ZWE4YTI1YTUwYmNmYTYwZWNjOGJmYmQKHwiLjrDVxMw2EMzp0MAGGO6_FSAMMOHVkqoGOAJA8QcaAmxmIiAzMWIzZTkzODYwZjljYjJlZWIzNTdlNDg4ZDk3Yzc1Mg; sid_ucp_v1=1.0.0-KDEzOWQ1NzIzNTk5Y2VhNTk2ZWE4YTI1YTUwYmNmYTYwZWNjOGJmYmQKHwiLjrDVxMw2EMzp0MAGGO6_FSAMMOHVkqoGOAJA8QcaAmxmIiAzMWIzZTkzODYwZjljYjJlZWIzNTdlNDg4ZDk3Yzc1Mg; ssid_ucp_v1=1.0.0-KDEzOWQ1NzIzNTk5Y2VhNTk2ZWE4YTI1YTUwYmNmYTYwZWNjOGJmYmQKHwiLjrDVxMw2EMzp0MAGGO6_FSAMMOHVkqoGOAJA8QcaAmxmIiAzMWIzZTkzODYwZjljYjJlZWIzNTdlNDg4ZDk3Yzc1Mg; ssid_ucp_v1=1.0.0-KDEzOWQ1NzIzNTk5Y2VhNTk2ZWE4YTI1YTUwYmNmYTYwZWNjOGJmYmQKHwiLjrDVxMw2EMzp0MAGGO6_FSAMMOHVkqoGOAJA8QcaAmxmIiAzMWIzZTkzODYwZjljYjJlZWIzNTdlNDg4ZDk3Yzc1Mg; COOKIE_IS_LOGIN_FLAG=1; COOKIE_IS_LOGIN_FLAG=1; is_novice_240124284372747=0; view_id=20250502110000246ECFDE203FFCFD1FBF; timestamp=1746154800233',
    }

    session = requests.Session()
    session.cookies.update(cookies)
    session.headers.update(headers)
    json_data = {
        'args': [
            {
                'TaskID': task_id,
            },
        ],
    }

    response = session.post('https://www.baike.com/api/v2/hotDoc/GetTask', cookies=cookies, headers=headers,
                            json=json_data)

    with open('GetTask.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(response.json()))

    json_data = {
        'args': [
            {
                'TaskID': task_id,
                'TaskType': 1,
                'DocID': '1912264274709045028',
                'Price': 10,
                'cookie_enabled': True,
                'screen_width': 1920,
                'screen_height': 1080,
                'browser_language': 'zh-CN',
                'browser_platform': 'Win32',
                'browser_name': 'Mozilla',
                'browser_version': '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
            },
        ],
    }

    response = session.post('https://www.baike.com/api/v2/mission/claimTask', cookies=cookies, headers=headers,
                            json=json_data)

    with open('claimTask.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(response.json()))


browser = Chromium()
tab = browser.new_tab()

cookie = 'ttwid=1|z9uF5Q8szJKaZ2uf8wUKzL8UDZvYW-6rEXX6sS9TDOo|1745647070|be686dd66bbb5ac571d893f57d3b673283050d24fda6b5ba8bf4055396805070; ttwid_ss=1|z9uF5Q8szJKaZ2uf8wUKzL8UDZvYW-6rEXX6sS9TDOo|1745647070|be686dd66bbb5ac571d893f57d3b673283050d24fda6b5ba8bf4055396805070; passport_csrf_token=f2f73777c72bcfd77ed3e1621fc94b21; passport_csrf_token_default=f2f73777c72bcfd77ed3e1621fc94b21; s_v_web_id=verify_m9xt7axs_Gzk4hqE2_A2h0_4E1F_ACrZ_OyHTAL8kjxfx; is_hit_partitioned_cookie_canary_ss=true; is_hit_partitioned_cookie_canary_ss=true; is_staff_user=false; is_hit_partitioned_cookie_canary=true; is_hit_partitioned_cookie_canary=true; is_novice_1797067853020256=0; is_novice_64234685734692=0; is_novice_240124284372747=0; first_screen_node_count=5; passport_mfa_token=Cjj9RtJyPtDhr6zORi8qStRx1XJ%2FLk6cDpl1UrJbPDYPoYo%2BcId1%2BUXTQsxEd2UzVY0U%2BCq9OUy6NBpKCjwAAAAAAAAAAAAATvWMmnrPA%2BM%2FWfMemCYCMvx7oSrsCprP3c4aD6y6fHol86trWU10IxzAZM2%2FUXScf3wQrcTwDRj2sdFsIAIiAQMHUmOM; d_ticket=f2f820aee60be7fd3d5db96c23f20c434ca13; odin_tt=09fc3e38a2446795d5dfcf1ee8c85badbe4727f8cdee6512d1c923b6f8787d2a9530489f23dcfd122968987dc5fd206d42bb30220d9f91f6b89b313a969a6d16; n_mh=QIuYCA8O2aWZzaMKKnIl7cPs_DWjo5qAwHizR0ugccU; passport_auth_status=c268367f1ae422ec383ad25852a07597%2C2ab025a2c7f8cee2149fa80320d26c3a; passport_auth_status_ss=c268367f1ae422ec383ad25852a07597%2C2ab025a2c7f8cee2149fa80320d26c3a; sid_guard=acfbe256b4fb0500ea0d12d9fe816975%7C1746412863%7C5184000%7CFri%2C+04-Jul-2025+02%3A41%3A03+GMT; uid_tt=1233e149b98614b07aba3aba86c4e454; uid_tt_ss=1233e149b98614b07aba3aba86c4e454; uid_tt_ss=1233e149b98614b07aba3aba86c4e454; sid_tt=acfbe256b4fb0500ea0d12d9fe816975; sessionid=acfbe256b4fb0500ea0d12d9fe816975; sessionid_ss=acfbe256b4fb0500ea0d12d9fe816975; sessionid_ss=acfbe256b4fb0500ea0d12d9fe816975; sid_ucp_v1=1.0.0-KDE0NjBjNGQ2MDUzOWYwZjBjYWI5ZTg4ZWRlYTdmNjBlZjZiN2I0N2MKIAiTgKCojMzGBRC_yuDABhjuvxUgDDDCobGoBjgCQPEHGgJsZiIgYWNmYmUyNTZiNGZiMDUwMGVhMGQxMmQ5ZmU4MTY5NzU; sid_ucp_v1=1.0.0-KDE0NjBjNGQ2MDUzOWYwZjBjYWI5ZTg4ZWRlYTdmNjBlZjZiN2I0N2MKIAiTgKCojMzGBRC_yuDABhjuvxUgDDDCobGoBjgCQPEHGgJsZiIgYWNmYmUyNTZiNGZiMDUwMGVhMGQxMmQ5ZmU4MTY5NzU; ssid_ucp_v1=1.0.0-KDE0NjBjNGQ2MDUzOWYwZjBjYWI5ZTg4ZWRlYTdmNjBlZjZiN2I0N2MKIAiTgKCojMzGBRC_yuDABhjuvxUgDDDCobGoBjgCQPEHGgJsZiIgYWNmYmUyNTZiNGZiMDUwMGVhMGQxMmQ5ZmU4MTY5NzU; ssid_ucp_v1=1.0.0-KDE0NjBjNGQ2MDUzOWYwZjBjYWI5ZTg4ZWRlYTdmNjBlZjZiN2I0N2MKIAiTgKCojMzGBRC_yuDABhjuvxUgDDDCobGoBjgCQPEHGgJsZiIgYWNmYmUyNTZiNGZiMDUwMGVhMGQxMmQ5ZmU4MTY5NzU; COOKIE_IS_LOGIN_FLAG=1; COOKIE_IS_LOGIN_FLAG=1; view_id=20250505104110BE53EAFFBE801AF06555; timestamp=1746412870212; is_novice_3125227668635667=0'


# 打开目标页面
tab.get('https://www.baike.com/task_center/hotTask?subPage=hot_doc_update')

# 设置 cookies
tab.set.cookies(cookie)  # 用你的 cookie 替换

# 替换为你要监听的接口关键词，注意要包含域名部分
# target = ['queryHotDocPartialUpdateTask' , 'queryHotDocFullUpdateTask']
target = True
# 启动监听器，并指定 request_type 为 'xhr'（也可选 'fetch' 或不写监听全部）
tab.listen.start(target, res_type='Fetch')  # 或 request_type='fetch'

# 打开目标页面
tab.get('https://www.baike.com/task_center/hotTask?subPage=hot_doc_update')

while True:
    try:
        el = tab.ele('xpath://*[@id="root"]/div/div[2]/div/div[1]/div[2]/div/div[1]/div[2]')
        el.click()
        time.sleep(1)
        el = tab.ele('xpath://*[@id="root"]/div/div[2]/div/div[1]/div[2]/div/div[1]/div[4]')
        # el = tab.ele('xpath://*[@id="root"]/div/div[2]/div/div[1]/div[2]/div/div[1]/div[3]')

        el.click()
        res = tab.listen.wait(3)

        for i in res:
            if 'queryHotDocCreateTask' in i.url or 'queryHotDocFullUpdateTask' in i.url:
                print(i.response.body)
                with open('get_tasks.json', 'w', encoding='utf-8') as f:
                    f.write(json.dumps(i.response.body))

                task_ids = jsonpath.jsonpath(i.response.body, '$..TaskID')
                if task_ids != False:
                    print("任务ID：", task_ids)
                    get_resp(task_ids)

        time.sleep(1)
    except Exception as e:
        print(e)

tab.listen.stop()
tab.close()
