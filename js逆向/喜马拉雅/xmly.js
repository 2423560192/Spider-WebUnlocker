window = global;
// 引入 jsencrypt 库
const CryptoJs = require("crypto-js");
const JSEncrypt = require('jsencrypt');  // 如果你是在 Node.js 环境下使用，可以直接使用 `require`

function get_pwd(pwd) {


    const publickey = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCVhaR3Or7suUlwHUl2Ly36uVmboZ3+HhovogDjLgRE9CbaUokS2eqGaVFfbxAUxFThNDuXq/fBD+SdUgppmcZrIw4HMMP4AtE2qJJQH/KxPWmbXH7Lv+9CisNtPYOlvWJ/GHRqf9x3TBKjjeJ2CjuVxlPBDX63+Ecil2JR9klVawIDAQAB";

    let jse = new JSEncrypt();
    jse.setPublicKey(publickey);

    return jse.encrypt(pwd)
}

console.log(get_pwd('123456'))

let security_key = 'WEB-V1-PRODUCT-E7768904917C4154A925FBE1A3848BC3E84E2C7770744E56AFBC9600C267891F'


function getQueryString(e) {
    var t = ""
        , r = Object.keys(e).sort((function (e, t) {
            return (e = e.toLowerCase()) < (t = t.toLowerCase()) ? -1 : e > t ? 1 : 0
        }
    ))
        , n = r.length;
    return r.forEach((function (r, o) {
            var a = e[r];
            t += "".concat(r, "=").concat(a),
            o < n - 1 && (t += "&")
        }
    )),
        t
}

function sha1(s) {
    let encPwd = CryptoJs.SHA1(s).toString();
    return encPwd
}

function H(e) {
    var t = (0,
        getQueryString)(e) + "&" + security_key;
    console.log('t', getQueryString(e))
    return (0,
        sha1)(t.toUpperCase())
}

function get_sign(data) {
    sign = H(data)
    console.log(sign)
    return sign
}

data = {
    "account": '17782200192',
    "nonce": '0-C2C96530D74836ab627ba7b270d9eed8c7c7811c66fa1d540276ac4bed789c',
    "password": 'fAPQYIG6YH1i+LXA63T4Ng+hxvTjInmpFTaW+S1Tqy8vUgqEwhGDzOPOUsb0Jjoj0uZCUuOQR6UzeBm+uKCud4FVAJI5dbEFg28wqBT6kP/hIaQJv8+KMVSTWTUCQ8V/4kRlhTztCSp3k31JKF+A4qe7BYBQgMb9+E6XH8YrZPc=',
}

get_sign(data)
