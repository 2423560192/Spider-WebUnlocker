import json
import re
import requests

cookies = {
    'BIDUPSID': '1F020769C39164920A1FDCF9AD0879B1',
    'PSTM': '1719288743',
    'BAIDUID': '1F020769C39164920A1FDCF9AD0879B1:FG=1',
    'H_WISE_SIDS_BFESS': '60276_60334_60372',
    'H_WISE_SIDS': '60276_60852_60886_60875_60897',
    'H_PS_PSSID': '60276_60852_60886_60875_60897_60976',
    'BDORZ': 'B490B5EBF6F3CD402E515D22BCDA1598',
    'BAIDUID_BFESS': '1F020769C39164920A1FDCF9AD0879B1:FG=1',
    'ab_sr': '1.0.1_MjAyNjIwMDYwZWU4Y2I0YmJiNzc1YmU2NTU4Yjk2N2RhMzFhZjkzZWMzNTFmYTc0NzU5ODQ4NjBjOWRlN2Y2M2Y4ZjhlZjg1ODI1ZDYyZjgwZjU1M2YzZTNlYzU0YmViMmIyM2IxZjMwNjM2NWNmYmQxYzI3YWFlOGZiOWQxNGM2Y2VkYmE5NzcxZjJmOTljMzQ3OWI2YWI5NGNjMTIxOA==',
    'RT': '"z=1&dm=baidu.com&si=edc21e10-cede-40d3-91b1-13a65e0ab4f4&ss=m2ply441&sl=4&tt=3yq&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=206g"',
}

headers = {
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Acs-Token': '1729847221442_1729913818438_Bfily7UzfkSKVxSL7JiuFLraQTuOqKSo9XKD1WDvZgQcXB4WLZhKR61eg0Aa6tPIybQWvA8yD5WFurHcJgH/4HeLpl1nCd0kTO3G+doM7vw05CRl3cZlf5woT/UnSLZfBTXene8WzF1R3Ss2J1+5GxynrbJm0FeyKZTv9niG4ZnEdDJnY3PhPcg2bDmJhojKY+vFXHovyqcSrTkKQXXIfh8/iKTf+f2okVfWu3pHWgbd151znv+7EAG5AnGtr7gvOCdAFIe9JDoi97DvnQsVuoYHO2cJGdHvBDBQchedkymXavUd77uEgqAtdfMpS0AnCGd6EO/3p32lWXuV85in+13rhhAHbt/o00K5lEGi3Od1FX4uAAMpGkC8b+r6mAmSX3583hB8Rc06XBnch73h74ZO3kwOg33mMsvUTN8tTU1YZD5xCmHzFU/PZZmdsmhEkjnBvu1qtMxu2hZisXn3Q3kbXiao82lBdrJ43/0YgZs=',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    # 'Cookie': 'BIDUPSID=1F020769C39164920A1FDCF9AD0879B1; PSTM=1719288743; BAIDUID=1F020769C39164920A1FDCF9AD0879B1:FG=1; H_WISE_SIDS_BFESS=60276_60334_60372; H_WISE_SIDS=60276_60852_60886_60875_60897; H_PS_PSSID=60276_60852_60886_60875_60897_60976; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BAIDUID_BFESS=1F020769C39164920A1FDCF9AD0879B1:FG=1; ab_sr=1.0.1_MjAyNjIwMDYwZWU4Y2I0YmJiNzc1YmU2NTU4Yjk2N2RhMzFhZjkzZWMzNTFmYTc0NzU5ODQ4NjBjOWRlN2Y2M2Y4ZjhlZjg1ODI1ZDYyZjgwZjU1M2YzZTNlYzU0YmViMmIyM2IxZjMwNjM2NWNmYmQxYzI3YWFlOGZiOWQxNGM2Y2VkYmE5NzcxZjJmOTljMzQ3OWI2YWI5NGNjMTIxOA==; RT="z=1&dm=baidu.com&si=edc21e10-cede-40d3-91b1-13a65e0ab4f4&ss=m2ply441&sl=4&tt=3yq&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=206g"',
    'Origin': 'https://fanyi.baidu.com',
    'Referer': 'https://fanyi.baidu.com/mtpe-individual/multimodal?query=apple%0A&lang=en2zh&ext_channel=Aldtype',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'accept': 'text/event-stream',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

json_data = {
    'query': '苹果',
    'from': 'en',
    'to': 'zh',
    'reference': '',
    'corpusIds': [],
    'needPhonetic': True,
    'domain': 'common',
    'milliTimestamp': 1729913818502,
}

response = requests.post('https://fanyi.baidu.com/ait/text/translate', cookies=cookies, headers=headers, json=json_data)

res = response.text.split('\n')

for line in res:
    # print(line)
    if '获取词典成功' in line:
        # print(line)
        print(re.search(r'"text":"(.*?)"', line).groups(1)[0])


