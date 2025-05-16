import datetime

from CoreUtils.Encrypt import md5_encrypt


def get_sign(token, tt, appKey, data):
    print(token)
    print(tt)
    print(appKey)
    print(data)
    print('----------------')
    return md5_encrypt(token + "&" + tt + "&" + appKey + "&" + data)


def format_timestamp(ms):
    """
    时间转换
    :param ms:
    :return:
    """
    return datetime.datetime.fromtimestamp(ms / 1000).strftime('%Y-%m-%d %H:%M:%S')