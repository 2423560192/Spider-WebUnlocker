header = {
    "AppType": 2,
    "AppVersion": "3.3.5",
    "BusinessType": 1,
    "Channel": "bdw",
    "ClientType": "5",
    "DeviceManufacture": "devtools",
    "DeviceModel": "iPhone 12/13 (Pro)",
    "MessageId": "9b2fd883-3bec-392e-90d0-04f64015e0a7",
    "OsVersion": "iOS 10.0.1",
    "Timestamp": 1739455753045,
    "content-type": "application/json",
    "pageNo": 1,
    "pageSize": 20
}


var end = "%2Fbase%2Fapp%2Fstore%2FlistV2"


function md5(s) {
    const CryptoJs = require("crypto-js")
    return CryptoJs.MD5(s).toString();

}

function R(n, e, t, r, o, u, i, a, s, f) {
    var d = "987EBBF8450544D7A52D5539DF9A92A2"
        , l = "";
    return l = s ? "AppVersion=".concat(u, "Authorization=").concat(s, "Channel=").concat(i, "ClientType=").concat(o, "DeviceManufacture=").concat(t, "DeviceModel=").concat(r, "MessageId=").concat(a, "OsVersion=").concat(e, "Timestamp=").concat(n, "AppKey=").concat(d, "Url=").concat(f) : "AppVersion=".concat(u, "Channel=").concat(i, "ClientType=").concat(o, "DeviceManufacture=").concat(t, "DeviceModel=").concat(r, "MessageId=").concat(a, "OsVersion=").concat(e, "Timestamp=").concat(n, "AppKey=").concat(d, "Url=").concat(f),
        l = md5(l.replace(/\s*/g, "")).substring(4, 28).toLocaleUpperCase();
}


function get_sign(header) {
    var t = header
        , o = t.OsVersion
        , u = t.DeviceManufacture
        , i = t.DeviceModel
        , c = t.ClientType
        , a = t.AppVersion
        , f = t.Channel
        , d = t.MessageId
        , p = t.Authorization;
    return R(header.Timestamp, o, u, i, c, a, f, d, p, end)
}



