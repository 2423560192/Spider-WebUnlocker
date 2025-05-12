window = global;


require('./mod1');
require('./mod2');


!function (a) {
    function e(e) {
        for (var n, t, r = e[0], o = e[1], u = 0, i = []; u < r.length; u++)
            t = r[u],
            l[t] && i.push(l[t][0]),
                l[t] = 0;
        for (n in o)
            Object.prototype.hasOwnProperty.call(o, n) && (a[n] = o[n]);
        for (f && f(e); i.length;)
            i.shift()()
    }

    var t = {}
        , l = {
        12: 0
    };

    function c(e) {
        if (t[e])
            return t[e].exports;
        var n = t[e] = {
            i: e,
            l: !1,
            exports: {}
        };
        console.log('n:::', n)

        return a[e].call(n.exports, n, n.exports, c),
            n.l = !0,
            n.exports
    }

    window.loader = c;


    c.e = function (u) {
        var e, n = [], t = l[u];
        if (0 !== t)
            if (t)
                n.push(t[2]);
            else {
                var r = new Promise(function (e, n) {
                        t = l[u] = [e, n]
                    }
                );
                n.push(t[2] = r);
                var o, i = window.createElement('script');
                i.charset = 'utf-8',
                    i.timeout = 120,
                c.nc && i.setAttribute('nonce', c.nc),
                    i.src = c.p + '' + ({
                        0: 'loginCommon',
                        6: 'login'
                    }[e = u] || e) + '.d4f04.js',
                    o = function (e) {
                        i.onerror = i.onload = null,
                            clearTimeout(a);
                        var n = l[u];
                        if (0 !== n) {
                            if (n) {
                                var t = e && ('load' === e.type ? 'missing' : e.type)
                                    , r = e && e.target && e.target.src
                                    , o = new Error('Loading chunk ' + u + ' failed.\n(' + t + ': ' + r + ')');
                                o.type = t,
                                    o.request = r,
                                    n[1](o)
                            }
                            l[u] = undefined
                        }
                    }
                ;
                var a = setTimeout(function () {
                    o({
                        type: 'timeout',
                        target: i
                    })
                }, 12e4);
                i.onerror = i.onload = o,
                    window.getElementsByTagName('head')[0].appendChild(i)
            }
        return Promise.all(n)
    }
        ,
        c.m = a,
        c.c = t,
        c.d = function (e, n, t) {
            c.o(e, n) || (e[n] = t())
        }
        ,
        c.r = function (e) {
            'undefined' != typeof Symbol && Symbol.toStringTag && Object.defineProperty(e, Symbol.toStringTag, {
                value: 'Module'
            }),
                Object.defineProperty(e, '__esModule', {
                    value: !0
                })
        }
        ,
        c.t = function (n, e) {
            if (1 & e && (n = c(n)),
            8 & e)
                return n;
            if (4 & e && 'object' == typeof n && n && n.__esModule)
                return n;
            var t = Object.create(null);
            if (c.r(t),
                Object.defineProperty(t, 'default', {
                    enumerable: !0,
                    value: n
                }),
            2 & e && 'string' != typeof n)
                for (var r in n)
                    c.d(t, r, function (e) {
                        return n[e]
                    }
                        .bind(null, r));
            return t
        }
        ,
        c.n = function (e) {
            var n = e && e.__esModule ? function () {
                        return e['default']
                    }
                    : function () {
                        return e
                    }
            ;
            return c.d(n, 'a', n),
                n
        }
        ,
        c.o = function (e, n) {
            return Object.prototype.hasOwnProperty.call(e, n)
        }
        ,

        c.p = "/coremail/bundle/",

        c.oe = function (e) {
            throw console.error(e),
                e
        }
    ;
    var n, r, o = window.webpackJsonp = window.webpackJsonp || [], u = (n = o,
            r = [].push,
            function () {
                r.apply(n, arguments)
            }
    );
    o.push = e,
        o = o.slice();
    for (var i = 0; i < o.length; i++)
        e(o[i]);
    var f = u;
    c(c.s = 329)
}({
    329: function (e, n, t) {
        window.onreadystatechange = function () {
            Promise.all([t.e(0), t.e(6)]).then(t.t.bind(null, 338, 7))
        }
    }
});
//# sourceMappingURL=$login.d4f04.js.map
var t = '123456'



function get_sign(t) {
    var o = 'b179cfbd5e56643ad2774ffa0021a182bdb062ad2418563a4dd0159e4b5f22272eeae0e481eb6641b3b438c09d9c23a7694381007d8011ef82311ff25d4b8e28b91c7dffa37fd402717dd10ac091bc620d84a6f0f6416817745f9a3a31c2bcf442ca44bf51348eb605f8d4b453c874e723ae6444a50bb7e2e80dc754278a0283'
    var n = '10001'

    return window.loader(437).encrypt(t, o, n)

}