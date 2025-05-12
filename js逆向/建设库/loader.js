const CryptoJS = require('crypto-js');

Bc = function (e) {
    var t = new Array
        , n = 0;
    for (var i in e)
        t[n] = i,
            n++;
    return t.sort()
}

zc = function e(t) {
    var n;
    if (Array.isArray(t)) {
        for (var r in n = new Array,
            t) {
            var o = t[r];
            for (var i in o)
                null == o[i] ? delete t[r][i] : Array.isArray(t[r][i]) && e(t[r][i])
        }
        return n = t,
            JSON.stringify(n).replace(/^(\s|")+|(\s|")+$/g, "")
    }
    return n = t && t.constructor === Object ? JSON.stringify(t) : t
}

$c = function (e) {
    var t = Bc(e)
        , n = "";
    for (var i in t) {
        var r = zc(e[t[i]]);
        null != r && "" != r.toString() && (n += t[i] + "=" + r + "&")
    }
    return n
}

Qc = function (e, t, time) {
    var n = t + e + time;
    return n =  CryptoJS.MD5(n).toString();
}

function get_sign(param, tt) {

    var time = tt;
    var t = $c(param);

    console.log("t:", t);  // 打印 $c(param) 的结果

    var intermediateSign = Qc("ZuSj0gwgsKXP4fTEz55oAG2q2p1SVGKK", t, time);
    console.log("intermediateSign:", intermediateSign);  // 打印 Qc 的中间结果

    var secondSign = Qc("mwMlWOdyM7OXbjzQPulT1ndRZIAjShDB", intermediateSign, time);
    console.log("secondSign:", secondSign);  // 打印 Qc 的第二次结果

    var finalSign = Qc("ghaepVf6IhcHmgnk4NCTXLApxQkBcvh1", secondSign, time);
    console.log("finalSign:", finalSign);  // 打印 Qc 的最终结果
    return finalSign
}