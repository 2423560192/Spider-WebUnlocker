from cursorer import Cursor

if __name__ == '__main__':
    # proxy = {
    #     "http": "http://127.0.0.1:7890",
    #     "https": "http://127.0.0.1:7890"
    # }
    cursor = Cursor()
    # 请求登录页
    cursor.get_first_request()
