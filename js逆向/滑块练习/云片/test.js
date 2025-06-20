window = global;
const JSEncrypt = require('jsencrypt');
publickey = "-----BEGIN PUBLIC KEY-----MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDnOWe/gs033L/2/xR3oi6SLAMPBY5VledUqqH6dbCNOdrGX4xW+1x6NUfvmwpHRBA2C7xWDDvOIldTl0rMtERTDy9homrVqEcW6/TY+dSVFL3e2Yg2sVaehHv7FhmATkgfC2FcXt8Wvm99QpKRSrGKpcFYJwOj2F8hJh+rTG0IPQIDAQAB-----END PUBLIC KEY-----"

//加密
let jse = new JSEncrypt();
jse.setPublicKey(publickey);
var enStr = jse.encrypt('123456');

console.log(enStr)