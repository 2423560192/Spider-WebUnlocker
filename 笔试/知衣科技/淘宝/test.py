import requests


headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9",
    "bx-v": "2.5.22",
    "cache-control": "no-cache",
    "content-type": "application/x-www-form-urlencoded",
    "eagleeye-pappname": "gf3el0xc6g@256d85bbd150cf1",
    "eagleeye-sessionid": "7dmeXaRInmbdpez9FvjvmFkhmU04",
    "eagleeye-traceid": "14b20b6e1747193691217101150cf1",
    "origin": "https://login.taobao.com",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://login.taobao.com/havanaone/login/login.htm?bizName=taobao&redirectURL=https%3A%2F%2Fi.taobao.com%2Fmy_itaobao%3Fspm%3Dpc_detail.29232929%2Fevo365560b447259.1997525045.1.36647dd6hzGE6k",
    "sec-ch-ua": "\"Chromium\";v=\"136\", \"Google Chrome\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
}
cookies = {
    "XSRF-TOKEN": "6e49db30-2d0c-4486-aab1-fb3c1dc6441f",
    "_samesite_flag_": "true",
    "cookie2": "175d2764148381a1480a760aca368ce0",
    "t": "52362914eedb2269b995a5e9344af16f",
    "_tb_token_": "e17351b38b196",
    "tfstk": "gWvsv7jJiP4sEHBYc1mFVUYzyeXXHDkPMosvqneaDOBtcETJ5s5AufYfGE8hMdWwbeZXu3oGgfXwG-_pJN8w_n8IceLkbs-v3ipfIpRa3NuGhnLPh4urUY-MjsXxz4SWQv-FeisTWZU4vMBVcXrvUhKMjtXxKdCivhqfrsIwDtLAp6IRVtFOHEHdJwjcDPIYBDiC-gSADiIYJJINDtQvktnCJwjfHGLAHxwgViG1ShiGpSqwNk0BbwwYHpsKowK_yJSXQGN5zh_IyqJQE1_JXwwxWe8n7Z_He2lBxBd97MYjF26D-ILAceUKu1xvOes674acudxwhN-s6VxCpNTO1Bi8sMteCnOAOcH9AO_1apTT05X6MFvfsCZmqHB9-Qbl6X0hAdJPGafQJVKeANCWGFu3HNRWve1yLyyPneAvkiTL5gr_UaOsFSZCZ-sCzDiQiSmCzDyncdYyT1Ihf6oIAPdc6MjCzDiQiSfOxG_EADa9i"
}
url = "https://login.taobao.com/havanaone/loginLegacy/password/login.do"
params = {
    "bizEntrance": "taobao_pc",
    "bizName": "taobao"
}
data = {
    "loginId": "17782200192",
    "password2": "4ce27db5e49dc222fbf05edd610d833c61b1052c1d0b4efd6cd012fb3033f4399d64631d4d41b41fa406ca0a9b19919f696554a9837cbdfcfef3f6e8b0756028ae953b7347d7e6cc0bbcf2867cdb9184fe2df021180f47e2c6f7397025450249d2652aa39ea72a1d2d64e85554830af9b58f583ebd8f46a4454b21cfc5395a16a5d54a483e0959a5a20a26c9dd38845921ced377f119336c5697deea8b3a2ee1f67aba85137470b4687f8e95637010083d5da9ac85a9a8cbfdd2723a6cbc65edcc71658b9b0a70bc9c725a93c0a3ed915f7295f207b5b332452fcbc0b1613f994e7d9701da2dae529f3cefc91d4644f1b6ed2686f2cc2e7de2a49246c5fd53b4",
    "keepLogin": "false",
    "isIframe": "false",
    "banThirdPartyCookie": "false",
    "documentReferer": "https://i.taobao.com/my_itaobao?spm=pc_detail.29232929/evo365560b447259.1997525045.1.36647dd6hzGE6k",
    "defaultView": "sms",
    "ua": "",
    "umidGetStatusVal": "",
    "screenPixel": "1920x1080",
    "navlanguage": "zh-CN",
    "navUserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "navPlatform": "Win32",
    "hitRSA2048Gray": "true",
    "bizEntrance": "taobao_pc",
    "bizName": "taobao",
    "renderRefer": "https://i.taobao.com/my_itaobao?spm=pc_detail.29232929/evo365560b447259.1997525045.1.36647dd6hzGE6k",
    "_csrf": "625425590f360bea36ca21ac5a529399",
    "returnUrl": "https://i.taobao.com/my_itaobao?spm=pc_detail.29232929/evo365560b447259.1997525045.1.36647dd6hzGE6k",
    "lang": "zh_CN",
    "umidToken": "",
    "umidTag": "NOT_INIT",
    "weiBoMpBridge": "",
    "jsVersion": "0.10.25",
    "deviceId": "KAJsH9kP0n4CAXuT+UD32lk5",
    "pageTraceId": "213e366217471936647095898e7b99",
    "bx-ua": "231\\u0021Vw07DAmUH7R j7M4ZA3ijhzjUa6lfXVofsOi7dqX7BwQbpJYvo1O75syTD B02icBpz5J3 EdqTHgpG7c7CqngY4VJktUw3WtTonmf9DRnDXQDMRSiKZvQ/Tf/qeTt3gQOvvd3 M7En8xHpn2tYSFnlUmDxTj8aJWlWQuJeK89QyotqOKQrJgz mNNX2TsG25/Brbz3b55bI4KNfqiD Eu8e Zd  6WF1cs eITXHJBh   j ygU3 jOKHDDQU QF k3kwyxbBX50NTEUhLCo/I4uzpOQPK5ZgIxM bmhG65/Cy XTpOt933uhAyTdaoP2gc7F4YCgEADjU nTigce X5r3wCaFtf skWJDKlz0EeuVghv1xlcg wHCUwLGKQmfkIIiturIdigirZieWLV/UwmpPk1slY3JanRqi/w7OjophgW9nNPHhjQZ4l9s 4XEB8JaDtK/iJTF3349/pvTYnKMmpIszmgv3khyaRadtfPivYqc/X5AR4LCS5MTKINHCxA4b1JCTd1IxH4rtYL86HqYbrW I/GTvxxf6qxcbQbZthXGz7qJeDrw0c899gaC8yyC7X 2eeT/Lzjtw7HzwaMNkNLnmzwo2QlbISR9gy7p3ezY3m4KOJkWj PKbgiDmJ37iJwll fg1CuSf1JbNAQAZcCn7IOWMLrVtlPmp9tbZmdhpzdBA9oAIHrCWynO/ IuedgTBrHYX/bdd/MLrXovAbNh5hQmBeQSYOKpGB91fJyllTflqjO9CovFGoLiebN7PPNebDSKGWOL16f04puoOmOpk0yczuJ4Au0Zj3VeP8tr lJ1e5G4f1CEhsaQCyab8Y9EXDeOz8 XPgM25RJMyVsZFogs2r4oLmthjzW2bPJJG85wOo2QLhgKbK80TSPk4nc/WaKsR/rHoWbqkGEYOtJkTHhNASFuBrU8IePspBsMXaQVPD7IK1DG8naJGKpSH9WCNla4V3megoicYh0haOUopetGQKBangIwSEHXabOCNJIxambD U9fCvzSbBTvOeh6c gnJnTO5uL3s00sAOg5GaNarZX1jfR jtvE4uDy2Mw4CM1zqT1jd0MI6Dj5lSuMben/aUHSExaDf8GIePqJhIXBSBL09Q4U9V6FgW2jcoLlTJ CdHwLcsw2RTqWd0h3IBkEL8XBwmvZlTk04aq AgC6mybl1n/RlkhocM6awGyQw /kCipyf6aeySCajqZjrSMqDsLk0avpRtZYqtKn6sFnINGXp62RfalhjQ6E C/udx/6wxH8sMpZ215bJCxsB3WZK8zixcIms4PtjyjJJ1XzwkkIAJqJDPqCfK5CDQjyD6HF zBYZJGDnJAHQXhJShSEVuFOyUUOgvlg2it0zO0VUhxTl1aXrjvGF9qe3zmB76uPOQIeNYMUpCH/WdE0/Y7BQyS8Xns4j32sSia9Akn14 RHStaDGZSl5xQYfOdFN7Rw8oKkyutmIFaUfRoUTWLtq6sA03lmCedRZXeZaz1TFcivKf3OXtdDhFSK81HtMrJZ0lIk0mI8Q TljcFXjwgst1dwxAZ6PSLVgHiOg90I0E4eiBpQVAGA2yCYN3U79F7md9gQHd9eKYvFrnIK9 CTogBaAx0CKPmrQNWIgHUvWr14mz3uUF84 WtERO30mBLe/B917SU1FWlkz//nxh1uZfqUF95tqNKvkuHd OdF6ZicCwK/4mtf0Ms0b/4Zdo5DJKxOAfOfWXayWjWGWAJCBhI7r37BD2C0F0/Gq4FHK0BreVA==",
    "bx-umidtoken": "T2gAJFYexKnWIpivZX7tluA7KflIqkWwvm9AoAFOHcLXkyksiyFdrOeJxV5fP6HPrXU=",
    "bx_et": "gd-qYPMwAmn2yGfAo3sa8MFRasjAlGlCIh11IdvGhsfD1iNZbQ57fxIjWGRNaCCflix1bPA6NxCXCxdrQQAphNsD1CPwGQ_M119bHUdBKotjkGZNDGIiOXiIAK9AXGm-yO6QHgXO3Pm1ssvlDOwzIB9mAKpAXrKcHYmQQTSkkifMsZbuZ91uo1AgjLDPION0SoAiUYWGdoX0m1flr96Gj1AGjYJlwOSGICjiLL9DIuWCoAM3dFhZpS7ctKcic0ed6ZVDCPZ0m3WVuhvVaT6W4t7VtNjSR6-DNdxXDahUtGpW8C8M62aR0dYcm99x0uSHnUtNFhM_7sAv4LxAzJrFbEA2SwLrvyQc7s8kmaygjLIkrwTwgjzAiEOPJTbuQDBWO_vvmUkTZKACgiXlPDDeENYWDwKjZoSHJKsXSC3QyiJMogSrf5Buu-t9u54NoTBPOYkyd-gYROzliezTWajdU6MfhPUOoTBPOYkzWPQlpT5Iht1.."
}
response = requests.post(url, headers=headers, cookies=cookies, params=params, data=data)

print(response.text)
print(response)