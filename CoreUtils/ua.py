import random

from fake_useragent import UserAgent


def get_random_ua():
    # 实例化UserAgent类创建了一个UserAgent对象
    # 实例化对象语法：对象 = 类名( )
    ua = UserAgent()

    # 输出ua，可以看到ua是一个UserAgent对象
    print(ua.random)
    return ua.random



