const CryptoJS = require("crypto-js");

function aesEncrypt(data, key, iv) {
  // 将 key 和 iv 数组转换为 WordArray（CryptoJS 内部数据格式）
  const keyWordArray = CryptoJS.enc.Utf8.parse(String.fromCharCode(...key));
  const ivWordArray = CryptoJS.enc.Utf8.parse(String.fromCharCode(...iv));

  // 执行 AES 加密
  const encrypted = CryptoJS.AES.encrypt(data, keyWordArray, {
    iv: ivWordArray,
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.Pkcs7
  });

  return encrypted.toString();  // 返回加密后的密文（字符串）
}

function aesDecrypt(encryptedData, key, iv) {
  // 将 key 和 iv 数组转换为 WordArray（CryptoJS 内部数据格式）
  const keyWordArray = CryptoJS.enc.Utf8.parse(String.fromCharCode(...key));
  const ivWordArray = CryptoJS.enc.Utf8.parse(String.fromCharCode(...iv));

  // 执行 AES 解密
  const decrypted = CryptoJS.AES.decrypt(encryptedData, keyWordArray, {
    iv: ivWordArray,
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.Pkcs7
  });

  // 返回解密后的明文字符串
  return decrypted.toString(CryptoJS.enc.Utf8);
}

// 测试示例
const key = [ 1160790837, 875835697, 927023429, 877016627 ];  // 16 字节
const iv = [ 909325872, 825517105, 926115120, 875835449 ]

console.log("")
