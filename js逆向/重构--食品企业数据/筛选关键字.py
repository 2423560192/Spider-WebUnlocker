import ast
import random
import time
import requests
from jsonpath import jsonpath
from openpyxl import workbook
import pandas as pd
import aiohttp
import asyncio
import json
import aiofiles

pc_USE_AGENT = [
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3451.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:57.0) Gecko/20100101 Firefox/57.0',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2999.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.70 Safari/537.36',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.4; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.1.4322; MS-RTC LM 8; InfoPath.2; Tablet PC 2.0)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36 OPR/55.0.2994.61',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.814.0 Safari/535.1',
    'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/418.9.1 (KHTML, like Gecko) Safari/419.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0; Touch; MASMJS)',
    'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1041.0 Safari/535.21',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3451.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:57.0) Gecko/20100101 Firefox/57.0',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2999.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.70 Safari/537.36',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.4; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.1.4322; MS-RTC LM 8; InfoPath.2; Tablet PC 2.0)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36 OPR/55.0.2994.61',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.814.0 Safari/535.1',
    'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/418.9.1 (KHTML, like Gecko) Safari/419.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0; Touch; MASMJS)',
    'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1041.0 Safari/535.21',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4093.3 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko; compatible; Swurl) Chrome/77.0.3865.120 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4086.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:75.0) Gecko/20100101 Firefox/75.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/91.0.146 Chrome/85.0.4183.146 Safari/537.36',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 VivoBrowser/8.4.72.0 Chrome/62.0.3202.84',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:83.0) Gecko/20100101 Firefox/83.0',
    'Mozilla/5.0 (X11; CrOS x86_64 13505.63.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:68.0) Gecko/20100101 Firefox/68.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 OPR/72.0.3815.400',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
]

h = {
    'content-type': 'application/json',
    'origin': 'https://www.dingtalk.com',
    'referer': 'https://www.dingtalk.com/',
    'user-agent': random.choice(pc_USE_AGENT)
}

# 添加计数
sign = 1


async def get_data(p,key,cat):
    url = 'https://holmes.taobao.com/web/corp/customer/searchWithSummary'
    payload = {
        "pageNo": p,
        "pageSize": 10,
        "keyword": key,
        "orderByType": 5,
        "bizCategory": {
            "bigCategory": cat,
            "smallCategory": None
        }
    }
    try:
        if sign % 100 == 0:
            # 延时
            time.sleep(10)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=json.dumps(payload), headers=h) as resp:
                json_data = await resp.json()
                values = jsonpath(json_data, '$..data.data[0:10]..ocid')
                if values:
                    print("页数已完成任务", payload['pageNo'], "数据:", values)
                    async with aiofiles.open('企业id.csv', 'a', encoding='utf-8') as f:
                        await f.write("\n".join(values))
                        await f.write("\n")
                else:
                    print('数据为空')
                await asyncio.sleep(1)

    except Exception as e:
        print("页数出错啦", payload['pageNo'], e)
        time.sleep(20)


