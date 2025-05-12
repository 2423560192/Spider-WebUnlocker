import requests
from lxml import etree
from openpyxl import workbook

url = 'https://sports.163.com/special/00051C9E/gjb.html'

h = headers = {
    'cache-control': 'max-age=0',
    'cookie': '__bid_n=186f480b32f90633264207; _ntes_nnid=6a6998c40b11e24fac050dadd18f4f3a,1685173925401; _ntes_nuid=6a6998c40b11e24fac050dadd18f4f3a; FPTOKEN=ptFnUncfqHuFVRk4JxKqbhrOctbycXAfSGNTJSqP2OIRj0cn/NF3JSQC0xt+GxqZFTnIVH6qyCBoUHRR9ui+Qmmczq24cok88Fa9EtaAmbY2H97hqwm8Q0i4nWZaAZel4Tlal6hq/HGijw8ZtZHTDTX14bIg/o6x1M8UGbNHX/T1OvEb/TkkJ6Spoz494e7ChAaku4ESw0pG9vtnNahE6V6AbL7XgdQ5vuj0RSNb9H5+psvBL06rLdyq38bqJKEZzxNQ+/kugrWFvpGWGmCB/ELjafkL6gjFonViaaVSe/5RpBAtXMtwM9gmQV1s0mr54zPHefA95yPuKh65QxC6flVo+7VnAOX6GSR0NxO2E7Gh3d6+e6jswp4jamxYA3oIEz5XUmJXxa3jsJzLL7GVFw==|unx10FYaGZb26QoMlEjZqKfJwQhNEkHcxM+Gt+mPOZA=|10|1bdfe28ebe9b3b713ec2475bb307e317; ne_analysis_trace_id=1688711845700; s_n_f_l_n3=8bd79af6746fb6f61688711845701; _antanalysis_s_id=1688711846391; vinfo_n_f_l_n3=8bd79af6746fb6f6.1.12.1679139299791.1685971677970.1688711904976',
    'referer': 'https://sports.163.com/special/00051C9E/gjb_19.html',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}
ws = workbook.Workbook()
wb = ws.active
wb.append(['新闻标题', '新闻链接', '新闻时间'])
ws.save('网易新闻网.xlsx')


def get_data(url):
    r = requests.get(url, headers=h)
    r.encoding = r.apparent_encoding
    if r.status_code == 200:
        data = r.text
        # print(data)
        lxml = etree.HTML(data)

        titles = lxml.xpath('//div[@class="new_list"]//div[@class="news_item"]//h3/a/text()')
        links = lxml.xpath('//div[@class="new_list"]//div[@class="news_item"]//h3/a/@href')
        times = lxml.xpath('//div[@class="new_list"]//div[@class="news_item"]//div[@class="post_date"]/text()')
        for t, l, tt in zip(titles, links, times):
            print(t)
            print(l)
            print(tt)
            print('======================')
            save_data(t, l, tt)

def save_data(t, l, tt):
    wb.append([t, l, tt])
    ws.save('网易新闻网.xlsx')

def main(url):
    get_data(url)
    for i in range(2, 21):
        s = i
        if i<10:
            s = '0'+str(i)
        print(f'这是第{s}页')

        url = 'https://sports.163.com/special/00051C9E/gjb_{}.html'.format(s)
        get_data(url)


if __name__ == '__main__':
    main(url)
