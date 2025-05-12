def get_ip():
    import requests

    # 提取代理API接口，获取1个代理IP
    api_url = "https://dps.kdlapi.com/api/getdps/?secret_id=o9ntciol602nhd4d0r8e&signature=nifj9hzd3kpty6umri0kwliwfhjl8fnb&num=1&pt=1&format=json&sep=1"

    # 获取API接口返回的代理IP
    proxy_ip = requests.get(api_url).json()
    proxy_ip = proxy_ip['data']['proxy_list'][0]

    # 用户名密码认证(私密代理/独享代理)
    username = "d2074621077"
    password = "nhrxmo0g"
    proxies = {
        "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip},
        "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip}
    }
    return proxies