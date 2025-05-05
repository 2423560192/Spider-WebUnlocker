import requests
from jsonpath import jsonpath

class Spider:
    def __init__(self):
        self.session = requests.Session()
        headers = {
            'Host': 'ebeikeapi.ebeck.cn',
            'xweb_xhr': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c33)XWEB/11581',
            'Content-type': 'application/json;charset=UTF-8',
            'accept': '*/*',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://servicewechat.com/wx51a2021dd921f747/244/page-frame.html',
            'accept-language': 'zh-CN,zh;q=0.9',
        }
        self.session.headers.update(headers)



    def search(self):
        """
        搜索某个商品
        :return:
        """
        json_data = {
            'version': '251',
            'client': 'wxmp',
            'search_value': '火锅',
            'city_id': 500100,
            'page': 1,
            'page_size': 10,
        }
        response = self.session.post('https://ebeikeapi.ebeck.cn/api/bargain/search', json=json_data)

        data = response.json()
        origin_prices = jsonpath(data , '$.data..origin_price')
        ids = jsonpath(data , '$.data..id')
        goods_names = jsonpath(data , '$.data..goods_name')





