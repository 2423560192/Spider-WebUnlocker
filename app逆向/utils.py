def query_to_dict(s):
    return {item.split('=')[0]: item.split('=')[1] for item in s.split('&')}


def header_str_to_dict(header_str):
    res = [item for item in
           header_str.split('\n')]
    res = res[1:len(res) - 1]
    d = {item.split('\t')[0]: item.split('\t')[1] for item in res}
    return d

# aes 加密
###aes的加密
# aes加密方法  pip3 install pycryptodome
from Crypto.Cipher import AES
import base64
def pad_data(data):
    # 计算需要填充的字节数
    pad_len = AES.block_size - (len(data) % AES.block_size)
    # 使用填充字节进行填充
    padding = bytes([pad_len] * pad_len)
    padded_data = data + padding
    return padded_data
def encrypt_data(password):
    # 创建 AES 密码对象
    # cipher = AES.new(key, AES.MODE_CBC, iv)
    # 密钥（16 字节）
    key = b'6d6656a37cdb7977c10f6d83cab168e9'
    # 初始化向量（16 字节）
    iv = b'0000000000000000'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 填充数据
    padded_data = pad_data(password.encode('utf-8'))
    print(padded_data)
    # 加密数据
    encrypted_data = cipher.encrypt(padded_data)
    return base64.b64encode(encrypted_data).decode('utf-8')



if __name__ == '__main__':
    s = 'appId=32&hashSign=8356ebae71a0aa643f87ad4c5691a456&imgUrl=&lat=29.568295&lng=106.559123&loginName=18953675221&nickName=&openId=&place=%E9%87%8D%E5%BA%86&pwd=25d55ad283aa400af464c76d713c07ad&sessionId=392032c5-09c8-4c3c-bb17-16a1dc49f7fc&token=&type='
    print(query_to_dict(s))
    h = '''
Mobile-Token	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxNjcxMTMyMDA2MDczNjA2MTQ1IiwiZXhwIjoxNzQyNTcwMDYxLCJpYXQiOjE3NDI1NjY0NjEsInVzZXJJZCI6IjE2NzExMzIwMDYwNzM2MDYxNDUiLCJ1c2VybmFtZSI6IjE3NzE3ODIzMjQ0In0.7U5BIQ6rJ1EqNpXe5lvlHEMY4YVwSLDADTGKXN3SXqQ
Content-Type	application/json
user-agent	Mozilla/5.0 (Linux; Android 11; Pixel 2 XL Build/RP1A.201005.004.A1; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/28.0)
Host	miappshop.jshulin.com
Connection	Keep-Alive
Accept-Encoding	gzip
    '''
    print(header_str_to_dict(h))
