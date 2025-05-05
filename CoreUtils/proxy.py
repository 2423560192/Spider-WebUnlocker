import requests


def get_proxy():
    """从代理API获取代理地址"""
    proxy_api = 'http://api2.xkdaili.com/tools/XApi.ashx?apikey=XK69862370B1CA650629&qty=1&format=txt&split=0&sign=87a269171ead05ba5185eba8eb5a162a&time=3'
    try:
        response = requests.get(proxy_api, timeout=10)
        response.raise_for_status()
        proxy_address = response.text.strip()
        if not proxy_address:
            print("代理API返回空地址")
            return None
        print(f"成功获取代理地址：{proxy_address}")
        return {'http': f'http://{proxy_address}', 'https': f'http://{proxy_address}'}
    except Exception as e:
        print(f"获取代理失败：{e}")
        return None