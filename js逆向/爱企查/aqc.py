"""
筛选获取企业信息
"""

import json
import time

import requests
from jsonpath import jsonpath


# 请求数据
def get_data(page):
    url = 'https://aiqicha.baidu.com/s/advanceSearchAjax?p=1&s=10&f=%7B%22provinceCode%22:[%22430000%22],%22openStatus%22:[%22%E5%BC%80%E4%B8%9A%22]%7D&o=0'
    cookies = {
        'BIDUPSID': '1F020769C39164920A1FDCF9AD0879B1',
        'PSTM': '1719288743',
        'BAIDUID': '1F020769C39164920A1FDCF9AD0879B1:FG=1',
        'H_WISE_SIDS_BFESS': '60276_60334_60372',
        'BA_HECTOR': 'al8h2k8k800081a4a5ak2lak0bgaik1jin2ed1u',
        'BAIDUID_BFESS': '1F020769C39164920A1FDCF9AD0879B1:FG=1',
        'ZFY': 'QVTd2gQKGqBwUd3RFP3yzG7EN:ADOFnHvmqWYJpDXq28:C',
        'log_guid': '574a6f14dcce0cd81d8f5dd2383ad8cb',
        '_j47_ka8_': '57',
        'BDPPN': '756024c753e35d5357573d82a00456bf',
        'login_type': 'passport',
        'in_source': '',
        'log_chanel': '',
        'entry': '1301',
        'H_PS_PSSID': '60276_60976_61027_61036_61055',
        'H_WISE_SIDS': '60276_60976_61027_61036_61055',
        'ab173094840': '37e29e498a485add55c941f7867f8f121730951919974',
        'Hm_lvt_ad52b306e1ae4557f5d3534cce8f8bbf': '1730950204,1730950950,1730951658,1730952809',
        'HMACCOUNT': '74E03469813A9187',
        'log_first_time': '1730952809080',
        'ppfuid': 'FOCoIC3q5fKa8fgJnwzbE67EJ49BGJeplOzf+4l4EOvDuu2RXBRv6R3A1AZMa49I27C0gDDLrJyxcIIeAeEhD8JYsoLTpBiaCXhLqvzbzmvy3SeAW17tKgNq/Xx+RgOdb8TWCFe62MVrDTY6lMf2GrfqL8c87KLF2qFER3obJGkHJI5+HejCI+YBMRTRlDLcGEimjy3MrXEpSuItnI4KD/NdbETTXVM/HiVYi+p9C7CxTCPSdVRLNIHr8AOsArK5bzU2pJXOqMxuSsjck7x1XxJsVwXkGdF24AsEQ3K5XBbh9EHAWDOg2T1ejpq0s2eFy9ar/j566XqWDobGoNNfmfpaEhZpob9le2b5QIEdiQcF+6iOKqU/r67N8lf+wxW6FCMUN0p4SXVVUMsKNJv2T7rJLWgnpOIt4YoCI7gnPiHasmgOrJ40n63OsKSOpoSLs44C79cnwEM1bKFV00Jh1mB1PULpOQ476DSkY5lfAX7Q+//wdrn6SUz7a0vEMm7QqGqBJJILGchC/ZM0axiniVRKx4R3cqVpTVNqTP1tWGnGGu/AVLS3NcPF3XemJkZyi6L0BPA661JDj0lmZIgcCHm0lGODoYWzuL7ZDizBm0d8BJIJUS1lUOPNebjg5OCjwkSq16g64gugrO/OhN+XjRMTNne43cKuMDmex1CEngB2QvyTjxXMcJvDDEe3McIycHFbZmbEY9LT3RuWsSjij5HIeKAxeCJRzKQmiJrt2NexbTUpDMHY3FqKJQQbes2pnRwJmyPPetCsazMsGbpopQep3LV4GbXTxzeIwuufIYh/q1uQn9VsBjBmLNQsYnwiX1i39zQE19TGybrzqrM1pICo4W+Id8GDvscflaNVaQHaBDBV0+6QTz5Y6CfsuieRrNsXbKicl3rMF+gCh2AJdoGcRtGosj9VGpISSuHPrXzYKTGvwJlObLezeBG8hnEWVDGPrlVtFrOI/UAqoYrzvlj69C/hrqQfDCqphLYxCmrXe4z5I+YWwRarkCjOEvrQyd+I5qZTk66qik+zz1X63YHeDpCtd6RMvOgbCfDNICl4LYr1IDPAY5dZv6ZINErg8p7Vi3a5jMXGWL4Mkr0ksENkLZvBJChyDMkf14Hx56V+b2nRqUTK6NqmhPLvsfMNfCwB1HCLk4s0A0zEL1aSR9anh5W7SCFFwD0CtgCptuZDfXvvrhuygE2okEhzyUeNysr3FVnmQ+GG+O0KssWpTzjgymOnBYuzYFgCuiXNRuGYbl2BH/FCzbmQE59lyoCwCARd+2gYcoj1jwDnmFwagA==',
        'BDUSS': 'kdsdlg5VU5ORm9mS0U2bVVUaTlaNjA4YnEtMlFMay1xRUwzU2Rlb3E3LUZ5MU5uSUFBQUFBJCQAAAAAAAAAAAEAAACksY~2Y3MyNDgwNDE5MTcyAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIU-LGeFPixnN',
        'BDUSS_BFESS': 'kdsdlg5VU5ORm9mS0U2bVVUaTlaNjA4YnEtMlFMay1xRUwzU2Rlb3E3LUZ5MU5uSUFBQUFBJCQAAAAAAAAAAAEAAACksY~2Y3MyNDgwNDE5MTcyAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIU-LGeFPixnN',
        '_t4z_qc8_': 'xlTM-TogKuTw%2ATjGL4XvEWcZ7ppS6N169gmd',
        '_fb537_': 'xlTM-TogKuTwajj51%2AX10imt1JwiFnFmaT%2AgkdwgDKke5rwEbKBvMgT9aiPiTCqEhS21xv3xY8tabg7t3Y0ldNEmd',
        'delPer': '0',
        'PSINO': '3',
        'BDORZ': 'B490B5EBF6F3CD402E515D22BCDA1598',
        'Hm_lpvt_ad52b306e1ae4557f5d3534cce8f8bbf': '1730953252',
        'ab_sr': '1.0.1_MGM5NWM1NzczMTkwY2FjMTljMDA5NDExNzc5YmYxMzI3ZWI3MGE1MTFmOGFlNGFhNDBmNTY4MTJlYTJhYTdkZTFhN2VmYWY4YmY2ZmQ3NTAwNTMzNGQ5YTk3Yjc2YWM3YzRhNmY4NGFlYmVhMGFjZGQ1NGMzNDBiMzMzNmY3NjczYjhmMTFiMWVjMjVmY2MxZjZiNjdmMzRhOTVhNDc3OTEyOWFkMjcxYTYzZjc2ZDczZjlkOWE3NzJhOTNiMDY4OTc5Y2RjMmU4NzY5YTJhYzVkYTlmODk3OWUzMDAxMWM=',
        '_s53_d91_': '92dd502652601ecd306ab07ce115801e18401b15b72b13488b985fad6a91eac735248becbf96673b23df0fd69f902d4bba2e63a51156c17b802558403e2d74017415d64be8160c24ab2c2df50a6a4016ff4729512befa6cd8b2dc83a687eef0d6bded3ab926c66688988384736530224f0354371fc1b6dcdce4919d25ff8b671f45390998c4396900fbc0c4b469276c1ce1eeddae326a885d063bbd7c707778bee2600c9d7ac11404282e342154165f477438dbda0eb2518eb0d5877b6b085e8d41ff1c4b0445d1c0e44c32451242f808735f32793a6b62053900e21a50bbb97eb4ed56dc34325851cf23107a478f9ff',
        '_y18_s21_': '729bb8bd',
        'log_last_time': '1730953278194',
        'RT': '"z=1&dm=baidu.com&si=4d93b286-dc5c-4159-9e94-9a7239af5616&ss=m36r23tm&sl=3c&tt=2f6j&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf"',
        'ab173095200': '35e29e498a485add55c941f7867f8f121730953279274',
    }

    param = {
        'p': page,
        's': '10',
        'f': '{"provinceCode": ["430000"], "openStatus": ["开业"]}',
        'o': 0,
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        # 'Cookie': 'BIDUPSID=1F020769C39164920A1FDCF9AD0879B1; PSTM=1719288743; BAIDUID=1F020769C39164920A1FDCF9AD0879B1:FG=1; H_WISE_SIDS_BFESS=60276_60334_60372; BA_HECTOR=al8h2k8k800081a4a5ak2lak0bgaik1jin2ed1u; BAIDUID_BFESS=1F020769C39164920A1FDCF9AD0879B1:FG=1; ZFY=QVTd2gQKGqBwUd3RFP3yzG7EN:ADOFnHvmqWYJpDXq28:C; log_guid=574a6f14dcce0cd81d8f5dd2383ad8cb; _j47_ka8_=57; BDPPN=756024c753e35d5357573d82a00456bf; login_type=passport; in_source=; log_chanel=; entry=1301; H_PS_PSSID=60276_60976_61027_61036_61055; H_WISE_SIDS=60276_60976_61027_61036_61055; ab173094840=37e29e498a485add55c941f7867f8f121730951919974; Hm_lvt_ad52b306e1ae4557f5d3534cce8f8bbf=1730950204,1730950950,1730951658,1730952809; HMACCOUNT=74E03469813A9187; log_first_time=1730952809080; ppfuid=FOCoIC3q5fKa8fgJnwzbE67EJ49BGJeplOzf+4l4EOvDuu2RXBRv6R3A1AZMa49I27C0gDDLrJyxcIIeAeEhD8JYsoLTpBiaCXhLqvzbzmvy3SeAW17tKgNq/Xx+RgOdb8TWCFe62MVrDTY6lMf2GrfqL8c87KLF2qFER3obJGkHJI5+HejCI+YBMRTRlDLcGEimjy3MrXEpSuItnI4KD/NdbETTXVM/HiVYi+p9C7CxTCPSdVRLNIHr8AOsArK5bzU2pJXOqMxuSsjck7x1XxJsVwXkGdF24AsEQ3K5XBbh9EHAWDOg2T1ejpq0s2eFy9ar/j566XqWDobGoNNfmfpaEhZpob9le2b5QIEdiQcF+6iOKqU/r67N8lf+wxW6FCMUN0p4SXVVUMsKNJv2T7rJLWgnpOIt4YoCI7gnPiHasmgOrJ40n63OsKSOpoSLs44C79cnwEM1bKFV00Jh1mB1PULpOQ476DSkY5lfAX7Q+//wdrn6SUz7a0vEMm7QqGqBJJILGchC/ZM0axiniVRKx4R3cqVpTVNqTP1tWGnGGu/AVLS3NcPF3XemJkZyi6L0BPA661JDj0lmZIgcCHm0lGODoYWzuL7ZDizBm0d8BJIJUS1lUOPNebjg5OCjwkSq16g64gugrO/OhN+XjRMTNne43cKuMDmex1CEngB2QvyTjxXMcJvDDEe3McIycHFbZmbEY9LT3RuWsSjij5HIeKAxeCJRzKQmiJrt2NexbTUpDMHY3FqKJQQbes2pnRwJmyPPetCsazMsGbpopQep3LV4GbXTxzeIwuufIYh/q1uQn9VsBjBmLNQsYnwiX1i39zQE19TGybrzqrM1pICo4W+Id8GDvscflaNVaQHaBDBV0+6QTz5Y6CfsuieRrNsXbKicl3rMF+gCh2AJdoGcRtGosj9VGpISSuHPrXzYKTGvwJlObLezeBG8hnEWVDGPrlVtFrOI/UAqoYrzvlj69C/hrqQfDCqphLYxCmrXe4z5I+YWwRarkCjOEvrQyd+I5qZTk66qik+zz1X63YHeDpCtd6RMvOgbCfDNICl4LYr1IDPAY5dZv6ZINErg8p7Vi3a5jMXGWL4Mkr0ksENkLZvBJChyDMkf14Hx56V+b2nRqUTK6NqmhPLvsfMNfCwB1HCLk4s0A0zEL1aSR9anh5W7SCFFwD0CtgCptuZDfXvvrhuygE2okEhzyUeNysr3FVnmQ+GG+O0KssWpTzjgymOnBYuzYFgCuiXNRuGYbl2BH/FCzbmQE59lyoCwCARd+2gYcoj1jwDnmFwagA==; BDUSS=kdsdlg5VU5ORm9mS0U2bVVUaTlaNjA4YnEtMlFMay1xRUwzU2Rlb3E3LUZ5MU5uSUFBQUFBJCQAAAAAAAAAAAEAAACksY~2Y3MyNDgwNDE5MTcyAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIU-LGeFPixnN; BDUSS_BFESS=kdsdlg5VU5ORm9mS0U2bVVUaTlaNjA4YnEtMlFMay1xRUwzU2Rlb3E3LUZ5MU5uSUFBQUFBJCQAAAAAAAAAAAEAAACksY~2Y3MyNDgwNDE5MTcyAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIU-LGeFPixnN; _t4z_qc8_=xlTM-TogKuTw%2ATjGL4XvEWcZ7ppS6N169gmd; _fb537_=xlTM-TogKuTwajj51%2AX10imt1JwiFnFmaT%2AgkdwgDKke5rwEbKBvMgT9aiPiTCqEhS21xv3xY8tabg7t3Y0ldNEmd; delPer=0; PSINO=3; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; Hm_lpvt_ad52b306e1ae4557f5d3534cce8f8bbf=1730953252; ab_sr=1.0.1_MGM5NWM1NzczMTkwY2FjMTljMDA5NDExNzc5YmYxMzI3ZWI3MGE1MTFmOGFlNGFhNDBmNTY4MTJlYTJhYTdkZTFhN2VmYWY4YmY2ZmQ3NTAwNTMzNGQ5YTk3Yjc2YWM3YzRhNmY4NGFlYmVhMGFjZGQ1NGMzNDBiMzMzNmY3NjczYjhmMTFiMWVjMjVmY2MxZjZiNjdmMzRhOTVhNDc3OTEyOWFkMjcxYTYzZjc2ZDczZjlkOWE3NzJhOTNiMDY4OTc5Y2RjMmU4NzY5YTJhYzVkYTlmODk3OWUzMDAxMWM=; _s53_d91_=92dd502652601ecd306ab07ce115801e18401b15b72b13488b985fad6a91eac735248becbf96673b23df0fd69f902d4bba2e63a51156c17b802558403e2d74017415d64be8160c24ab2c2df50a6a4016ff4729512befa6cd8b2dc83a687eef0d6bded3ab926c66688988384736530224f0354371fc1b6dcdce4919d25ff8b671f45390998c4396900fbc0c4b469276c1ce1eeddae326a885d063bbd7c707778bee2600c9d7ac11404282e342154165f477438dbda0eb2518eb0d5877b6b085e8d41ff1c4b0445d1c0e44c32451242f808735f32793a6b62053900e21a50bbb97eb4ed56dc34325851cf23107a478f9ff; _y18_s21_=729bb8bd; log_last_time=1730953278194; RT="z=1&dm=baidu.com&si=4d93b286-dc5c-4159-9e94-9a7239af5616&ss=m36r23tm&sl=3c&tt=2f6j&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf"; ab173095200=35e29e498a485add55c941f7867f8f121730953279274',
        'Referer': 'https://aiqicha.baidu.com/advancesearch/list',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Zx-Open-Url': 'https://aiqicha.baidu.com/advancesearch/list',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'ymg_ssr': '1730884031918_1730953279313_A5Ycwep2v/fpmcQpCNXLB3QUtRz4bYU6jTALKQ2kJhyEzKGWsfOTJkUNBSVSpclXso5esWcC0/zDyWQ0KruZ85zZCMrgnhNTY11iTIi+ZIlZCy4bba0AASl3OY3wtei/5zJrZCPzGoRJjpDDSyyU/ZuDK+EKDhPzCNpMxIzg0/maj2q8NX+0W2AmCghy9OPps/mbABo47HwKxF3VcF1DirvaAUW6hG2CkghEdhX5VnWPcgU8PZgcVRQSCYOVPt8pK3MUot4IV53tMQVtn5iviBBnvz2xb07RatsO6SE2Sd7iq1Tdh3Kd84BohpolVW3x',
    }

    response = requests.get(
        url=url,
        params=param,
        cookies=cookies,
        headers=headers,
        verify=False
    )

    data = response.json()
    return data


# 保存数据
def save_data(info_dic):
    print(info_dic)
    with open('data.json', 'a+', encoding='utf-8') as f:
        json.dump(info_dic, f, ensure_ascii=False, indent=4)

    print('数据已保存到data.json')


# 获取数据：企业名 + pid

def get_name_pid(data):
    entNames = jsonpath(data, '$.data.resultList..entName')
    pids = jsonpath(data, '$.data.resultList..pid')
    # print(entNames, pids, len(entNames), len(pids))
    info_dic = dict(zip(entNames, pids))
    lst.append(info_dic)


if __name__ == '__main__':
    lst = []  # 最终数据
    for i in range(1, 3):
        data = get_data(i)
        print(data)
        get_name_pid(data)
        time.sleep(3)
    save_data(lst)
