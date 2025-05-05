# 向outlook的接口发送数据注册账号
import json
import os
import re
import time
from datetime import datetime

import requests

from outlook_create_agreement.util.user_agent import message
from outlook_create_agreement.api.long_email.long_email import long_email
from outlook_create_agreement.util import market_data
from outlook_create_agreement.util.unicode.unicode import unescape_unicode_sequences


class send:
    def __init__(self, root, proxy_api, user, gj, token_api):
        self.no = 0
        self.gj = gj
        self.session = requests.Session()
        self.regis_data = {
            'redirectUrl': '',
            'slt': ''
        }
        self.root = root
        self.cookie_e = 0
        self.proxy_api = proxy_api
        self.proxy = {}
        self.user_agent = ''
        self.user = user
        self.da_ma_num = 0
        self.cs_num = 0
        self.token_api = token_api
        self.market = ''
        pass

    # 控制中央
    def control(self):
        self.prt(f'当前线程:{len(self.root.p_list)}')
        if self.user['password'] == '':
            print('获取的账号为空,10s后开始重新提取')
            time.sleep(10)
            if self in self.root.p_list:
                self.root.p_list.remove(self)
            return
        rps = False
        try:
            self.proxy = self.proxy_api.get_proxy()  # 获取一个代理
            rps = self.start()
        except Exception as e:
            Exception_type = type(e)
            print(Exception_type)
            rps = False
        self.prt(f'{self.user["username"]}rps:{rps}')
        if rps == 'zcsb':
            # 判断最大尝试次数
            self.cs_num += 1
            rps = False
        if rps == 'cookie_e':
            # self.cookie_e += 1
            rps = False
        self.root.info.set(f'{self.root.total}/{self.root.token_total}')
        if rps:
            self.prt(f'{self.user["username"]}注册成功!')
            self.root.total += 1  # 总注册成功账号
            self.root.info.set(f'{self.root.total}/{self.root.token_total}')
            # 注册成功
            self.root.cg += 1
            self.no = self.root.tree.insert("", "end",
                                            values=[len(self.root.tree.get_children()), self.user['username'],
                                                    self.user['password'], '注册成功!', self.da_ma_num,
                                                    f'数据已保存'])
            self.root.tree.after(100, lambda: self.root.tree.yview_moveto(1.0))
            self.root.number2 += 1
            info = self.user['username'] + "----" + self.user['password']
            if self.root.tj_url.get() != '不填默认关闭' and self.root.tj_url.get() != '':
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
            with open(f'{self.root.url.get()}/account.txt', 'a', encoding='utf-8') as f:
                f.write(info + "\n")
            # 开启令牌流程
            try:
                if '登录' in self.root.model_.get():
                    long = long_email(self.proxy_api, self.proxy, self.user, self.user_agent,
                                      self.regis_data, self.session, self.root, self.no)
                    long.start()
            except Exception as e:
                pass
        else:
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
                                                  self.user['password'],
                                                  '失败!', self.da_ma_num,
                                                  f'可能风控'])
                    with open(f'{self.root.url.get()}/fk.txt', 'a', encoding='utf-8') as f:
                        f.write(f"{self.user['username']}----{self.user['password']}" + "\n")
                self.root.yjcz_num += 1
        if self in self.root.p_list:
            self.root.p_list.remove(self)

    # 开始执行流程
    def start(self):
        self.session = requests.session()
        os.environ[
            "NO_PROXY"] = "https://signup.live.com/API/CheckAvailableSigninNames?lic=1 fpt.live.com https://signup.live.com/API/CreateAccount?lic=1 https://signup.live.com/API/CreateAccount?lic=1"
        self.prt(f'{self.user["username"]}开始注册!')
        # 获取必须的参数
        suffix = '@' + self.user['username'].split('@')[-1]
        self.user_agent = message.get_user_agent()
        user_agent = self.user_agent
        argument = self.get_argument(suffix, self.user_agent)
        if argument is not None:
            self.prt(f'{self.user["username"]}参数获取成功!')
        else:
            self.prt(f'{self.user["username"]}参数获取失败!')
            return False
        # 获取cookie
        cookie = self.get_cookie(argument['cookie.txt'], argument['dfpUrl'], user_agent)
        if cookie is not None:
            self.prt(f'{self.user["username"]}取得cookie!')
        else:
            self.prt(f'{self.user["username"]}无法取得cookie!')
            return False
        # 判断是否被注册
        is_reg = self.cheek_have(user_agent, argument, self.user, cookie)
        if not is_reg:
            self.prt(f'{self.user["username"]}可以进行注册!')
        else:
            self.prt(f'{self.user["username"]}该账号已存在!')
            return True
        # 验证参数
        rps = self.cheek_data(self.user, user_agent, argument, self.gj, cookie)
        if rps is not None:
            self.prt(f'{self.user["username"]}参数验证完成!')
        else:
            self.prt(f'{self.user["username"]}参数验证失败!')
            return False
        # 开始获取token
        self.prt(f'{self.user["username"]}开始打码(1-10s)!')
        token = self.token_api.get_token(rps['arkoseBlob'], user_agent)
        if token:
            self.da_ma_num += 1  # 当前账号打码次数
            self.root.token_total += 1  # 总打码次数
            self.prt(f'{self.user["username"]}获取token成功,token:{token}')
        else:
            self.prt(f'{self.user["username"]}获取token失败! token:{token}')
            return False
        # 开始注册
        regs = self.regis(self.user, self.gj, rps, argument, token, user_agent, cookie)
        if regs:
            return True
        else:
            # 注册失败，判断是不是因为代理返回超时但是实际已经注册成功
            time.sleep(8)
            is_reg = self.cheek_have(user_agent, argument, self.user, cookie)
            print(self.prt(f'{self.user["username"]}is_reg:{is_reg}'))
            if is_reg:
                return True
            else:
                # 失败
                self.prt(f'{self.user["username"]}返回‘zcsb’')
                return 'zcsb'

    # 获取必须的参数
    def get_argument(self, suffix, user_agent):
        self.market = market_data.market_data[suffix]
        url = f'https://signup.live.com/?{self.market}lic=1'
        headers = {
            'Host': 'signup.live.com',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US',
        }

        def req():
            try:
                return self.session.post(url=url, headers=headers, proxies=self.proxy)
            except Exception as e:
                exception_type = type(e)
                print(str(e))
                self.prt(f'{self.user["username"]}{exception_type}')
                self.proxy = self.proxy_api.get_proxy()
                return self.session.post(url=url, headers=headers, proxies=self.proxy)

        rps = req()
        cookie = rps.headers['Set-Cookie']
        rps = rps.text
        re_s = re.compile(r'sHipFid":"(?P<key>.*?)"', re.S)
        HFId = re_s.search(rps).group('key')
        re_s = re.compile(r'urlDfp":"(?P<key>.*?)"', re.S)
        dfpUrl = re_s.search(rps).group('key')
        uaid = dfpUrl.split('session_id=')[-1].split('&CustomerId')[0]
        re_s = re.compile(r'apiCanary":"(?P<key>.*?)"', re.S)
        apiCanary = re_s.search(rps).group('key')
        apiCanary = unescape_unicode_sequences(apiCanary)
        if HFId != '' and dfpUrl != '' and uaid != '' and apiCanary != '':
            return {
                'HFId': HFId,
                'dfpUrl': dfpUrl,
                'uaid': uaid,
                'apiCanary': apiCanary.encode('utf-8'),
                'cookie.txt': cookie
            }
        else:
            return None

    # 获取验证的时候需要的cookie
    def get_cookie(self, cookie, dfpUrl, user_agent):
        headers = {
            'Host': 'signup.live.com',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'cookie': cookie,
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US',
        }

        def req(dfpUrl, headers):
            try:
                d = self.session.post(url=dfpUrl, headers=headers)
                return d
            except Exception as e:
                exception_type = type(e)
                self.prt(f'{self.user["username"]}{exception_type}')

        rps = req(dfpUrl, headers)
        if rps.headers.get('Set-Cookie') is not None:
            cookie += rps.headers['Set-Cookie']
            if self.market != '':
                cookie = cookie.replace(' domain=.live.com; path=/; secure; httponly, ', "")
                cookie = cookie.replace(' secure; HttpOnly; SameSite=None, ', '')
            return cookie
        else:
            return None

    # 验证账号是否被注册
    def cheek_have(self, user_agent, argument, user, cookie):
        headers = {
            'Host': 'signup.live.com',
            'Connection': 'keep-alive',
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US',
            'Cookie': cookie,
            'Origin': 'https://signup.live.com',
            'Referer': 'https://signup.live.com/?lic=1',
            'hpgid': '200225',
            'Content-Type': 'application/json; charset=utf-8',
            'canary': argument['apiCanary'],
            'client-request-id': argument['uaid'],
            'correlationId': argument['uaid']
        }
        url = f'https://signup.live.com/API/CheckAvailableSigninNames?lic=1'
        data = {
            'signInName': user['username'],
            'uaid': argument['uaid'],
            'includeSuggestions': True,
            'uiflvr': 1001,
            'scid': 100118,
            'hpgid': 200225
        }
        data = json.dumps(data)

        def req():
            try:
                s = self.session.post(url, data=data, headers=headers, proxies=self.proxy).text
                s = json.loads(s)
                ss = s['isAvailable']
                return ss
            except Exception as e:
                exception_type = type(e)
                if exception_type == KeyError:
                    return True
                self.prt(f'{self.user["username"]}{exception_type}')
                self.proxy = self.proxy_api.get_proxy()
                return req()

        s = req()
        # self.cookie = cookie
        if s:
            return False
        else:
            return True

    # 校验数据是否正确
    def cheek_data(self, user, user_agent, argument, gj, cookie):
        url = f'https://signup.live.com/API/CreateAccount?lic=1'
        headers = {
            'Host': 'signup.live.com',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US',
            'Cookie': cookie,
            'Origin': 'https://signup.live.com',
            'Referer': f'https://signup.live.com/?lic=1',
            'hpgid': '200225',
            'Content-Type': 'application/json; charset=utf-8',
            'canary': argument['apiCanary'],
            'client-request-id': argument['uaid'],
            'correlationId': argument['uaid']
        }
        data = {
            'BirthDate': user['birthdate'],
            'CheckAvailStateMap': [f'{user["username"]}:false'],
            'Country': gj,
            'EvictionWarningShown': [],
            'FirstName': user['firstName'],
            'IsRDM': False,
            'IsOptOutEmailDefault': False,
            'IsOptOutEmailShown': 1,
            'IsOptOutEmail': False,
            'IsUserConsentedToChinaPIPL': False,
            'LastName': user['lastName'],
            'LW': 1,
            'MemberName': user['username'],
            'RequestTimeStamp': datetime.utcnow().isoformat(timespec='milliseconds') + 'Z',
            'ReturnUrl': '',
            'SignupReturnUrl': '',
            'SuggestedAccountType': 'EASI',
            'SiteId': '68692',
            'VerificationCode': '',
            'VerificationCodeSlt': '',
            'WReply': '',
            'Password': user['password'],
            'MemberNameChangeCount': 1,
            'MemberNameAvailableCount': 1,
            'MemberNameUnavailableCount': 0,
            'uiflvr': '1001',
            'scid': '100118',
            'uaid': argument['uaid'],
            'hpgid': '200225'
        }
        data = json.dumps(data)

        def req():
            try:
                return self.session.post(headers=headers, data=data, url=url, proxies=self.proxy).text
            except Exception as e:
                exception_type = type(e)
                self.prt(f'{self.user["username"]}{exception_type}')
                self.proxy = self.proxy_api.get_proxy()
                return req()

        rps = req()
        rps = json.loads(rps)
        # self.prt(f'{self.user["username"]}{rps}')
        if rps['error']['code'] == '1041':
            info = rps['error']['data']
            re_s = re.compile(r'repMapRequestIdentifierDetails":"(?P<key>.*?)"', re.S)
            repMapRequestIdentifierDetails = re_s.search(info).group('key')
            repMapRequestIdentifierDetails = unescape_unicode_sequences(repMapRequestIdentifierDetails)
            re_s = re.compile(r'arkoseBlob":"(?P<key>.*?)"', re.S)
            arkoseBlob = re_s.search(info).group('key')
            arkoseBlob = unescape_unicode_sequences(arkoseBlob)
            re_s = re.compile(r'"riskAssessmentDetails":"(?P<key>.*?)"', re.S)
            riskAssessmentDetails = re_s.search(info).group('key')
            riskAssessmentDetails = unescape_unicode_sequences(riskAssessmentDetails)
            return {
                'repMapRequestIdentifierDetails': repMapRequestIdentifierDetails,
                'arkoseBlob': arkoseBlob,
                'riskAssessmentDetails': riskAssessmentDetails,
                'headers': headers,
                'argument': argument
            }
        else:
            return None

    # 最后一步注册邮箱
    def regis(self, user, gj, rps, argument, token, user_agent, cookie):
        headers = {
            'Host': 'signup.live.com',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US',
            'Cookie': cookie,
            'Origin': 'https://signup.live.com',
            'Referer': f'https://signup.live.com/?lic=1',
            'hpgid': '200225',
            'Content-Type': 'application/json; charset=utf-8',
            'canary': argument['apiCanary'],
            'client-request-id': argument['uaid'],
            'correlationId': argument['uaid']
        }
        data = {
            'BirthDate': user['birthdate'],
            'CheckAvailStateMap': [f'{user["username"]}:false'],
            'Country': gj,
            'EvictionWarningShown': [],
            'FirstName': user['firstName'],
            'IsRDM': False,
            'IsOptOutEmailDefault': False,
            'IsOptOutEmailShown': 1,
            'IsOptOutEmail': False,
            'IsUserConsentedToChinaPIPL': False,
            'LastName': user['lastName'],
            'LW': 1,
            'MemberName': user['username'],
            'RequestTimeStamp': datetime.utcnow().isoformat(timespec='milliseconds') + 'Z',
            'ReturnUrl': '',
            'SignupReturnUrl': '',
            'SuggestedAccountType': 'EASI',
            'SiteId': '68692',
            'VerificationCode': '',
            'VerificationCodeSlt': '',
            'WReply': '',
            'Password': user['password'],
            'MemberNameChangeCount': 1,
            'MemberNameAvailableCount': 1,
            'MemberNameUnavailableCount': 0,
            'RiskAssessmentDetails': rps['riskAssessmentDetails'],
            'RepMapRequestIdentifierDetails': rps['repMapRequestIdentifierDetails'],
            # 'arkoseBlob': rps['arkoseBlob'],
            'HFId': argument['HFId'],
            'HPId': 'B7D8911C-5CC8-A9A3-35B0-554ACEE604DA',
            'HSol': token,
            'HType': 'enforcement',
            'HId': token,
            'uiflvr': '1001',
            'scid': '100118',
            'uaid': argument['uaid'],
            'hpgid': '200225',
        }
        data = json.dumps(data)
        url = f'https://signup.live.com/API/CreateAccount?ilc=1'

        def req():
            try:
                rr = self.session.post(headers=headers, data=data, url=url, proxies=self.proxy)
                return rr
            except Exception as e:
                exception_type = type(e)
                self.prt(f'{self.user["username"]}{exception_type}')
                self.proxy = self.proxy_api.get_proxy()
                return req()

        rr = req()
        r = json.loads(rr.text)
        self.prt(f'{self.user["username"]}{r}')
        if r.get('redirectUrl') is not None and r.get('redirectUrl') != '':
            try:
                self.regis_data = {
                    'redirectUrl': r.get('redirectUrl'),
                    'slt': r.get('slt')
                }
            except:
                pass
            return True
        else:
            return False

    # 输出日志
    def prt(self, s):
        print(f'[日志{datetime.now()}]:{s}')

    def change_cell_value(self, tree, row_id, column, new_value):
        # 获取当前行的数据
        current_values = tree.item(row_id, 'values')
        # 更新指定列的值
        values = []
        for i in current_values:
            values.append(i)
        values[column] = new_value
        # 更新行的数据
        tree.item(row_id, values=values)
