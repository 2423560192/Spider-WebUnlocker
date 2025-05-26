from lxml import etree


def get_resp_data():
    import requests

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "sec-ch-ua": "\"Chromium\";v=\"136\", \"Google Chrome\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    }
    cookies = {
        "RK": "wBXAgeL+7Z",
        "ptcz": "d32de47cbb14984f7061648cd978a513ffe9489c31940393aba9e367d3a26e4f",
        "pac_uid": "0_TW95fim5cj3JB",
        "omgid": "0_TW95fim5cj3JB",
        "_qimei_uuid42": "1951900122f100c898afd5caee96148a5856032d21",
        "_qimei_fingerprint": "97252720a76ba3430321a6adbfa654e4",
        "_qimei_q36": "",
        "_qimei_h38": "8f9578ee98afd5caee96148a0200000bd19519",
        "ua_id": "omWiKOI02IRTVdD6AAAAAJYmTok1I5GvXht8mr0PszM=",
        "_clck": "1hirrgb|1|fw7|0",
        "wxuin": "48140577492014",
        "data_bizuin": "3950457871",
        "data_ticket": "rFipZCB8ueys1+V9FwMOrcUfZWaSvZAdI3ZJqSj2WF4MDyeAJVHEvzpfsCKHMoMD",
        "xid": "e585651ecd5aa8db833a906df20743c0",
        "mm_lang": "zh_CN",
        "rewardsn": "",
        "wxtokenkey": "777"
    }
    url = "https://mp.weixin.qq.com/s/L5KVENGPMcYsgQK9Jc6SUA"
    response = requests.get(url, headers=headers, cookies=cookies)

    data = response.text

    # 解析数据
    lxml = etree.HTML(data)

    # 标题
    title = lxml.xpath('//*[@id="activity-name"]')[0].text.strip()
    print(title)
    sections = lxml.xpath('//div[@id="js_content"]/section')[0]

    elements = sections.xpath('.//p | .//img[@class="rich_pages wxw-img"]')  # 使用管道符组合两个选择器

    # 遍历并打印元素信息
    for elem in elements:
        if elem.tag == 'p':
            if not elem.text:
                continue
            print(f"段落: {','.join(elem.xpath('.//text()')) if elem.xpath('.//text()') else '无文本'}")
        elif elem.tag == 'img':
            if not elem.get('src') and not elem.get('data-src') and not elem.get('data-original'):
                continue
            print(elem.get('src') or elem.get('data-src') or elem.get('data-original'))


def main():
    # 获取文章数据
    get_resp_data()


if __name__ == '__main__':
    main()
