# 导入所需模块
import json
import os
import re
import time
from datetime import datetime

import requests
from outlook_create_agreement.util.user_agent import message  # 获取用户代理
from outlook_create_agreement.api.long_email.long_email import long_email  # 邮箱长登录流程模块
from outlook_create_agreement.util import market_data  # 市场参数配置
from outlook_create_agreement.util.unicode.unicode import unescape_unicode_sequences  # Unicode 解码工具


# 注册主逻辑类
class send:
    def __init__(self, root, proxy_api, user, gj, token_api):
        self.no = 0
        self.gj = gj  # 国家
        self.session = requests.Session()
        self.regis_data = {'redirectUrl': '', 'slt': ''}  # 注册成功后得到的跳转信息
        self.root = root
        self.cookie_e = 0  # cookie 错误次数计数
        self.proxy_api = proxy_api  # 获取代理 IP 的接口
        self.proxy = {}
        self.user_agent = ''
        self.user = user  # 当前用户数据
        self.da_ma_num = 0  # 打码次数
        self.cs_num = 0  # 重试次数
        self.token_api = token_api  # 获取验证码 token 接口
        self.market = ''  # 当前市场设置

    # 主控制函数
    def control(self):
        self.prt(f'当前线程:{len(self.root.p_list)}')

        # 若密码为空则退出
        if self.user['password'] == '':
            print('获取的账号为空,10s后开始重新提取')
            time.sleep(10)
            if self in self.root.p_list:
                self.root.p_list.remove(self)
            return

        rps = False
        try:
            self.proxy = self.proxy_api.get_proxy()  # 获取代理 IP
            rps = self.start()  # 开始注册流程
        except Exception as e:
            print(type(e))
            rps = False

        # 处理各种注册状态
        self.prt(f'{self.user["username"]}rps:{rps}')
        if rps == 'zcsb':
            self.cs_num += 1
            rps = False
        if rps == 'cookie_e':
            rps = False

        # 更新信息
        self.root.info.set(f'{self.root.total}/{self.root.token_total}')

        if rps:
            # 注册成功处理
            self.prt(f'{self.user["username"]}注册成功!')
            self.root.total += 1
            self.root.info.set(f'{self.root.total}/{self.root.token_total}')
            self.root.cg += 1

            # 写入到 UI 界面
            self.no = self.root.tree.insert("", "end",
                                            values=[len(self.root.tree.get_children()), self.user['username'],
                                                    self.user['password'], '注册成功!', self.da_ma_num,
                                                    f'数据已保存'])
            self.root.tree.after(100, lambda: self.root.tree.yview_moveto(1.0))
            self.root.number2 += 1
            info = self.user['username'] + "----" + self.user['password']

            # 若配置了提交 URL，提交账号信息
            if self.root.tj_url.get() not in ('不填默认关闭', ''):
                url = self.root.tj_url.get().replace("*", info)

                def send():
                    try:
                        r = requests.get(url).text
                        self.prt(f'已向{url}提交账号数据!')
                        self.change_cell_value(self.root.tree, self.no, 5, '已向服务器提交数据!')
                    except Exception as e:
                        self.prt(type(e))
                        self.prt(f'{url}提交失败,重新尝试ing')
                        send()

                send()

            # 保存账号到本地文件
            with open(f'{self.root.url.get()}/account.txt', 'a', encoding='utf-8') as f:
                f.write(info + "\n")

            # 若是登录模式，启动长邮箱处理逻辑
            try:
                if '登录' in self.root.model_.get():
                    long = long_email(self.proxy_api, self.proxy, self.user, self.user_agent,
                                      self.regis_data, self.session, self.root, self.no)
                    long.start()
            except Exception as e:
                pass
        else:
            # 注册失败处理逻辑
            self.cookie_e += 1
            if self.cs_num < 3 and self.cookie_e < 12:
                self.prt(f'{self.user["username"]}重新尝试!')
                time.sleep(8)
                self.control()
            else:
                self.root.number2 += 1
                if self.da_ma_num != 0:
                    self.root.tree.insert("", "end",
                                          values=[len(self.root.tree.get_children()), self.user['username'],
                                                  self.user['password'], '失败!', self.da_ma_num, '可能风控'])
                    with open(f'{self.root.url.get()}/fk.txt', 'a', encoding='utf-8') as f:
                        f.write(f"{self.user['username']}----{self.user['password']}" + "\n")
                self.root.yjcz_num += 1
        if self in self.root.p_list:
            self.root.p_list.remove(self)

    # 启动注册主流程
    def start(self):
        self.session = requests.session()
        os.environ["NO_PROXY"] = "https://signup.live.com"

        self.prt(f'{self.user["username"]}开始注册!')

        # 提取邮箱后缀
        suffix = '@' + self.user['username'].split('@')[-1]
        self.user_agent = message.get_user_agent()
        user_agent = self.user_agent

        # 获取注册参数
        argument = self.get_argument(suffix, user_agent)
        if not argument:
            self.prt(f'{self.user["username"]}参数获取失败!')
            return False
        self.prt(f'{self.user["username"]}参数获取成功!')

        # 获取注册 cookie
        cookie = self.get_cookie(argument['cookie.txt'], argument['dfpUrl'], user_agent)
        if not cookie:
            self.prt(f'{self.user["username"]}无法取得cookie!')
            return False
        self.prt(f'{self.user["username"]}取得cookie!')

        # 检查账号是否已被注册
        is_reg = self.cheek_have(user_agent, argument, self.user, cookie)
        if is_reg:
            self.prt(f'{self.user["username"]}该账号已存在!')
            return True
        self.prt(f'{self.user["username"]}可以进行注册!')

        # 数据验证
        rps = self.cheek_data(self.user, user_agent, argument, self.gj, cookie)
        if not rps:
            self.prt(f'{self.user["username"]}参数验证失败!')
            return False
        self.prt(f'{self.user["username"]}参数验证完成!')

        # 获取token打码验证
        self.prt(f'{self.user["username"]}开始打码(1-10s)!')
        token = self.token_api.get_token(rps['arkoseBlob'], user_agent)
        if not token:
            self.prt(f'{self.user["username"]}获取token失败! token:{token}')
            return False

        self.da_ma_num += 1
        self.root.token_total += 1
        self.prt(f'{self.user["username"]}获取token成功,token:{token}')

        # 提交注册
        regs = self.regis(self.user, self.gj, rps, argument, token, user_agent, cookie)
        if regs:
            return True
        else:
            # 检查是否因网络超时但注册成功
            time.sleep(8)
            is_reg = self.cheek_have(user_agent, argument, self.user, cookie)
            if is_reg:
                return True
            else:
                self.prt(f'{self.user["username"]}返回‘zcsb’')
                return 'zcsb'

    # 获取注册页面参数（包括cookie和dfpUrl）
    def get_argument(self, suffix, user_agent):
        try:
            url = f"https://signup.live.com/signup?mkt={self.gj}&lic=1"
            headers = {
                'User-Agent': user_agent,
                'Accept': 'text/html',
            }
            proxies = {"http": self.proxy["http"], "https": self.proxy["https"]}

            res = self.session.get(url, headers=headers, proxies=proxies, timeout=15)
            if res.status_code != 200:
                return None

            html = res.text
            dfp_url_match = re.search(r'dfpUrl":"(.*?)"', html)
            dfp_url = dfp_url_match.group(1).replace("\\u002f", "/") if dfp_url_match else ""

            return {
                "cookie.txt": res.cookies.get_dict(),  # 保存cookie
                "dfpUrl": dfp_url  # 获取dfp参数地址
            }
        except Exception as e:
            self.prt(f'获取argument失败: {e}')
            return None

    # 获取注册所需的 cookie（如 f= 参数等）
    def get_cookie(self, cookie_txt, dfp_url, user_agent):
        try:
            headers = {
                'User-Agent': user_agent,
                'Accept': 'application/json',
            }
            proxies = {"http": self.proxy["http"], "https": self.proxy["https"]}

            url = f"https://signup.live.com/{dfp_url}"
            res = self.session.get(url, headers=headers, cookies=cookie_txt, proxies=proxies, timeout=15)

            if res.status_code != 200:
                return None

            return res.cookies.get_dict()
        except Exception as e:
            self.prt(f'获取cookie失败: {e}')
            return None

    # 检查账号是否已被注册
    def cheek_have(self, user_agent, argument, user, cookie):
        try:
            proxies = {"http": self.proxy["http"], "https": self.proxy["https"]}
            url = "https://signup.live.com/API/CheckAvailableSigninNames"

            data = {
                "signInName": user["username"]
            }

            headers = {
                "User-Agent": user_agent,
                "Accept": "application/json",
                "Content-Type": "application/json"
            }

            res = self.session.post(url, json=data, cookies=cookie, headers=headers, proxies=proxies, timeout=15)
            if res.status_code == 200:
                result = res.json()
                return not result.get("isAvailable", False)
            else:
                return False
        except Exception as e:
            self.prt(f'检测是否注册失败: {e}')
            return False

    # 检查注册参数（是否可以继续注册）
    def cheek_data(self, user, user_agent, argument, gj, cookie):
        try:
            proxies = {"http": self.proxy["http"], "https": self.proxy["https"]}
            url = "https://signup.live.com/API/CreateAccountData"

            headers = {
                "User-Agent": user_agent,
                "Accept": "application/json",
                "Content-Type": "application/json"
            }

            payload = {
                "signInName": user["username"],
                "password": user["password"],
                "firstName": "Test",
                "lastName": "Account",
                "country": gj,
                "birthMonth": 1,
                "birthDay": 1,
                "birthYear": 1990
            }

            res = self.session.post(url, json=payload, cookies=cookie, headers=headers, proxies=proxies, timeout=15)
            if res.status_code == 200:
                return res.json()
            else:
                return None
        except Exception as e:
            self.prt(f'参数验证失败: {e}')
            return None

    # 提交注册请求
    def regis(self, user, gj, rps, argument, token, user_agent, cookie):
        try:
            proxies = {"http": self.proxy["http"], "https": self.proxy["https"]}
            url = "https://signup.live.com/API/CreateAccount"

            headers = {
                "User-Agent": user_agent,
                "Accept": "application/json",
                "Content-Type": "application/json"
            }

            payload = {
                "signInName": user["username"],
                "password": user["password"],
                "firstName": "Test",
                "lastName": "Account",
                "country": gj,
                "birthMonth": 1,
                "birthDay": 1,
                "birthYear": 1990,
                "proofConfirmationToken": token
            }

            res = self.session.post(url, json=payload, cookies=cookie, headers=headers, proxies=proxies, timeout=15)

            if res.status_code == 200 and "redirectUrl" in res.text:
                try:
                    js = res.json()
                    self.regis_data['redirectUrl'] = js.get('redirectUrl', '')
                    self.regis_data['slt'] = js.get('slt', '')
                except Exception:
                    pass
                return True
            else:
                return False
        except Exception as e:
            self.prt(f'注册提交失败: {e}')
            return False

    # 改变表格中某一行某一列的值
    def change_cell_value(self, tree, row, column, new_value):
        item = tree.item(row)
        values = list(item["values"])
        values[column] = new_value
        tree.item(row, values=values)

    # 控制台打印（带时间戳）
    def prt(self, text):
        print(f'[{datetime.now().strftime("%H:%M:%S")}] {text}')
