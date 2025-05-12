import execjs
import requests, re
from lxml import etree

session = requests.session()
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Referer": "https://sugh.szu.edu.cn/Html/News/Columns/540/Index.html",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "sec-ch-ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}


def spider_index01(url):
    response = session.get(url, verify=False)
    response.encoding = 'utf-8'
    html = etree.HTML(response.text)
    # print(html)
    meta_content = html.xpath('//meta[2]/@content')[0]
    auto_js = html.xpath('//script[2]/text()')[0]
    ts_url = 'https://sugh.szu.edu.cn' + html.xpath('//script[1]/@src')[0]
    ts_js = session.get(ts_url).text

    return meta_content, auto_js, ts_js


def update_cookie(meta_content, auto_js, ts_js):
    with open('main.js', 'r', encoding='utf-8') as js_file:
        js_code = js_file.read()
    js_code = js_code.replace('metaContent', meta_content).replace("'auto_js'", auto_js).replace("'ts_js'", ts_js)

    js_compile = execjs.compile(js_code)
    cookie_t = js_compile.call('get_cookie').split(';')[0].split('=')

    session.cookies.update({cookie_t[0]: cookie_t[1]})

    print(session.cookies.get_dict())


def spider_index02(url):
    response = session.get(url)
    response.encoding = "utf8"
    print(response.status_code)
    print(response.text)


def main():
    url = "https://sugh.szu.edu.cn/Html/News/Columns/7/3.html"
    meta_content, auto_js, ts_js = spider_index01(url)
    update_cookie(meta_content, auto_js, ts_js)
    spider_index02(url)


if __name__ == '__main__':
    main()
