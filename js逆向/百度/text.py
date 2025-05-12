# 打开excle获取文章id
import pandas as pd
from openpyxl import workbook


def get_id():
    dic = {'金台资讯': 0, '四川观察': 0, 'www.jj831.com/2023/0418/3744.....': 0, '封面新闻': 0, '中国消费网': 0, '四川日报': 0, '国际在线': 0, '人民号': 0, '同花顺财经': 0, '四川经济网': 0, 'gba.china.com.cn/2023-04/17/co...': 0, '四川发布': 0, '手机凤凰网': 0, 'app.ybxww.com/ta...php...': 0, '云上宜宾': 0, '新浪财经': 0, '搜狐网': 0, '世纪新能源网': 0, '四川新闻网': 0, '腾讯网': 0, '新浪汽车': 0, '汽车之家': 0, '高工锂电': 0, '宜宾新闻网': 0, '金投网': 0, '四川在线': 0, '证券之星': 0, '宜宾市人民政府': 0, '网易新闻': 0, '搜狐新闻客户端': 0, '中国科技网': 0, 'epaper.scjjrb.com/Article/inde...': 0, '中国高新网': 0, '太平洋汽车': 0, 'tv.cctv.cn/2023/04/24/VIDEnLUd...': 0, '财经网': 0, '中国经济网': 0, 'www.ybtv.cc/fccommon/Home/det....': 0, '网易': 0, '澎湃新闻': 0, '新城网': 0, 'm.gffr.harvest.com.cn/news/588...': 0, '云酒头条': 0, 'xartyy.com/gonglue/1286...html': 0, '永尚旅游': 0, '新浪新闻': 0, '手机新浪汽车': 0, '人人文库': 0, '头条': 0, '新浪': 0, 'm.bjx.com.cn/mnews/20230508/13...': 0, '第一电动网': 0, '东方财富网': 0, 'www.inewsweek.cn/auto/2023-04-...': 0, 'app.ybvv.com/wap/thread/view-t...': 0, 'wd.zhengxingzhijia.com/k/20230...': 0, '懂车帝': 0, '电子信息产业网': 0, '凤凰网': 0, 'www.cheyun.com/content/48...': 0, '牛媒': 0, 'm.hangxunbao.com/z/255896...html': 0, '知乎': 0}

    print(dic)
    df = pd.read_excel('云上数据.xlsx', usecols=[1], names=None)
    df_li = df.values.tolist()
    for s_li in df_li:
        dic[str(s_li[0])] += 1
    print(dic)
    ws = workbook.Workbook()
    wb = ws.active
    for k,v in dic.items():
        wb.append([k,v])
        ws.save('云上数据2.xlsx')
get_id()