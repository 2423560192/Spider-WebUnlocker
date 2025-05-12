const CryptoJS = require('crypto-js');

var _t = 8;


function du(e, t) {
    return e << t | e >>> 32 - t
}

function He(e, t) {
    var r = (e & 65535) + (t & 65535)
        , n = (e >> 16) + (t >> 16) + (r >> 16);
    return n << 16 | r & 65535
}

function Vt(e, t, r, n, a, o) {
    return He(du(He(He(t, e), He(n, o)), a), r)
}

function he(e, t, r, n, a, o, c) {
    return Vt(t ^ r ^ n, e, t, a, o, c)
}

function pe(e, t, r, n, a, o, c) {
    return Vt(t & n | r & ~n, e, t, a, o, c)
}

function de(e, t, r, n, a, o, c) {
    return Vt(t & r | ~t & n, e, t, a, o, c)
}

function vu(e, t, r) {
    const n = CryptoJS.enc.Utf8.parse(t)
        , a = CryptoJS.enc.Utf8.parse(r);
    return CryptoJS.AES.encrypt(e, n, {
        iv: a,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    }).toString()
}

function ve(e, t, r, n, a, o, c) {
    return Vt(r ^ (t | ~n), e, t, a, o, c)
}

function pu(e) {
    for (var t = Array(), r = (1 << _t) - 1, n = 0; n < e.length * _t; n += _t)
        t[n >> 5] |= (e.charCodeAt(n / _t) & r) << n % 32;
    return t
}

function xu(e, t) {
    e[t >> 5] |= 128 << t % 32,
        e[(t + 64 >>> 9 << 4) + 14] = t;
    for (var r = 1732584193, n = -271733879, a = -1732584194, o = 271733878, c = 0; c < e.length; c += 16) {
        var l = r
            , f = n
            , i = a
            , s = o;
        r = de(r, n, a, o, e[c + 0], 7, -680876936),
            o = de(o, r, n, a, e[c + 1], 12, -389564586),
            a = de(a, o, r, n, e[c + 2], 17, 606105819),
            n = de(n, a, o, r, e[c + 3], 22, -1044525330),
            r = de(r, n, a, o, e[c + 4], 7, -176418897),
            o = de(o, r, n, a, e[c + 5], 12, 1200080426),
            a = de(a, o, r, n, e[c + 6], 17, -1473231341),
            n = de(n, a, o, r, e[c + 7], 22, -45705983),
            r = de(r, n, a, o, e[c + 8], 7, 1770035416),
            o = de(o, r, n, a, e[c + 9], 12, -1958414417),
            a = de(a, o, r, n, e[c + 10], 17, -42063),
            n = de(n, a, o, r, e[c + 11], 22, -1990404162),
            r = de(r, n, a, o, e[c + 12], 7, 1804603682),
            o = de(o, r, n, a, e[c + 13], 12, -40341101),
            a = de(a, o, r, n, e[c + 14], 17, -1502002290),
            n = de(n, a, o, r, e[c + 15], 22, 1236535329),
            r = pe(r, n, a, o, e[c + 1], 5, -165796510),
            o = pe(o, r, n, a, e[c + 6], 9, -1069501632),
            a = pe(a, o, r, n, e[c + 11], 14, 643717713),
            n = pe(n, a, o, r, e[c + 0], 20, -373897302),
            r = pe(r, n, a, o, e[c + 5], 5, -701558691),
            o = pe(o, r, n, a, e[c + 10], 9, 38016083),
            a = pe(a, o, r, n, e[c + 15], 14, -660478335),
            n = pe(n, a, o, r, e[c + 4], 20, -405537848),
            r = pe(r, n, a, o, e[c + 9], 5, 568446438),
            o = pe(o, r, n, a, e[c + 14], 9, -1019803690),
            a = pe(a, o, r, n, e[c + 3], 14, -187363961),
            n = pe(n, a, o, r, e[c + 8], 20, 1163531501),
            r = pe(r, n, a, o, e[c + 13], 5, -1444681467),
            o = pe(o, r, n, a, e[c + 2], 9, -51403784),
            a = pe(a, o, r, n, e[c + 7], 14, 1735328473),
            n = pe(n, a, o, r, e[c + 12], 20, -1926607734),
            r = he(r, n, a, o, e[c + 5], 4, -378558),
            o = he(o, r, n, a, e[c + 8], 11, -2022574463),
            a = he(a, o, r, n, e[c + 11], 16, 1839030562),
            n = he(n, a, o, r, e[c + 14], 23, -35309556),
            r = he(r, n, a, o, e[c + 1], 4, -1530992060),
            o = he(o, r, n, a, e[c + 4], 11, 1272893353),
            a = he(a, o, r, n, e[c + 7], 16, -155497632),
            n = he(n, a, o, r, e[c + 10], 23, -1094730640),
            r = he(r, n, a, o, e[c + 13], 4, 681279174),
            o = he(o, r, n, a, e[c + 0], 11, -358537222),
            a = he(a, o, r, n, e[c + 3], 16, -722521979),
            n = he(n, a, o, r, e[c + 6], 23, 76029189),
            r = he(r, n, a, o, e[c + 9], 4, -640364487),
            o = he(o, r, n, a, e[c + 12], 11, -421815835),
            a = he(a, o, r, n, e[c + 15], 16, 530742520),
            n = he(n, a, o, r, e[c + 2], 23, -995338651),
            r = ve(r, n, a, o, e[c + 0], 6, -198630844),
            o = ve(o, r, n, a, e[c + 7], 10, 1126891415),
            a = ve(a, o, r, n, e[c + 14], 15, -1416354905),
            n = ve(n, a, o, r, e[c + 5], 21, -57434055),
            r = ve(r, n, a, o, e[c + 12], 6, 1700485571),
            o = ve(o, r, n, a, e[c + 3], 10, -1894986606),
            a = ve(a, o, r, n, e[c + 10], 15, -1051523),
            n = ve(n, a, o, r, e[c + 1], 21, -2054922799),
            r = ve(r, n, a, o, e[c + 8], 6, 1873313359),
            o = ve(o, r, n, a, e[c + 15], 10, -30611744),
            a = ve(a, o, r, n, e[c + 6], 15, -1560198380),
            n = ve(n, a, o, r, e[c + 13], 21, 1309151649),
            r = ve(r, n, a, o, e[c + 4], 6, -145523070),
            o = ve(o, r, n, a, e[c + 11], 10, -1120210379),
            a = ve(a, o, r, n, e[c + 2], 15, 718787259),
            n = ve(n, a, o, r, e[c + 9], 21, -343485551),
            r = He(r, l),
            n = He(n, f),
            a = He(a, i),
            o = He(o, s)
    }
    return Array(r, n, a, o)
}

function hu(e) {
    for (var t = "0123456789abcdef", r = "", n = 0; n < e.length * 4; n++)
        r += t.charAt(e[n >> 2] >> n % 4 * 8 + 4 & 15) + t.charAt(e[n >> 2] >> n % 4 * 8 & 15);
    return r
}

function gr(e) {
    return hu(xu(pu(e), e.length * _t))
}

function _r(e) {
    let t = gr(Date.now().toString());
    t.length < 16 && (t = t.padStart(16, "0")),
    t.length > 16 && (t = t.slice(0, 16));
    const n = vu(e, "TdSsvW3GN7YaETXo", t);
    return {
        time: t,
        encryptContent: n
    }
}

function get_sign(s) {
    s = JSON.stringify(s)

    return _r(s);
}

