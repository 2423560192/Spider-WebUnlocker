# python3
# 接口类型：互亿无线触发短信接口，支持发送验证码短信、订单通知短信等。
# 账户注册：请通过该地址开通账户https://user.ihuyi.com/new/register.html
# 注意事项：
# （1）调试期间，请用默认的模板进行测试，默认模板详见接口文档；
# （2）请使用 用户名 及 APIkey来调用接口，APIkey在会员中心可以获取；
# （3）该代码仅供接入互亿无线短信接口参考使用，客户可根据实际需要自行编写；

import random
import urllib.parse
import urllib.request


def get_code(num=4):
    """
    生成指定位数的验证码，如果不传值，就默认生成4位的验证码
    :param num: 要生成几位的验证码
    :return: 生成的验证码
    """
    return random.randint(
        int('1{}'.format('0' * (num - 1))),
        int('9{}'.format('9' * (num - 1)))
    )


def send_sms(mobile, account, password, content, code_num=4):
    """
    发送短信验证码
    :param mobile: 你要发给谁
    :param code_num: 发送几位的验证码
    :return:
    """
    # 接口地址，咱们不需要更改
    url = 'http://106.ihuyi.com/webservice/sms.php?method=Submit'

    # 验证码
    code = get_code()
    # 定义请求的数据
    values = {
        'account': 'C46751567',  # 这个是对应的APIID
        'password': '07b6e37c10dc281ef100b878cf0e4874',  # 这个是对应的APIKEY
        'mobile': mobile,  # 发给谁
        'content': '您的验证码是：{}。请不要把验证码泄露给其他人。'.format(code),
        # 没有购买套餐的，这个模板只能使用默认的，即你收到的短信长这样：【互亿无线】您的验证码是：7835。请不要把验证码泄露给其他人。
        'format': 'json',  # 不要动
    }

    # 将数据进行编码，下面代码不要动
    data = urllib.parse.urlencode(values).encode(encoding='UTF8')

    # 发起请求，下面代码不要动
    req = urllib.request.Request(url, data)
    response = urllib.request.urlopen(req)
    res = response.read()

    # 打印结果，然后你的手机应该就能接到短信了
    print(res.decode("utf8"))  # {"code":2,"msg":"提交成功","smsid":"16842079209571524017"}
    return code
