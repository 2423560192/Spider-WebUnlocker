require('./uitl')
const CryptoJs = require("crypto-js")


function encrypt(data) {
    sign = data['data']['sign']
    track = data['data']['track']
    key = data['aesKey']


    data = JSON.stringify({'sign': sign, 'track': track})
    
    data = CryptoJs.enc.Utf8.parse(data);

    key = CryptoJs.enc.Utf8.parse(key);

    //AES加密
    cfg = {
        mode: CryptoJs.mode.ECB,
        padding: CryptoJs.pad.Pkcs7
    };
    let res = CryptoJs.AES.encrypt(data, key, cfg).toString()

    return res
}


function get_data(checkId, clientIp, key, uuid, track) {
    track = JSON.parse(track)

    sign_param = clientIp + checkId + uuid + splicing(track)

    sign = CryptoJs.MD5(sign_param).toString();
    res = encrypt({
        'data': {
            'sign': sign,
            'track': track
        },
        'aesKey': key
    })

    return res
}

if (typeof process !== 'undefined' && process.argv.length > 2) {
    const checkId = process.argv[2];
    const clientIp = process.argv[3];
    const key = process.argv[4];
    const uuid = process.argv[5];
    const track = process.argv[6];

    const result = get_data(checkId, clientIp, key, uuid, track);
    console.log(result);
}

