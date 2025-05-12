"""
该窗体界面拓展性高
具体更改流程如下：

1.将用户名可替换为爬虫检索用户输入的关键词输入

2.密码可替换为账号登录的cookie输入

3.Text富文本框该位置课选择输出爬虫效果print内容

4.对比事件绑定方法借鉴，即可创建程序执行关联函数
"""
import random
import tkinter as tk
import tkinter.messagebox as msgbox
from idlelib import window
from threading import Thread
from requests_html import HTMLSession
from PIL import Image, ImageTk
session = HTMLSession()
import os, cv2
from tkinter.filedialog import askopenfilename
from telnetlib import EC

from time import sleep
from selenium import webdriver  # # 驱动浏览器
from selenium.webdriver.common.by import By  # 选择器
from selenium.webdriver.common.keys import Keys  # 按键
from selenium.webdriver.support.wait import WebDriverWait  # 等待页面加载完毕，寻找某些元素
from selenium.webdriver.support import expected_conditions as EC  ##等待指定标签加载完毕
# def get_image(file_name, width, height):
#     im = Image.open(file_name).resize((width, height))
#     return ImageTk.PhotoImage(im)


class TKSpider(object):


    def __init__(self):
        self.option = webdriver.ChromeOptions()
        # option.add_argument('headless')
        self.option.add_experimental_option('detach', True)
        self.driver = webdriver.Chrome(options=self.option)
        """定义可视化窗口，并设置窗口和主题大小布局"""
        self.window = tk.Tk()
        self.window.title('自动化发送邮件')
        self.window.geometry('1000x1000')

        # """给GUI添加背景图"""
        # self.canvas = tk.Canvas(self.window, width=800, height=600)
        # self.im_root = get_image('hkdg.jpg', 800, 600)
        # self.canvas.create_image(400, 300, image=self.im_root)
        # self.canvas.pack()
        # 具体数据
        self.keys = ''
        self.title = ''
        self.content = ''
        self.accepter = ''

        """上传keys"""
        self.label_user = tk.Label(self.window, text='上传邮箱key码', font=('Arial', 12), width=30, height=2)
        self.label_user.pack()
        self.upload_button_key = tk.Button(self.window, text="点击上传", command=self.upload_file)
        self.upload_button_key.pack()

        """创建主题"""
        self.label_authme = tk.Label(self.window, text='输入主题', font=('Arial', 12), width=30, height=2)
        self.label_authme.pack()
        """创建label_user关联输入"""
        self.entry_authme = tk.Entry(self.window, show=None, font=('Arial', 14))
        self.entry_authme.pack(after=self.label_authme)

        """邮箱内容"""
        self.label_content = tk.Label(self.window, text='邮件内容', font=('Arial', 12), width=30, height=2)
        self.label_content.pack()
        """创建label_user关联输入"""
        upload_button = tk.Button(self.window, text="点击上传", command=self.upload_mails)
        upload_button.pack()

        # 创建上传按钮
        self.label_user = tk.Label(self.window, text='上传收件人', font=('Arial', 12), width=30, height=2)
        self.label_user.pack()
        upload_button = tk.Button(self.window, text="点击上传", command=self.upload_users)
        upload_button.pack()

        """创建Text富文本框，用于按钮操作结果的展示"""
        # 定义富文本框滑动条
        scroll = tk.Scrollbar()
        # 放到窗口的右侧, 填充Y竖直方向
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.text1 = tk.Text(self.window, font=('Arial', 12), width=85, height=12)
        self.text1.pack()
        # 两个控件关联
        scroll.config(command=self.text1.yview)
        self.text1.config(yscrollcommand=scroll.set)





        """定义按钮1，绑定触发事件方法"""
        """即点击运行，采集按钮，当点击时将执行parse_hit_click_1方法。在真实使用场景中"""
        """parse_hit_click_1中可替换为自己写的真正登录函数。这里仅为示例"""
        self.button_1 = tk.Button(self.window, text='运行，发送', font=('Arial', 12), width=10, height=1, command=self.parse_hit_click_1)
        self.button_1.pack(before=self.text1)

        """定义按钮2，绑定触发事件方法"""
        self.button_2 = tk.Button(self.window, text='清除', font=('Arial', 12), width=10, height=1, command=self.parse_hit_click_2)
        self.button_2.pack(anchor="e")

        """定义按钮3，绑定触发事件方法"""
        self.button_2 = tk.Button(self.window, text='暂停/继续', font=('Arial', 12), width=10, height=1,
                                  command=self.parse_hit_click_3)
        self.button_2.pack(anchor="e")
        # 判断循环计数
        self.num_if = 0
        # 全局判断条件
        self.is_running = True
        # 继续执行
        self.is_data = ''

    """收件人"""
    def upload_users(self):
        file_path = askopenfilename()  # 打开文件选择对话框，返回选择的文件路径
        print("Selected file:", file_path)  # 输出选择的文件路径
        with open(file_path, "r", encoding="utf-8") as f:
            self.accepter = f.readlines()
            print(self.accepter)

    """邮箱"""
    def upload_mails(self):
        # self.window.withdraw()  # 隐藏Tkinter根窗口
        file_path = askopenfilename()  # 打开文件选择对话框，返回选择的文件路径
        print("Selected file:", file_path)  # 输出选择的文件路径
        with open(file_path, "r", encoding="utf-8") as f:
            self.content = f.read()
            print(self.content)


    """keys"""
    def upload_file(self):
        # self.window.withdraw()  # 隐藏Tkinter根窗口
        file_path = askopenfilename()  # 打开文件选择对话框，返回选择的文件路径
        print("Selected file:", file_path)  # 输出选择的文件路径
        with open(file_path, "r",encoding="utf-8") as f:
            self.keys = f.readlines()
            print(self.keys)


    def parse_hit_click_1(self):
        """使用线程执行爬虫任务，线程关联"""
        Thread(target=self.parse_spider_run).start()

    def parse_hit_click_3(self):
        Thread(target=self.parse_if_data).start()

    def parse_if_data(self):
        """程序暂停逻辑"""
        self.num_if += 1
        if self.num_if % 2 == 0:
            self.is_running = True
            self.is_data = "pause"
        else:
            self.is_running = False
            self.is_data = ''

    def parse_spider_run(self):
        """
        定义触发事件1, 将执行结果显示在文本框中
        :return: 也可作为爬虫任务函数，添加爬虫逻辑
        """
        self.title = self.entry_authme.get()
        print(self.title)
        """爬虫任务函数"""
        for i in range(0,len(self.accepter)):
            print('开始发送')
            sleep(1)
            if self.is_running:
                # 报错提示
                # msgbox.showerror(title='错误', message='无效，请重新输入！')
                """调用爬虫任务函数"""
                self.parse_start_url(i)
            else:
                text = "----------暂停中----------\n"
                # 界面：富文本框-信息显示
                self.text1.insert("insert", f'第{i+1}次' + text+'发送暂停\n')
                # gui界面滑动条自动下拉
                self.text1.see('insert')
                while True:
                    if len(self.is_data) > 0:
                        break
                    sleep(1.5)
                """调用爬虫任务函数"""
                self.parse_start_url(i)

    def parse_start_url(self, i):
        """
        邮箱发送任务函数，发送请求
        """
        print('启动selenium')
        self.driver.get('https://mail.qq.com/')

        sleep(5)

        # 定位账号、密码，并输入

        self.driver.find_element(By.XPATH, '//*[@id="navBarTd"]/li[3]/a"]').click()


        # 切换到mainFrame

        self.driver.switch_to.frame('mainFrame')
        self.driver.find_element(By.XPATH, '//*[@id="list"]/ul/div/li[1]/label/input').click()
        self.driver.find_element(By.XPATH, '//*[@id="bar"]/div/div[1]/a[1]').click()
        self.driver.find_element(By.XPATH, '//*[@id="normalComposeDlg_QMDialog_jumpToNewWin"]/a').click()

        sleep(1)

        # 定位主题，并输入

        self.driver.find_element(By.XPATH, '//*[@id="subject"]').send_keys(self.title)


        # 点击格式
        self.driver.find_element(By.XPATH,'//*[@id="editor_toolbar_btn_container"]/font').click()
        self.driver.find_element(By.XPATH,'//*[@id="qmEditorToolBarDiv"]/div[1]/div[15]/div/input').click()


        # 定位邮件正文，先进入到iframe

        # self.driver.switch_to.frame(self.driver.find_element(By.XPATH, '//*[@class="qmEditorIfrmEditArea"]'))

        # 必须先点击正文，再send_keys


        # self.driver.find_element(By.XPATH, '/html/body').click()
        #
        # self.driver.find_element(By.XPATH, '//html//body').send_keys(self.content)

        self.driver.find_element(By.XPATH, '//*[@id="QMEditorArea"]/table/tbody/tr[2]/td/textarea[1]').click()
        self.driver.find_element(By.XPATH, '//*[@id="QMEditorArea"]/table/tbody/tr[2]/td/textarea[1]').send_keys(self.content)


        # 返回到mainframe

        # self.driver.switch_to.parent_frame()
        # self.driver.switch_to.frame('mainFrame')


        # 定位发送按钮
        try:
            self.driver.find_element(By.XPATH, '//*[@name="sendbtn"]').click()
            text = f"key{random.randint(1, len(self.keys) + 1)}: 邮箱: {self.accepter[i]}发送成功\n"
            # 界面：富文本框-信息显示
            self.text1.insert("insert", f'第{i + 1}次' + text)
            # gui界面滑动条自动下拉
            self.text1.see('insert')
            sleep(3)
        except:
            self.text1.insert("insert", f'第keys{i},邮箱: {self.accepter[i]}发送失败\n')
            # gui界面滑动条自动下拉
            self.text1.see('insert')


    def parse_hit_click_2(self):
        """定义触发事件2，删除文本框中内容"""
        self.entry_authme.delete(0, "end")
        self.text1.delete("1.0", "end")

    def center(self):
        """创建窗口居中函数方法"""
        ws = self.window.winfo_screenwidth()
        hs = self.window.winfo_screenheight()
        x = int((ws / 2) - (800 / 2))
        y = int((hs / 2) - (600 / 2))
        self.window.geometry('{}x{}+{}+{}'.format(800, 600, x, y))

    def run_loop(self):
        """禁止修改窗体大小规格"""
        self.window.resizable(False, False)
        """窗口居中"""
        self.center()
        """窗口维持--持久化"""
        self.window.mainloop()


if __name__ == '__main__':
    t = TKSpider()
    t.run_loop()












