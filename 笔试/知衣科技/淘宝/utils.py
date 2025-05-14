from CoreUtils.Encrypt import md5_encrypt


def get_sign(token, tt, appKey, data):
    print(token)
    print(tt)
    print(appKey)
    print(data)
    print('----------------')
    return md5_encrypt(token + "&" + tt + "&" + appKey + "&" + data)
