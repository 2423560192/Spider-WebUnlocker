import requests

cookies = {
    '_zap': 'cbd9bf96-9231-488c-99d2-d2b9abea4f05',
    'd_c0': 'ABBSEgfH0xiPTo0_lZbq9ypo4haE1N_vIfs=|1719309004',
    '_xsrf': 'bClPqW30QSwYLLWBAwWvkLzkFVcgrPId',
    'captcha_session_v2': '2|1:0|10:1737623184|18:captcha_session_v2|88:N3hrc3hxeWUza0swKzlwRlp3dGpVbHFwOTZmbGU2VjAyaGE3YnBGMXRhSWxsbkFsYktrbTNxcTNSYjFJR0NNeA==|f0a04ede10243a3272807956dba52d668cb2bcff2682df2b872dd272f049b6b5',
    '__snaker__id': 'K2Pwm5Xx72SbBYKK',
    'gdxidpyhxdE': 'rRrJ5ZEGRAayU%2BJhGDfO783uL8jq29Uj6xIl3%2BNl9h4twGrmcgbd4pTkQDuRb4Kdit4j%5CIJDmOO5ELHb2rvPv92xRl1ORSkmh0YT41g%2FNmWgaZAlzllVNebWwR6Krfq4RZ0fI%2F5Mhhv%2FVn%2FeEacJHpQ%2BA8e%5CJy7SEoNIPvXLKgGzKuUJ%3A1737624083385',
    'q_c1': '2193fc7b42d34eb8a9bc28a9d41e90ad|1737623189000|1737623189000',
    'z_c0': '2|1:0|10:1737623192|4:z_c0|92:Mi4xeEk0ZVJnQUFBQUFBRUZJU0I4ZlRHQmNBQUFCZ0FsVk5sVlJfYUFBZnhQcVQtTjBhOTFxOHhPeE1vNHVWbUxPQ2pn|a4949c1dbe704190ba5536f8ee38d6fc8bb583db0af965f4ee506da06415af12',
    '__zse_ck': '004_6LbHXvpZUiwbJzQXJulaJrEPTwiBOIrRt25f50sBS8y11JvdFgYL1E5okiv24ilu/0Bbn0PT1ABcUxhun00fyJdIdIBvoh7l3TS4WPNrOEd=iHkusFFWSImHqec8m=Zi-i3F3Ainn33yjwlQ3Dl6duAREABdF2Azx/MTLbI+pvUs/0Hd32xR8uBQilQUh9VauVSwOOOorwTuALzAnl/AZs51TLg7B9aeFysS8EhYXZQotTNgQHURXfpV19J051euB',
    'Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49': '1736383101,1737095296,1737623182,1738142117',
    'HMACCOUNT': '74E03469813A9187',
    'SESSIONID': 'pEDMzWf22WeChTgBzIK8b4HzDYqKPlQ1irxeYgaNMqq',
    'JOID': 'W1oTCkihGhbUmTq9N6BLixxuGDYh2ltdk-lm3wqZRneY-2TRcQLgirOYNbYyK6STWuocxlhCS_Y9-8eY9sNL71Y=',
    'osd': 'V1kTAUytGRbfnTa-N6tPhx9uEzIt2VtWl-Vl3wGdSnSY8GDdcgLrjr-bNb02J6eTUe4QxVhJT_o--8yc-sBL5FI=',
    'Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49': '1738142338',
    'tst': 'r',
    'BEC': 'd6322fc1daba6406210e61eaa4ec5a7a',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    # 'cookie': '_zap=cbd9bf96-9231-488c-99d2-d2b9abea4f05; d_c0=ABBSEgfH0xiPTo0_lZbq9ypo4haE1N_vIfs=|1719309004; _xsrf=bClPqW30QSwYLLWBAwWvkLzkFVcgrPId; captcha_session_v2=2|1:0|10:1737623184|18:captcha_session_v2|88:N3hrc3hxeWUza0swKzlwRlp3dGpVbHFwOTZmbGU2VjAyaGE3YnBGMXRhSWxsbkFsYktrbTNxcTNSYjFJR0NNeA==|f0a04ede10243a3272807956dba52d668cb2bcff2682df2b872dd272f049b6b5; __snaker__id=K2Pwm5Xx72SbBYKK; gdxidpyhxdE=rRrJ5ZEGRAayU%2BJhGDfO783uL8jq29Uj6xIl3%2BNl9h4twGrmcgbd4pTkQDuRb4Kdit4j%5CIJDmOO5ELHb2rvPv92xRl1ORSkmh0YT41g%2FNmWgaZAlzllVNebWwR6Krfq4RZ0fI%2F5Mhhv%2FVn%2FeEacJHpQ%2BA8e%5CJy7SEoNIPvXLKgGzKuUJ%3A1737624083385; q_c1=2193fc7b42d34eb8a9bc28a9d41e90ad|1737623189000|1737623189000; z_c0=2|1:0|10:1737623192|4:z_c0|92:Mi4xeEk0ZVJnQUFBQUFBRUZJU0I4ZlRHQmNBQUFCZ0FsVk5sVlJfYUFBZnhQcVQtTjBhOTFxOHhPeE1vNHVWbUxPQ2pn|a4949c1dbe704190ba5536f8ee38d6fc8bb583db0af965f4ee506da06415af12; __zse_ck=004_6LbHXvpZUiwbJzQXJulaJrEPTwiBOIrRt25f50sBS8y11JvdFgYL1E5okiv24ilu/0Bbn0PT1ABcUxhun00fyJdIdIBvoh7l3TS4WPNrOEd=iHkusFFWSImHqec8m=Zi-i3F3Ainn33yjwlQ3Dl6duAREABdF2Azx/MTLbI+pvUs/0Hd32xR8uBQilQUh9VauVSwOOOorwTuALzAnl/AZs51TLg7B9aeFysS8EhYXZQotTNgQHURXfpV19J051euB; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1736383101,1737095296,1737623182,1738142117; HMACCOUNT=74E03469813A9187; SESSIONID=pEDMzWf22WeChTgBzIK8b4HzDYqKPlQ1irxeYgaNMqq; JOID=W1oTCkihGhbUmTq9N6BLixxuGDYh2ltdk-lm3wqZRneY-2TRcQLgirOYNbYyK6STWuocxlhCS_Y9-8eY9sNL71Y=; osd=V1kTAUytGRbfnTa-N6tPhx9uEzIt2VtWl-Vl3wGdSnSY8GDdcgLrjr-bNb02J6eTUe4QxVhJT_o--8yc-sBL5FI=; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1738142338; tst=r; BEC=d6322fc1daba6406210e61eaa4ec5a7a',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.zhihu.com/',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'x-api-version': '3.0.53',
    'x-requested-with': 'fetch',
    'x-zse-93': '101_3_3.0',
    'x-zse-96': '2.0_nZL0sM4SFqqn6UOkUJgiBWtKZ240V9sCKwByQuPdRm5+RdM46YaVMA50KVpIkTDt',
    'x-zst-81': '3_2.0aR_sn77yn6O92wOB8hPZnQr0EMYxc4f18wNBUgpTQ6nxERFZ80Y0-4Lm-h3_tufIwJS8gcxTgJS_AuPZNcXCTwxI78YxEM20s4PGDwN8gGcYAupMWufIeQuK7AFpS6O1vukyQ_R0rRnsyukMGvxBEqeCiRnxEL2ZZrxmDucmqhPXnXFMTAoTF6RhRuLPFTwmpDS16A9fAhLpTvO05BOGog3GiJX9hgC97u3f1JOybMtL6u3CH9C1o7STvHXmcQH_Bck8bh9ZJ4OGLDX14UVLe4LCLCxpIht0TbH8J7g1krLYF9x9JUYOY9eLHGLV2QNCpQSCer30egXLwCVyfUxLerUYJXNsEBN86GXGbvV_LJSxOqfzGw2q_uSMsqcY64wyK8OLthC06Cc1cGwOvBYfe038qDcV0GSBTwe81cU0J0SfE9wCmG30ErOBJ9SXrTtMG9e9rJuK3hX1SeXyUDo1CBxKpuV8WqXOBwYC',
}

params = {
    'action': 'down',
    'ad_interval': '-10',
    'after_id': '17',
    'desktop': 'true',
    'end_offset': '17',
    'page_number': '5',
    'session_token': '8009b3e1e67338abe7d67d155c6f2768',
}

response = requests.get('https://www.zhihu.com/api/v3/feed/topstory/recommend', params=params, cookies=cookies, headers=headers)


print(response.json())