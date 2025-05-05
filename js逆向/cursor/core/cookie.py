import base64
import uuid


def get_session_user_id():
    """
    获取cookie里面的一个动态值： IndrX2ZuSmZramJSX0NIYUZoRzRzUGZ0cENIVHpHNXk0VE0ya2ZiUkVzQU14X2Fub255bW91c1VzZXJJZCI%3D
    :return: 
    """
    input_string = str(uuid.uuid4())

    # 对字符串进行 Base64 编码
    encoded_string = base64.b64encode(input_string.encode('utf-8')).decode('utf-8')
    return encoded_string




