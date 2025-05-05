import json

import execjs


def jiemi(data):
    # 加载 JavaScript 解密代码
    js_code = execjs.compile(open('utils/loader.js', 'r', encoding='utf-8').read())

    decrypted_data = json.loads(json.dumps(js_code.call('l', data)))['data']

    return decrypted_data