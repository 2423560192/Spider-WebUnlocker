import json
import time

import requests
from jsonpath import jsonpath

from utils import get_sign

import json


class TaobaoSpider:
    def __init__(self):
        self.session = requests.Session()

        self.session.headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'referer': 'https://s.taobao.com/search?_input_charset=utf-8&commend=all&ie=utf8&initiative_id=tbindexz_20170306&page=1&preLoadOrigin=https%3A%2F%2Fwww.taobao.com&q=%E5%B0%8F%E4%BC%97%E7%88%86%E6%AC%BEt%E6%81%A4&search_type=item&source=suggest&sourceId=tb.index&spm=a21bo.jianhua%2Fa.search_guessRecommend.d3&ssid=s5-e&suggest_query=&tab=all&wq=',
            'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'script',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Mobile Safari/537.36',
            # 'cookie': 'thw=cn; tracknick=tb731460888397; havana_lgc2_0=eyJoaWQiOjIyMTcxMDI1NjM1ODQsInNnIjoiOGMyMDA0Y2RjZGI3YjNjOTExMjY5NWI1YjFkYzFkMzciLCJzaXRlIjowLCJ0b2tlbiI6IjE2aWF1eHpiYTM1c0dNaWg0aGVyY2FBIn0; _hvn_lgc_=0; wk_cookie2=1d756b3a187533920d689f5408cbadaa; wk_unb=UUpgQcOgsD8Saq3fcQ%3D%3D; t=e61a24da1f3a109eec7ccde9acabecaa; cna=KAJsH9kP0n4CAXuT+UD32lk5; mtop_partitioned_detect=1; _m_h5_tk=001908c2a5c1c6941d30c348836ffe94_1747144923799; _m_h5_tk_enc=56fab20ca2f1254336770cc34769f81c; _samesite_flag_=true; sgcookie=E100zeueOQ7WLh89ZfEBjvzKAYPlXOtrJWzEn%2By5QhyCp6VYjUItvydsN3NMzQZ6L32JziXIqhRGJMZzVWrymF3swatYb7aeluetj5ViNkQi6KQ%3D; havana_lgc_exp=1778238485868; unb=2217102563584; uc1=cookie15=UtASsssmOIJ0bQ%3D%3D&existShop=false&pas=0&cookie14=UoYajLSWFpUaRg%3D%3D&cookie21=URm48syIYRhCU6d3XQ%3D%3D&cookie16=Vq8l%2BKCLySLZMFWHxqs8fwqnEw%3D%3D; sn=; uc3=id2=UUpgQcOgsD8Saq3fcQ%3D%3D&nk2=F5RCZsqZNSA79LhfJxs%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D&vt3=F8dD2EXfK%2BqkPepqsDI%3D; csg=ecdd29c2; lgc=tb731460888397; cancelledSubSites=empty; cookie17=UUpgQcOgsD8Saq3fcQ%3D%3D; dnk=tb731460888397; skt=55e8c9db8af562ef; cookie2=18dc6fb36db58a4d046f9d0157f717a2; existShop=MTc0NzEzNDQ4NQ%3D%3D; uc4=nk4=0%40FY4JiMVL%2BoBpi0FnX4KAZgxCwJWcEh0HKg%3D%3D&id4=0%40U2gqztqNaLsjNlsL2IUEU8S1dlDpJPms; _cc_=WqG3DMC9EA%3D%3D; _l_g_=Ug%3D%3D; sg=745; _nk_=tb731460888397; cookie1=BqPn6PVl6cJ0Nf9ekHVllbAo16bg1uQsOT0TOaHepqU%3D; _tb_token_=e51483e10bbbb; sca=b8075283; havana_sdkSilent=1747220885872; xlly_s=1; sdkSilent=1747221691728; tfstk=gYzjaJGLjKvXnU391mfrOuX1JE06G_7ehCGTt5L26q3xBuN3Cx5GmqrSC8eSHE5cmcH_nqng0AkqCVNgd_WF8wP0iVmOL97ExeRC_VDO7VIrytR-5aWF8wPcDj0aw9zNhutmeX8tWmnOyQHo_AptDRn8wjkJkfLx6LCSEYhx6FnYwYht6dLTBVC7wYctWjetX_N-pO8iaZk_Gs0bQBd1FjPxFFLTPwijdSKwWFUSGmwQMYN4gzGjcvitzK6Yk8PTurmldp3gakw_XRjeqqNTDqhUiZTSJSEz5bzN_hMYnzN8o0OBRVZYhln3VwxnDcMb2rnW6FFoyunUf-6XmxE4FDc-2C_naJk8irE5sLFYLxgxw07dO7nT4rm3uTLjJkVquleGY30b6o354kTEdo_BfhDv5bMFN_tMj7L7rm5CheXxDbcPH_1WAJnxZbMFN_tMjmhoatC5NHwd.; ariaScale=1; ariaDefaultTheme=default; isg=BIWF6NS6QSfdsWu9471ymsLFlMG_QjnU5wRvFIfqRLz9HqmQTpBTpFy4LUToe1GM',
        }

        self.cookie = {
            "_samesite_flag_": "true",
            "cookie2": "175d2764148381a1480a760aca368ce0",
            "t": "52362914eedb2269b995a5e9344af16f",
            "_tb_token_": "e17351b38b196",
            "unb": "2206787696506",
            "uc1": "existShop=false&pas=0&cookie15=VT5L2FSpMGV7TQ%3D%3D&cookie14=UoYajLScRzlGgg%3D%3D&cookie21=VFC%2FuZ9aidsF3vBAgQ%3D%3D&cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D",
            "sn": "",
            "uc3": "lg2=W5iHLLyFOGW7aA%3D%3D&vt3=F8dD2EXfIUA88DsXjc0%3D&nk2=F5RHpC2cIoejhjw%3D&id2=UUphzOV5nsYb%2Bf81eg%3D%3D",
            "csg": "84a1a321",
            "lgc": "tb256721506",
            "cancelledSubSites": "empty",
            "cookie17": "UUphzOV5nsYb%2Bf81eg%3D%3D",
            "dnk": "tb256721506",
            "skt": "3f3681c5c5de4fa2",
            "existShop": "MTc0NzE5NDMwMA%3D%3D",
            "uc4": "nk4=0%40FY4MthPoY97ivHUhM%2Bk6Wu64j1E2rg%3D%3D&id4=0%40U2grF862PT9uTiwTjVJofiu3WPaF89cn",
            "tracknick": "tb256721506",
            "_cc_": "UtASsssmfA%3D%3D",
            "_l_g_": "Ug%3D%3D",
            "sg": "663",
            "_nk_": "tb256721506",
            "cookie1": "WvSbKUmIvCaSCoZwCZArCpjV9oN31apKdqCn1Be9FSM%3D",
            "wk_cookie2": "12dd50cb3a72f253d3b9664d2219ec6c",
            "wk_unb": "UUphzOV5nsYb%2Bf81eg%3D%3D",
            "sgcookie": "E100HcJgsHv5zKzLYvMvnKcik9%2BfWuWSCnNDX3amL9qhKTs3oBl9gOTFeqp3Npk7VL7YU2VLjKntigGnPWGechM1C70XMnL%2BYuEtGvCRuq1cDMA%3D",
            "mtop_partitioned_detect": "1",
            "_m_h5_tk": "2063070def441d557a1d9dae9b7f22d9_1747202582633",
            "_m_h5_tk_enc": "a59be7e45d250d0ad984a5d3f07ea798",
            "bxuab": "0",
            "cna": "KAJsH9kP0n4CAXuT+UD32lk5",
            "aui": "2206787696506",
            "sca": "edc108a1",
            "thw": "cn",
            "xlly_s": "1",
            "tfstk": "g5CxI4vQ5uq0w4fvrZyoIyohS3ao68b4mi7IshxmCgIR53cguI2w6GKRbnvDGnc96NINjGQauFt1fGKGn8VhuZRw1kxTtWbqs_pw3OHXfPOWueaklmFkgrOw1kqnEf949CSf1EByGYTW4FLsfxs6NYTH7CT6CdaJVFLECms1fzKWoEt65h91PLT2VhO61G_7yF-W5COspPE9Vqti69PtFiP4Ahls1_LvF8bXVx-CNEpvAZ1x1fgekKKCl3ZbgM_XFNJO_Vl9cZ6FbesjckvV5TIJkCFohB_RCMLPGWmvztb5-3_K7f7XM9CpGtErUIjANQ1fpVG1yIK2BUprDuKCga1eNLVQJa1PmZ5RSVN6rMx5usOTOyRvGnOJz1qrGhB5Csv2_mZH3N6R2EdC4R5h9e8rxHLihzU-QAJXz-Tyrvoqz0_XyH4Y6AkwUz8JxzU-QAJXzUK3kPHZQLzP.",
            "isg": "BDo6RSHvBpFxEoS8YITVSzGsi2Bc677FlXaxgEQzxE2YN9txLXtQ1bhJh8PrpzZd"
        }

        self.session.cookies.update(self.cookie)

    def parse_search_goods(self, data):
        """
        解析数据，获取商品信息
        :return:
        """
        title = jsonpath(data, '$..data..result..title')
        item_id = jsonpath(data, '$..data..result..nid')
        print(title)
        print(item_id)
        return title, item_id

    def search_goods(self):
        """
        搜索某商品
        :return:
        """
        tt = str(int(time.time() * 1000))
        url = "https://h5api.m.taobao.com/h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0/"

        params = {
            "pageNum": 2,
            "pageSize": 25,
            "itemLastCount": 48,
            "hasMore": True,
            "latestHundredItem": "815215290870,782432204935,868552430950,683919088914,891848265600,642455092973,821945383862,687724808723,793206077262,710800167776,742026061092,855723799635,782021190974,780935789714,917015888643,888708498340,824951880212,624644088852,523138769220,906769811187,677300255301,913986330620,833117315193,855777378803,911470987906,886339060989,810248929194,872196614606,539024191938,896468130353,893621993825,598005255813,730183363447,736309790459,915626126625,863280763842,919859688585,910926711806,566623330401,829132595816,726459905578,900855240477,602997773315,712594330858,757026400780,675547149426,908133475019,666560089810",
            "firstPagePVID": "b965b4f4-4f6e-4352-afaf-afb22c2bde57",
            "itemTotal": 300,
            "invalidItemId": "872580600491",
            "isFirstPage": False,
            "myCna": "4z6qIOKo/HUCAZ0ASGzroCO7"
        }

        data = {
            "appId": "47291",
            "params": json.dumps(params, separators=(',', ':'))
        }

        data = json.dumps(data, separators=(',', ':'))

        # p_data = json.loads(data)
        # p_data = json.dumps(p_data)
        # p_data['params'] = json.loads(p_data['params'])
        # print(p_data)

        # print(final_payload)
        params = {
            "jsv": "2.7.4",
            "appKey": "12574478",
            "t": "1747141938626",
            "sign": "4c768abb673b3bbbc16b2e633d35c03a",
            "api": "mtop.relationrecommend.wirelessrecommend.recommend",
            "v": "2.0",
            "timeout": "10000",
            "type": "json",
            "dataType": "json",
            "callback": "mtopjsonp34",
            "data": data,
            # "bx-ua": "231\\u0021ORA7K4mUnS4+jIIkd+7o3zBjUGg0uSOn+fYFmLQQwGng0wmHntUSK+2ttWIwYfiRlXeQ+thKJXIvfegh2cGUuRIvbZ9fhRfZbrcyCwJp1Tn/1O6FZphC2AulaWUlfRBJq3bU1v0W87TgQDikKIFEkKqn/me4vvko5JhcqYNvyHwJvLPgQpw+ykcg5YdC1GhpxzZduewMmenoSwQRur1zpjO94AlsT9Ba2gXj7xGlnJinhiBclz/r+hMep4Dqk+I9xGdF43e1LglCok+++4mWYi++6PXgobpS+UADjDmnuOXMEuy19T1fHkZoQzm+uvlQeeQh1WOYZHsCTI4XXUuI2dGaCpqpMIQXBT7soGygRlUFVHWlHGoQ1Z5+yJGc35JdbI82eiIiOEmc/+YsZ2FtCb0elWtDk351bKJ5outcsK5TqrFM3NC7a5g9hDkQKaAXK4yVjQEH8VKLKzOxCXsSg5CbBsMwgZu8N173158HwBSewpjidAlfDemwQmqmH1h5oHujqw+69XSlj8F0+c4BCK5zxHbTxS4juvoiy1SZOyGDvwLM+ahcLdmP9vS56IxL7rWz3YSNCo6NOw1GZEX+Ga6Z68Y3s0rLg3YESC2iOnkM+AwjSpGUXmTlFDqQN/yxZYqX07F4Kdspgd1D0hEEdwoB0RNB/vvoGa+kHpY38DShyWxoYQdmDVHMNNY8pZtM21A8Cy3AyZ3KUwXRvONYzvQQDVINpA/4Sp3Ida3jgpbEcPLaU1F+gGhoOM/o/eTLdnDkIdeANFJ53notBqvxpesDz+e0/V6e25DrmQV8Mpih2rrMttXZifQ+25/5UJv5pSAOYFc/ZtFTNJa3uYQ/GC93XFUyIUai7CvSEHnrbgXHhB2j21CwPp6PhfyjdSL8F5aLZfP5kDg5D1uW/8T39HnKXHaQgNVpDGREJHyBf8IrX5glAsNdAuZL2UWc54+PqOmZUoAYS1gqhC1Z3HFZQZlagG6yTNwDz5kZw8dKRZU7t9PVrl0W0qoYMZjn2K/XaPDfaUw4Q5fW3omGh2T93dwlzKi0c1hoTuya/bg+J58BMTDkLsTbGaHxIcAcHyg5sQVHtAG1EGrcetwbBVHUG2bzdFXTL6U/vXp6zC2HhkVmpPxfiJswVMQVuA4tni7aob1fm+OqPc+fIo4L/qk3m9+BbkFe4qxful1opaXp9FJiiYOPCO/iY4kw/F4OZaHNgD2WREo5lNZo+PEOjrcbXjKqru0KDXBZh9U3RaE+UZYgqZwUZa9bsGB8Ud9A6QoyKnCJICvysHsQzjMzfZuM6nYwhGfmnNi/gRvEGO0ZOe/COBLT5js/DBSAy6iCai3AkJvdnzjwzSz/5fEe+2U8u1lBln0cwW5DK7sazkzcHces2v3vrNwSt6kQUtBsbH24/mrR8M7+Hsk+d2PqxPr67XTTPoPveEZ8ZdbCcBmOV3HZcW/TLiM2uJsTXKbpOorV8k4bE+kb0ICNFMuh9emVWcP7gX1D/TkdmjNdS7bKjbiJuAzR0gEBcM2cvbZiG8/2Z3PZ6MKQPQcSSSUP47BaDFiJ0q7ybo09v4HEax8kIL2kwlYdlfMiFueeao+qqTtD6Kg76y+uII9HC0D4ozRPRT0NEuXXGJ+WUeoAOCYtCHb4ZGbZ1RHnhhNVoj3ntL+uvs3Wnz567j8bsF3qIwFVzu0MBNCN3ntu/CGEZwbdLS0SDbUzwEiAIqJZ3Sas1buIzM99AQ8KW2Y6STLAh7zwjuTQ8sbLGqrxpVeopeQpr6nKlaxSfpJC87eQ92j8N7EkjmSwhK2GPPfL1Ul7MZLqtqfYzsz9SekZDt7lgYOI9kNuPOgssHTMhIHnWcyxgDVdbEHt09u6EhQ8EtM6gGIyRIevrRLS",
            "bx-umidtoken": "T2gAFiZPRNsq7pnNBc4WOTUh1-Stl_LSTbVboK_gHOrDu8ohxav7LTpy2pZ0pxE0x_k=",
            # "bx_et": "gAyoQMGwG7l5Ss7xM-M5sLvwUW5vkYMINypKJv3FgquXeXudNyc3JrGUeYE8o2zT-De8pJVXKlZQegMdVYZSdv7OWOH3VuMCNyaQKJDqgciNpDuE8YMqansAHOBTVuiMIbScBJ3DhD0vTpzEajWqxqRE4QzEgKoIuLoeUD8VmqgqY3lyLIlqxc8yaykFmoujYvoz8XS00x6JLV2Uh-7XT6ySClpII0co7uuz2uyVFXA7Dqmr2-oo9AqyOpJUn0cz37MNKOl8TlG_e8WHhYEggxoTVTvmQuogyqUNQKD4DozK1S_BBja0KfwraHSqu840FYzRTd4iEycaUjxepurqPxm4QMdsk-0888cVXdcK3RhZUSCfyXHojyy7rHvU7oETFjwhSEuQwcMqXu6knArrYg-MgC-2RpiVv-RBObojmVhrK5J-T29u-ijD1_Grc0QOmiABObojmVIcmCTSamiRW"
        }

        sign = get_sign(self.cookie.get('_m_h5_tk').split('_')[0], tt, params['appKey'], data)

        params['t'] = tt
        params['sign'] = sign

        response = self.session.get(url, params=params)

        resp_data = response.json()
        # print(resp_data)

        # 解析数据
        titles, ids = self.parse_search_goods(resp_data)

        for title, id in zip(titles, ids):
            print(title, '-------', id)

        sid = input('请你选择要采集的商品号：')

        return sid

    def parse_detail_info(self, data):
        # print(data)
        base_url = 'https://img.alicdn.com/imgextra/'
        # 标题
        # 标题
        title = jsonpath(data, '$.data.item.title')
        title = title[0] if title else None

        # 主图
        main_img_path = jsonpath(data, '$.data.item.images[0]')
        main_img = base_url + main_img_path[0] if main_img_path else None

        # 销量
        buy_nums = jsonpath(data, '$.data.item.vagueSellCount')
        buy_nums = buy_nums[0] if buy_nums else None

        # 原价
        orign_price = jsonpath(data, '$.data.skuCore..price.priceMoney')
        orign_price = round(float(orign_price[0]) / 100, 2) if orign_price else None

        # 优惠价
        now_price = jsonpath(data, '$.data.skuCore..subPrice.priceMoney')
        now_price = round(float(now_price[0]) / 100, 2) if now_price else None

        # 优惠券信息
        res = []
        try:
            promotionTitle = jsonpath(data, '$.data..promotionTitle')
            if promotionTitle:
                res.append(promotionTitle[0])

            coupon_info = jsonpath(data, '$.data..itemApplyParams')
            if coupon_info:
                res.append(json.loads(coupon_info)[0])

        except:
            res = ["无优惠券信息"]

        # 打印结果
        print("标题:", title)
        print("主图URL:", main_img)
        print("月销量:", buy_nums)
        print("原价:", orign_price)
        print("优惠价:", now_price)
        print("优惠券信息:", "、".join(res))

    def get_base_info(self, sid):
        """
        获取商品基础信息
        :return:
        """
        tt = str(int(time.time() * 1000))

        exParams = {'abbucket': '7', 'detail_redpacket_pop': 'true', 'id': sid, 'ns': '1',
                    'query': '鞋子',
                    'spm': 'a21n57.1.hoverItem.3',
                    'xxc': 'taobaoSearch',
                    'domain': 'https://detail.tmall.com', 'path_name': '/item.htm', 'pcSource': 'pcTaobaoMain', }

        data = {'id': sid, 'detail_v': '3.3.2',
                'exParams': json.dumps(exParams, ensure_ascii=False, separators=(',', ':')).replace(' ', '')}

        data = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace(' ', '')

        url = "https://h5api.m.tmall.com/h5/mtop.taobao.pcdetail.data.get/1.0/"

        params = {
            "jsv": "2.7.5",
            "appKey": "12574478",
            "t": tt,
            "sign": "e33e377035affd53d8e5b227584341a2",
            "api": "mtop.taobao.pcdetail.data.get",
            "v": "1.0",
            "isSec": "0",
            "ecode": "0",
            "timeout": "10000",
            "ttid": "2022@taobao_litepc_9.17.0",
            "AntiFlood": "true",
            "AntiCreep": "true",
            "jsonpIncPrefix": "pcdetail",
            "type": "json",
            "dataType": "json",
            "callback": "mtopjsonppcdetail1",
            "data": data,
            "bx-umidtoken": "T2gAdZUPPZFFTUO-yrZPsugmC1aiUZJy5Q4e5-kPqJMxXSQQi7tiHIx6lraG8QWBZOM=",
            "x-pipu2": "h%7Bdugn%7F%7Bgkhffpk%7D)%24%252'k%24sf(7z%2C29nc'%3C7j61%3B%3A9%3C%2C6%3Dj%0D%3E%11%7B*%3B%266%3F'-%3A%3B%7Boqrw",
            "bx-ua": "fast-load"
        }

        sign = get_sign(self.cookie.get('_m_h5_tk').split('_')[0], tt, params['appKey'], data)

        params['sign'] = sign

        response = self.session.get(url, params=params)
        data = response.json()
        # 解析数据
        # print(response.json())
        self.parse_detail_info(data)

        # print(response)

    def main(self):
        """
        主方法
        :return:
        """
        # 搜索商品,返回商品的id
        sid = self.search_goods()
        # 获取商品基础信息
        self.get_base_info(sid)
