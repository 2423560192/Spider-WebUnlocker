require('./env')
require('./aes')

const axios = require('axios');



// var hostname = '../mock/';//本地测试
var hostname = 'https://gd.10086.cn/apph5/openapi/app/handle2';//正式
var rsa = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAs4VXnzCnGoOr0camO/kB/KC+cM57FoIHnAVyvUOLgLWTptP76hC/FD/yBjdVHMzcBazkJuTVKvhd5Y+31YNSR3wPjMwus9re7AQdj8DI5RnZdRjXtLfKxG/PC8MlJ98rkZYXg6vp1xyo3Oq9qXJ1ff9WJOAMSAS6dfkzA+qSumw1UzpX1duhAm8QhYAbEW24Leto55uuoUKnS5LXAN8qVe5uKLueb787xQm5NTj2M3eB0w//NTiKlV3g2JsGJv8H0vShQK0ez5bR73dxyrO0qY6Xr2ri6Dp2SHNEjdclohoANkNB649tUgadGId546Fvs0Ln0VzW909LCz4vxMKmsQIDAQAB'
var aesKey = '38ef2c46b95bb5237b0312b3'


function getReqTime() {
    var date = new Date();
    return (
        date.getFullYear().toString() +
        pad2(date.getMonth() + 1) +
        pad2(date.getDate()) +
        pad2(date.getHours()) +
        pad2(date.getMinutes()) +
        pad2(date.getSeconds())
    );
}

function pad2(n) {
    return n < 10 ? "0" + n : n;
}


function getQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return r[2];
    return "";
};

/**
 * @description 请求报文加密
 * @param {string} encryptText 加密文本
 * @returns {string} 加密后的文本
 */
function encryptFn(encryptText) {
    return encryptAES(encryptText, aesKey);
}

/**
 * @description 请求报文解密
 * @param {string} decryptText 解密文本
 * @returns {string} 解密后的文本
 */
function decryptFn(decryptText) {
    return decryptAES(decryptText, aesKey);
}

const encryptionMobile = (mobile) => {
    const encrypt = new JSEncrypt();
    encrypt.setPublicKey(rsa);
    return encrypt.encrypt(mobile);
};


function axiosHTTP(data, serviceId) {
    return new Promise((resolve, reject) => {
        // var url=hostname+serviceId+'.json'
        var url = hostname
        let req = {
            publicData: {
                reqTime: getReqTime(),
                reqSeq: getReqTime() + "htSearch",
                activityId: "htSearch",
                appid: "cxcc7a4a1608df4431",
                serviceId: serviceId,
                version: "1.0"
            },
            data: data
        }
        axios.post(url, {
            data: encryptFn(JSON.stringify(req)),
            key: encryptionMobile(aesKey),
        }).then(res => {
            if (res.data.data) {
                res.data.data = JSON.parse(decryptFn(res.data.data));
            }
            setTimeout(function () {
                resolve(res.data)
            }, 300)
        }).catch(err => {
            setTimeout(function () {
                reject(err)
            }, 300)
        });
    });
}

axiosHTTP({
    servicecode: "Fe90322c88553590",
    params: {
        mobile: '17782200193'
    }
}, 'ability_customize').then(res => {
    vm.loadingShow = false;

    if (res.publicData.retInfo.retCode == 0 && res.data.result.status == 0) {
        var _frontline = res.data.result.data.frontline;
        if (_frontline === -1) {
            vm.frontline = '否'
        }
        if (_frontline === 0) {
            vm.frontline = '符合HT,不符合充送'
        }
        if (_frontline === 1) {
            vm.frontline = '不符合HT，符合充送'
        }
        if (_frontline === 2) {
            vm.frontline = '符合HT，符合充送'
        }
    } else {
        //发送失败
        alert(res.publicData.retInfo.retMsg)
    }
}).catch((err) => {
    console.log("%c Line:47 🥝 err", "color:#2eafb0", err);
    alert(errorTip)
    vm.loadingShow = false;
});

