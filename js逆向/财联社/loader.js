window = global

require('./mod1');
require('./mod2');
require('./mod3');
!function (e) {
    function r(r) {
        for (var n, u, i = r[0], f = r[1], c = r[2], p = 0, s = []; p < i.length; p++)
            u = i[p],
            Object.prototype.hasOwnProperty.call(o, u) && o[u] && s.push(o[u][0]),
                o[u] = 0;
        for (n in f)
            Object.prototype.hasOwnProperty.call(f, n) && (e[n] = f[n]);
        for (l && l(r); s.length;)
            s.shift()();
        return a.push.apply(a, c || []),
            t()
    }

    function t() {
        for (var e, r = 0; r < a.length; r++) {
            for (var t = a[r], n = !0, i = 1; i < t.length; i++) {
                var f = t[i];
                0 !== o[f] && (n = !1)
            }
            n && (a.splice(r--, 1),
                e = u(u.s = t[0]))
        }
        return e
    }

    var n = {}
        , o = {
        1: 0
    }
        , a = [];

    function u(r) {
        if (n[r])
            return n[r].exports;
        var t = n[r] = {
            i: r,
            l: !1,
            exports: {}
        }
            , o = !0;
        try {
            console.log("t:::", t)
            e[r].call(t.exports, t, t.exports, u),
                o = !1
        } finally {
            o && delete n[r]
        }
        return t.l = !0,
            t.exports
    }

    window.loader = u;
    u.e = function (e) {
        var r = []
            , t = o[e];
        if (0 !== t)
            if (t)
                r.push(t[2]);
            else {
                var n = new Promise((function (r, n) {
                        t = o[e] = [r, n]
                    }
                ));
                r.push(t[2] = n);
                var a, i = document.createElement("script");
                i.charset = "utf-8",
                    i.timeout = 120,
                u.nc && i.setAttribute("nonce", u.nc),
                    i.src = function (e) {
                        return u.p + "static/chunks/" + ({}[e] || e) + "." + {
                            65: "171ca62a04a6be76f495",
                            66: "f2e18edd4b3b1ee68f7d",
                            67: "6b03fbeba14fe7563455",
                            68: "aa9bfb31d6a18a5f8e5a"
                        }[e] + ".js"
                    }(e);
                var f = new Error;
                a = function (r) {
                    i.onerror = i.onload = null,
                        clearTimeout(c);
                    var t = o[e];
                    if (0 !== t) {
                        if (t) {
                            var n = r && ("load" === r.type ? "missing" : r.type)
                                , a = r && r.target && r.target.src;
                            f.message = "Loading chunk " + e + " failed.\n(" + n + ": " + a + ")",
                                f.name = "ChunkLoadError",
                                f.type = n,
                                f.request = a,
                                t[1](f)
                        }
                        o[e] = void 0
                    }
                }
                ;
                var c = setTimeout((function () {
                        a({
                            type: "timeout",
                            target: i
                        })
                    }
                ), 12e4);
                i.onerror = i.onload = a,
                    document.head.appendChild(i)
            }
        return Promise.all(r)
    }
        ,
        u.m = e,
        u.c = n,
        u.d = function (e, r, t) {
            u.o(e, r) || Object.defineProperty(e, r, {
                enumerable: !0,
                get: t
            })
        }
        ,
        u.r = function (e) {
            "undefined" !== typeof Symbol && Symbol.toStringTag && Object.defineProperty(e, Symbol.toStringTag, {
                value: "Module"
            }),
                Object.defineProperty(e, "__esModule", {
                    value: !0
                })
        }
        ,
        u.t = function (e, r) {
            if (1 & r && (e = u(e)),
            8 & r)
                return e;
            if (4 & r && "object" === typeof e && e && e.__esModule)
                return e;
            var t = Object.create(null);
            if (u.r(t),
                Object.defineProperty(t, "default", {
                    enumerable: !0,
                    value: e
                }),
            2 & r && "string" != typeof e)
                for (var n in e)
                    u.d(t, n, function (r) {
                        return e[r]
                    }
                        .bind(null, n));
            return t
        }
        ,
        u.n = function (e) {
            var r = e && e.__esModule ? function () {
                        return e.default
                    }
                    : function () {
                        return e
                    }
            ;
            return u.d(r, "a", r),
                r
        }
        ,
        u.o = function (e, r) {
            return Object.prototype.hasOwnProperty.call(e, r)
        }
        ,
        u.p = "",
        u.oe = function (e) {
            throw console.error(e),
                e
        }
    ;
    var i = window.webpackJsonp = window.webpackJsonp || []
        , f = i.push.bind(i);
    i.push = r,
        i = i.slice();
    for (var c = 0; c < i.length; c++)
        r(i[c]);
    var l = f;
    t()
}([]);

function get_sign() {
    let data = {os: 'web', sv: '7.7.5', app: 'CailianpressWeb'}
    return window.loader('W2Yj')(data)
}

// console.log(window.loader('W2Yj'))
console.log()



