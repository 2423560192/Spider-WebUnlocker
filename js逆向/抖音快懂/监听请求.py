import json

from mitmproxy import http
import logging
import jsonpath
import requests


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
        'is_novice_898716661456987': '1',
        'is_novice_1797067853020256': '0',
        'is_novice_64234685734692': '0',
        'first_screen_node_count': '5',
        'passport_mfa_token': 'CjcqeqwEjE2i2kATpk%2BoQncXBn3pjharn6KHMYXALmEOVwZDU6iddqOc3tEnkkny%2BXsJV28guRwVGkoKPAAAAAAAAAAAAABO8rX%2F9f98JwgHDHBTNRpXLJXuRfU%2Fuzw%2BrNIgZcw5Pxc6qNLiXdotEUVePaEBK4Mh1xCCo%2FANGPax0WwgAiIBA2%2BCXjM%3D',
        'd_ticket': '7f96d4294d1811eff9013e249bb8d6754ca13',
        'odin_tt': 'ee9adf7cf36f905520394ed5e438d07c4bf59ded90fab18d61021554069c2454806a3c7347e66e950be8daca92a3fa208520e6ca234489264755e0e35df9b069',
        'n_mh': 'lqlXEPcEZVh98FSesQG2V7LvO3_tyg86rpRiSZijZFg',
        'passport_auth_status': '0fa14174cb69be8ba207d778118c05ca%2C9a3d063325015d9f1c8633c599ef3aa9',
        'passport_auth_status_ss': '0fa14174cb69be8ba207d778118c05ca%2C9a3d063325015d9f1c8633c599ef3aa9',
        'sid_guard': '31b3e93860f9cb2eeb357e488d97c752%7C1746154700%7C5184000%7CTue%2C+01-Jul-2025+02%3A58%3A20+GMT',
        'uid_tt': '0ebe172e0416c720829569152c8bcf67',
        'uid_tt_ss': '0ebe172e0416c720829569152c8bcf67',
        'uid_tt_ss': '0ebe172e0416c720829569152c8bcf67',
        'sid_tt': '31b3e93860f9cb2eeb357e488d97c752',
        'sessionid': '31b3e93860f9cb2eeb357e488d97c752',
        'sessionid_ss': '31b3e93860f9cb2eeb357e488d97c752',
        'sessionid_ss': '31b3e93860f9cb2eeb357e488d97c752',
        'sid_ucp_v1': '1.0.0-KDEzOWQ1NzIzNTk5Y2VhNTk2ZWE4YTI1YTUwYmNmYTYwZWNjOGJmYmQKHwiLjrDVxMw2EMzp0MAGGO6_FSAMMOHVkqoGOAJA8QcaAmxmIiAzMWIzZTkzODYwZjljYjJlZWIzNTdlNDg4ZDk3Yzc1Mg',
        'sid_ucp_v1': '1.0.0-KDEzOWQ1NzIzNTk5Y2VhNTk2ZWE4YTI1YTUwYmNmYTYwZWNjOGJmYmQKHwiLjrDVxMw2EMzp0MAGGO6_FSAMMOHVkqoGOAJA8QcaAmxmIiAzMWIzZTkzODYwZjljYjJlZWIzNTdlNDg4ZDk3Yzc1Mg',
        'ssid_ucp_v1': '1.0.0-KDEzOWQ1NzIzNTk5Y2VhNTk2ZWE4YTI1YTUwYmNmYTYwZWNjOGJmYmQKHwiLjrDVxMw2EMzp0MAGGO6_FSAMMOHVkqoGOAJA8QcaAmxmIiAzMWIzZTkzODYwZjljYjJlZWIzNTdlNDg4ZDk3Yzc1Mg',
        'ssid_ucp_v1': '1.0.0-KDEzOWQ1NzIzNTk5Y2VhNTk2ZWE4YTI1YTUwYmNmYTYwZWNjOGJmYmQKHwiLjrDVxMw2EMzp0MAGGO6_FSAMMOHVkqoGOAJA8QcaAmxmIiAzMWIzZTkzODYwZjljYjJlZWIzNTdlNDg4ZDk3Yzc1Mg',
        'COOKIE_IS_LOGIN_FLAG': '1',
        'COOKIE_IS_LOGIN_FLAG': '1',
        'is_novice_240124284372747': '0',
        'view_id': '20250502110000246ECFDE203FFCFD1FBF',
        'timestamp': '1746154800233',
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

    with open('GetTask.json' , 'w' , encoding='utf-8') as f:
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

    with open('claimTask.json' , 'w' , encoding='utf-8') as f:
        f.write(json.dumps(response.json()))



# 禁掉mitmproxy自身所有日志，只留自己写的print
logging.basicConfig(level=logging.CRITICAL)

def response(flow: http.HTTPFlow) -> None:
    if "/queryHotDocCreateTask" in flow.request.pretty_url or 'queryHotDocFullUpdateTask' in flow.request.pretty_url or 'queryHotDocFullUpdateTask' in flow.request.pretty_url:
        body = flow.response.get_text()

        data = json.loads(body)

        # 提取task_id
        task_ids = jsonpath.jsonpath(data , '$..TaskID')

        get_resp(task_ids[0])



        print("\n=== 🚀 捕获到 queryDocFullUpdateTask 响应 ===")
        with open('body.json' , 'w' , encoding='utf-8') as f:
            f.write(json.dumps(body))
        print("=== 🚀 结束 ===\n")
