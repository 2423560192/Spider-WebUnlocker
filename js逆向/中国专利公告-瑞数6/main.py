import requests
import execjs
import re
import lxml

session = requests.Session()

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'http://epub.cnipa.gov.cn/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
}

response = session.get('http://epub.cnipa.gov.cn/', headers=headers, verify=False)

res = response.text


# 获取content
def get_content(res):
    content = re.findall('content="(.*?)"', res)[1]
    return content


content = get_content(res)


# 获取source
def get_source():
    import requests

    cookies = {
        'NOh8RTWx6K2dS': '60OevBhcDeP9knVpSelGwoBiZ0WTLIe7xj3QcauxaYQRVJ5TI81SoW0_Pz.uUE4M468Vb.sUlAUR53XuMls3tIVG',
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        # 'Cookie': 'NOh8RTWx6K2dS=60OevBhcDeP9knVpSelGwoBiZ0WTLIe7xj3QcauxaYQRVJ5TI81SoW0_Pz.uUE4M468Vb.sUlAUR53XuMls3tIVG',
        'Pragma': 'no-cache',
        'Referer': 'http://epub.cnipa.gov.cn/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    }

    response = requests.get(
        'http://epub.cnipa.gov.cn/z5gPWiiwO6ht/2h9AIDg9eZgY.b4c45da.js',
        cookies=cookies,
        headers=headers,
        verify=False,
    )
    return response.text


source = get_source()


# 获取ts
def get_ts(res):
    ts = re.findall("<script\stype=\"text/javascript\"\sr='m'>(.*?)</script>", res, re.DOTALL)[0]
    return ts


ts = get_ts(res)


# 生成cookie

def get_cookie(content, ts, source):
    r = open('res.js', encoding='utf-8').read().replace('myContent', content).replace('"ts.js"', ts).replace(
        '"source.js"', source)
    cookie = execjs.compile(r).call('get_cookie').split(';')[0].split('=')

    session.cookies.update({cookie[0]: cookie[1]})
    print(cookie)


get_cookie(content, ts, source)

# 发出请求

response = session.get('http://epub.cnipa.gov.cn/', headers=headers, verify=False, )
print(response.status_code)
print(response.text)
