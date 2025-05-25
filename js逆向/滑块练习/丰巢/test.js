const CryptoJs = require("crypto-js")

let data = '123456';
let key = 'j9eJrzqYYNnd3hOr';

data = CryptoJs.enc.Utf8.parse(data);
key = CryptoJs.enc.Utf8.parse(key);


//AES加密
cfg = {
    mode:CryptoJs.mode.ECB,
    padding:CryptoJs.pad.Pkcs7
};
let res = CryptoJs.AES.encrypt(data, key, cfg).toString()

console.log(res)