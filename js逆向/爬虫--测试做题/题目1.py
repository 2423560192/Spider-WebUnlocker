import requests
from bs4 import BeautifulSoup
from openpyxl import workbook

url = 'http://renshi.people.com.cn/'

h = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'wdcid=7d9b460585bc3233; wdses=1f3047718ca80654; wdlast=1688710271',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}
ws = workbook.Workbook()
wb = ws.active
wb.append(['新闻标题','新闻链接','新闻时间'])
ws.save('中国共产党新闻网.xlsx')

def get_data(url):
    r = requests.get(url, headers=h)
    r.encoding = r.apparent_encoding
    if r.status_code == 200:
        data = r.text
        print(data)
        soup = BeautifulSoup(data, 'lxml')
        titles = soup.select('div[class="fl"] ul li a')
        links = soup.select('div[class="fl"] ul li a')
        times = soup.select('div[class="fl"] ul li i')
        for t,l,tt in zip(titles,links,times):
            title = t.text
            print(title)
            link = 'http://renshi.people.com.cn/' + t['href']
            print(link)
            tt = tt.text.replace('[','').replace(']','')   # 时间
            print(tt)
            print('======================')
            save_data(title,link,tt)
def main(url):
    get_data(url)
    for i in range(1,8):
        print(f'这是第{i+1}页')
        url = 'http://renshi.people.com.cn/index{}.html'.format(i)
        get_data(url)


def save_data(t,l,tt):
    wb.append([t,l,tt])
    ws.save('中国共产党新闻网.xlsx')

if __name__ == '__main__':
    main(url)
