const CryptoJS = require('crypto-js');




// 模拟从服务器获取的密钥和 IV
const key = CryptoJS.lib.WordArray.create([
  1228432451,
  1215312982,
  1431131496,
  1265725516,
  1648449614,
  1228034390
], 24);

const iv = CryptoJS.lib.WordArray.create([
  842019381,
  808792119
], 8);

// 要解密的密文（Base64字符串）
const ciphertextBase64 = 'VLr+acX0cxAhGTRoj4LR/NkIIOgBWzIHOIRMrSE0novqkFd0qnwVr+VWjbdc8j5EeE9sg+yD96lXPcUDvfxE0MgfixLDb9SZ6t4vlU23FTqTGeUX2MqFT4Vd76A6qbbU2hi8zv75uUyuVOAQZ7D+mcMrkqpItnfgPq/Qz9wdh/xlC8UHzC+kA0tFapxn0jhadG2+F+UDQendRRXawziaTChMU2GXIBwNILmBsfMa7W+gr6Bcu9NGTTjZh/c4MYoo67ZdaL/CDBFKJ3Ot1OJ6Jadwfr2JQRG5psr70AZr4UCoBwzB9W3shafgduG6vsfkSJS70xuvaOkvHZCE7SqF871R3zAVHP3UK7cuT3myUyTvHfLKpJVZRw05aNOMbOVKBpW6CcQDaNPcBXmU9y1b2iDXO41oF6dTFFHwasLKdULNCLHRouwPNJGsjEVy6AUNqVjLKS2KtKaQ8oVmKbnZEG3JZCdn4ND2S5ldZn/hfV4FdstVu5CKICkDeivhjqjwMfx3w0xWtcMqLadFiO+uC8qsCik7rMudD+QkDb+eESA+ReQg1hxdDsNeleiAyYuaM6AzHl8/wsrMlobKZYU1dhY6sKQ3GC4FfNhlVPlrj70ISKuGr4fLF+V39rOwc1yEXXlFzTy7kYkkrnLO/SJNt51hgcRdaR6xyU07YTo80bYUiq2k8lcNbQK2xO3ahk1KmyrgFQS8sIiV8YmgwUUy7CFktExg8WAaWacuUrkX/SeyuoCvT17Ocj7LppE+QzpD6/q6IKpbS0Q=';

// 解密
const decrypted = CryptoJS.TripleDES.decrypt(ciphertextBase64, key, {
  iv: iv,
  mode: CryptoJS.mode.CBC,
  padding: CryptoJS.pad.Pkcs7
});

// 转为 UTF-8 字符串
const plaintext = CryptoJS.enc.Utf8.stringify(decrypted);

console.log("解密结果:", plaintext);
