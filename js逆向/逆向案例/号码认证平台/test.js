const CryptoJs = require("crypto-js");

let data = '123456';
let key = 'E0C544117AAE4F63';
let iv = '636014d173e04409';  // IV 必须是 16 字节

// 转换成 WordArray 类型
data = CryptoJs.enc.Utf8.parse(data);
key = CryptoJs.enc.Utf8.parse(key);
iv = CryptoJs.enc.Utf8.parse(iv);

// 配置 CBC 模式 + IV
let cfg = {
    mode: CryptoJs.mode.CBC,
    padding: CryptoJs.pad.Pkcs7,
    iv: iv
};

// 加密
let res = CryptoJs.AES.encrypt(data, key, cfg).toString();
console.log("加密结果：", res);