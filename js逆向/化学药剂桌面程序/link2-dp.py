import time

from DrissionPage import ChromiumPage , ChromiumOptions

import pandas as pd


def get_urls(url):
    cp.get(url, retry=3, interval=2, timeout=15)
    all_urls = []
    f = open('urls.txt', 'w')
    p = 1
    for i in range(1 , 4):
        print('第',p , '页')
        p += 1
        urls = cp.eles('tag:a@class=product-item-link')

        for i in urls:
            url = i.link
            print(url)
            f.write(str(url) + '\n')

        # 点击下一页
        next = cp.ele('xpath://a[@class="action  next"]', timeout=3)
        print(next)
        if next:
            next.click()
        else:
            print('没有下一页了')
            break
        time.sleep(3)
    # 关闭浏览器
    # cp.quit()


if __name__ == '__main__':
    co = ChromiumOptions()
    co.auto_port()
    co.incognito(True)
    co.set_argument('--guest')
    # co.set_argument(
    #     '--no-sandbox')  # 禁用沙箱 禁用沙箱可以避免浏览器在加载页面时进行安全检查,从而提高加载速度 默认情况下，所有Chrome 用户都启用了隐私沙盒选项  https://zhuanlan.zhihu.com/p/475639754
    co.set_argument("--disable-gpu")  # 禁用GPU加速可以避免浏览器在加载页面时使用过多的计算资源，从而提高加载速度
    co.headless(False)
    # 创建浏览器对象
    cp = ChromiumPage(co)

    # 打开爬取内容
    df = pd.read_excel('乙醇金属盐汇总.xlsx')
    names = df['名称']

    for name in names:
        url = f'https://www.aladdin-e.com/zh_cn/catalogsearch/result/index/?p=1&product_list_limit=48&product_list_mode=grid&q={name}'
        get_urls(url)
