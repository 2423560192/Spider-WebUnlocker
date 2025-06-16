window = global;


var lj = window,
    lk = lj["document"],
    ll = lj["location"],
    lm = lj["navigator"],
    lo = lj["screen"],
    lp = lj["eval"],
    lq = lj["Function"],
    ls = lj["Math"],
    lu = Object["create"] || function (ba) {
        return oG["prototype"] = ba, ba = new oG(), oG["prototype"] = null, ba;
    },
    lv = {
        "extend": function (ba) {
            var cR = lu(this);
            return ba && cR["Db"](ba), cR["hasOwnProperty"]("init") || this["g"] !== cR["g"] || (cR["g"] = function () {
                cR["Jb"]["g"]["apply"](this, arguments);
            }), (cR["g"]["prototype"] = cR)["Jb"] = this, cR;
        },
        "create": function () {
            var ba = this["extend"]();
            return ba["g"]["apply"](ba, arguments), ba;
        },
        "g": function () {
        },
        "Db": function (ba) {
            for (var cR in ba) ba["hasOwnProperty"](cR) && (this[cR] = ba[cR]);
            ba["hasOwnProperty"]("toString") && (this["toString"] = ba["toString"]);
        },
        "clone": function () {
            return this["g"]["prototype"]["extend"](this);
        }
    },
    lw = {
        "stringify": function (ba) {
            var cR = ba["m"];
            ba = ba["i"];
            for (var e5 = [], eh = 0; eh < ba; eh++) {
                var bp = cR[eh >>> 2] >>> 24 - eh % 4 * 8 & 255;
                e5["push"]((bp >>> 4)["toString"](16)), e5["push"]((15 & bp)["toString"](16));
            }
            return e5["join"]('');
        },
        "parse": function (ba) {
            for (var cR = ba["length"], e5 = [], eh = 0; eh < cR; eh += 2) e5[eh >>> 3] |= parseInt(ba["substr"](eh, 2), 16) << 24 - eh % 8 * 4;
            return new lx["g"](e5, cR / 2);
        }
    },
    lx = lv["extend"]({
        "g": function (ba, cR) {
            ba = this["m"] = ba || [], this["i"] = null != cR ? cR : 4 * ba["length"];
        },
        "toString": function (ba) {
            return (ba || lw)["stringify"](this);
        },
        "concat": function (ba) {
            var cR = this["m"],
                e5 = ba["m"],
                eh = this["i"];
            if (ba = ba["i"], this["Oa"](), eh % 4) for (var bp = 0; bp < ba; bp++) cR[eh + bp >>> 2] |= (e5[bp >>> 2] >>> 24 - bp % 4 * 8 & 255) << 24 - (eh + bp) % 4 * 8; else for (bp = 0; bp < ba; bp += 4) cR[eh + bp >>> 2] = e5[bp >>> 2];
            return this["i"] += ba, this;
        },
        "Oa": function () {
            var ba = this["m"],
                cR = this["i"];
            ba[cR >>> 2] &= 4294967295 << 32 - cR % 4 * 8, ba["length"] = Math["ceil"](cR / 4);
        },
        "clone": function () {
            var ba = lv["clone"]["call"](this);
            return ba["m"] = this["m"]["slice"](0), ba;
        },
        "random": function (ba) {
            for (var cR = [], e5 = 0; e5 < ba; e5 += 4) {
                var eh = function (ba) {
                        var cR = 987654321;
                        return function () {
                            return ((((cR = 36969 * (65535 & cR) + (cR >> 16) & 4294967295) << 16) + (ba = 18000 * (65535 & ba) + (ba >> 16) & 4294967295) & 4294967295) / 4294967296 + 0.5) * (0.5 < Math["random"]() ? 1 : -1);
                        };
                    }(4294967296 * (bp || Math["random"]())),
                    bp = 987654071 * eh();
                cR["push"](4294967296 * eh() | 0);
            }
            return new lx["g"](cR, ba);
        }
    }),
    ly = function (ba) {
        var cR = ba["m"];
        ba = ba["i"];
        for (var e5 = [], eh = 0; eh < ba; eh++) e5["push"](String["fromCharCode"](cR[eh >>> 2] >>> 24 - eh % 4 * 8 & 255));
        return e5["join"]('');
    },
    lz = function (ba) {
        for (var cR = ba["length"], e5 = [], eh = 0; eh < cR; eh++) e5[eh >>> 2] |= (255 & ba["charCodeAt"](eh)) << 24 - eh % 4 * 8;
        return new lx["g"](e5, cR);
    };


console.log(lz("E0C544117AAE4F63"))
bl = "E0C544117AAE4F63"
bm = "636014d173e04409"
key = lz(unescape(encodeURIComponent(bl)))
iv = lz(unescape(encodeURIComponent(bm)))
console.log(key)
console.log(iv)
console.log(lz(unescape(encodeURIComponent("123456"))))

