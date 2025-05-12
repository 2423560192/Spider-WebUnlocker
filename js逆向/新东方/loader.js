const CryptoJS = require('crypto-js');

function get_sign(e) {
    var t = "appId=".concat("5053", "&t=").concat((new Date).getTime());
    console.log(t)
    for (var n in e)
        String(e[n]) && void 0 != e[n] && null != e[n] && "undefined" != e[n] && "null" != e[n] && (t = "".concat(t, "&").concat(n, "=").concat(e[n]));

    return {
        params: t,
        sign: CryptoJS.MD5("".concat(t).concat('750F82C2-D8F6-49F6-878C-1E7EBEBC8DA2')).toString()
    }
}

var data = {
    "cityCode": "110100",
    "pageIndex": 2,
    "pageSize": 12,
    "keyword": "%E8%8B%B1%E8%AF%AD",
    "order": "0"
}


console.log(get_sign(data)['sign']);