async def main():
    keywords = ['滨州大有', '扬子石化', '旭化成', '扬州石化', '山东凯日', '浙铁大风', '日照三星', '沙特先进石化',
                '浙江永和', '平顶山神马', '潍坊振兴日升', '越南平山石化', '淄博齐翔腾达', '潍坊富维', '乐金LG',
                '仁泰化学', '华峰集团', '沧州大化', '寿光健元春', '中石化中原石化', '中天合创', '神华包头竞拍',
                '宁波台塑', '新疆中泰', '内蒙君正', '天津联化', '江苏瑞美福', '日照中博', '思创石化', '湛江东兴',
                '山东恒通', '东营海容', '中油华南', '浙江卫星', '苏州华苏', '内蒙古', '南通星辰', '宜宾天原',
                '石家庄炼厂', '东华能源（张家港）', '福建时代', '广东泰宝', '安徽华塑', '华东地区', '兰州石化',
                '台湾台塑', '洛阳石化', '新疆天利', '山东信发', '辽宁市场', '合肥金菱里克', '辽阳石化', '韩华宁波',
                '中石油锦西石化', '山东鲁清', '天津联华', '镇江奇美', '赛宝龙', '山东安达', '克拉玛依石化', '茂名石化',
                '联泓集团', '亚通石化', '江苏市场', '福建天原', '陶氏化学', '台湾宝理', '浙江兴兴', '惠州仁信',
                '山东海江', '伊朗阿拉克石化', '临沂阿里山', '卡塔尔石化', '山东诺宏', '宜昌山水', '山东富宇',
                '河南安化', '海科瑞林', '韩国工程', '鄂尔多斯电力冶金集团', '盘锦浩业', '延长集团', '天津龙王',
                '浙江华健', '青岛海湾化学', '印度海地亚', '神华榆林竞拍', '神华新疆竞拍', '日本旭化成', '江苏康宁',
                '内蒙亿利', '泰国暹罗化工', '南通宝泰菱', '惠州石化', '河北海伟', '菏泽恒大', '陶氏', '浙江鸿基',
                '沈阳东海', '台化出光', '神驰化工', '呼和浩特石化', '天津石化', '湖北百科', '天津长芦海晶', '东莞创丰',
                '锦西化工', '宁波富德', '大庆炼化', '三井', '山东齐成', '宁波台化', '阿曼石化', '江苏嘉昌', '宁夏宝丰',
                '辽通化工', '阳煤太化', '康辉石化', '垦利石化', '宁波LG甬兴', '福建联合', '开封龙宇', '三菱化学',
                '山东三义', '青海宜化', '金诚石化', '印尼钱德拉阿斯里', '福建天源', '内蒙三联', '中煤榆林', '鲁泰化学',
                '中石化华北', '泰国石化', '韩国可隆', '德国拜耳', '马来西亚宝理', '宝来石化', '山西榆社', '锦西石化',
                '常州华润聚酯', '太原市场', '石家庄三虎', '泰国TPI', '宁夏煤业', '沙特阿美', '济宁中联', '东明石化',
                '河南联创', '神华榆林', '石家庄炼化', '甘肃银光', '韩华沙特', '泰国三菱', '五粮液', '云天化集团',
                '青海盐湖', '长岭石化', '万华化学', '盘锦瑞斯特', '大连石化', '越南聚苯乙烯', '天津渤化', '咸阳助剂厂',
                '湖北金澳', '科威特', '湖北宜化', '山东广庆', '浙江伊美', '恒瑞新科', '福建福融辉', '江苏宝生',
                '济南炼厂', '安徽丰原', '四川金路', '山东齐旺达', '中石化三井', '印度', '苏州双象', '山西霍家沟',
                '印尼乐天', '包头海平面', '天津化工', '中煤蒙大', '山东联盟', '武汉友发', '齐鲁石化', '海南逸盛',
                '大庆华科', '山东东海', '山东信恩', '东华能源（宁波）', '广东新会美达', '天津大沽', '巴斯夫中国',
                '延安能化', '天津', '泰石油', '新疆天业', '神马集团', '云南云天化', '中石化华中', '久泰能源',
                '内蒙伊利', '浙江方圆', '河南开祥', '上海氯碱', '伊东东兴', '大连瑞光', '伊朗石化', '临沂奥星化工',
                '久泰集团', '滨州正海', '东营石化', '科思创（上海拜耳）', '锦州石化', '联泓新材料', '上海高桥',
                '美国杜邦', '中游华北', '阳煤昔阳', '韩国LG', '燕山石化', '北海炼厂', '宁波乐金', '青岛大炼油',
                '菏泽玉皇', '杭州聚合顺', '新三明', '山东东岳', '湛江新中美', '北海炼化', '哈尔滨石化', '兖矿鲁南',
                '青岛安邦', '扬子巴斯夫', '中蓝国塑', '珠三角市场', '汕头冠华', '福建湄洲湾', '北京有机', '台聚',
                '恒天中纤', '泰国', '武汉斯德隆', '科威特石化', '神华新疆', 'LG化学']
    category = ['制造业', '批发业', '批发和零售业']
    for k in keywords:
        for cat in category:
            tasks = []
            try:
                for i in range(1, 2):
                    tasks.append(asyncio.create_task(get_data(i,k,cat)))
                    print("页数加入任务", i,"关键字:",k)
                await asyncio.wait(tasks)
            except Exception as e:
                print("发生错误", e)
            break
        break


if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
