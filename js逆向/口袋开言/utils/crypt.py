import execjs

def encrypt(data):
    data = execjs.compile(open('utils/loader.js', encoding='utf-8').read()).call('encrypt', data)

    return data


def decrypt(data):
    data = execjs.compile(open('utils/loader.js', encoding='utf-8').read()).call('decrypt', data)

    return data