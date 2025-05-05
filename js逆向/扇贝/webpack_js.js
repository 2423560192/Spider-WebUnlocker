// webpack
window = global
!function (t, e) {
    "object" == typeof exports && "object" == typeof module ? module.exports = e() : "function" == typeof define && define.amd ? define([], e) : "object" == typeof exports ? exports.bays4 = e() : t.bays4 = e()
}(this, function () {
    return function (r) {
        var n = {};

        function o(t) {
            if (n[t])
                return n[t].exports;
            var e = n[t] = {
                i: t,
                l: !1,
                exports: {}
            };
            return r[t].call(e.exports, e, e.exports, o),
                e.l = !0,
                e.exports
        }

        window.d = o;

        return o.m = r,
            o.c = n,
            o.i = function (t) {
                return t
            }
            ,
            o.d = function (t, e, r) {
                o.o(t, e) || Object.defineProperty(t, e, {
                    configurable: !1,
                    enumerable: !0,
                    get: r
                })
            }
            ,
            o.n = function (t) {
                var e = t && t.__esModule ? function () {
                            return t.default
                        }
                        : function () {
                            return t
                        }
                ;
                return o.d(e, "a", e),
                    e
            }
            ,
            o.o = function (t, e) {
                return Object.prototype.hasOwnProperty.call(t, e)
            }
            ,
            o.p = "",
            o(o.s = 3)
    }([function (t, e, r) {
        "use strict";
        Object.defineProperty(e, "__esModule", {
            value: !0
        });
        var n = function () {
            function n(t, e) {
                for (var r = 0; r < e.length; r++) {
                    var n = e[r];
                    n.enumerable = n.enumerable || !1,
                        n.configurable = !0,
                    "value" in n && (n.writable = !0),
                        Object.defineProperty(t, n.key, n)
                }
            }

            return function (t, e, r) {
                return e && n(t.prototype, e),
                r && n(t, r),
                    t
            }
        }()
            , o = function () {
            function r() {
                !function (t, e) {
                    if (!(t instanceof r))
                        throw new TypeError("Cannot call a class as a function")
                }(this)
            }

            return n(r, null, [{
                key: "loop",
                value: function (t, r) {
                    "v".repeat(t).split("").map(function (t, e) {
                        return r(e)
                    })
                }
            }]),
                r
        }();
        e.default = o
    }
        , function (t, e, r) {
            "use strict";
            Object.defineProperty(e, "__esModule", {
                value: !0
            });
            var n = function () {
                function n(t, e) {
                    for (var r = 0; r < e.length; r++) {
                        var n = e[r];
                        n.enumerable = n.enumerable || !1,
                            n.configurable = !0,
                        "value" in n && (n.writable = !0),
                            Object.defineProperty(t, n.key, n)
                    }
                }

                return function (t, e, r) {
                    return e && n(t.prototype, e),
                    r && n(t, r),
                        t
                }
            }()
                , o = a(r(5))
                , u = a(r(0));

            function a(t) {
                return t && t.__esModule ? t : {
                    default: t
                }
            }

            function i(t, e) {
                if (!(t instanceof e))
                    throw new TypeError("Cannot call a class as a function")
            }

            var f = function () {
                function t() {
                    i(this, t),
                        this._char = ".",
                        this._children = {}
                }

                return n(t, [{
                    key: "getChar",
                    value: function () {
                        return this._char
                    }
                }, {
                    key: "getChildren",
                    value: function () {
                        return this._children
                    }
                }, {
                    key: "setChar",
                    value: function (t) {
                        this._char = t
                    }
                }, {
                    key: "setChildren",
                    value: function (t, e) {
                        this._children[t] = e
                    }
                }]),
                    t
            }()
                , s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
                , c = [1, 2, 2, 2, 2, 2]
                , l = function () {
                function e(t) {
                    i(this, e),
                        this._random = new o.default,
                        this._sign = "",
                        this._inter = {},
                        this._head = new f
                }

                return n(e, [{
                    key: "init",
                    value: function (t) {
                        var e = this;
                        this._random.seed(t),
                            this._sign = t,
                            u.default.loop(64, function (t) {
                                e._addSymbol("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"[t], c[parseInt((t + 1) / 11)])
                            }),
                            this._inter["="] = "="
                    }
                }, {
                    key: "_addSymbol",
                    value: function (t, e) {
                        var r = this
                            , n = this._head
                            , o = "";
                        return u.default.loop(e, function (t) {
                            for (var e = s[r._random.generate(32)]; e in n.getChildren() && "." !== n.getChildren()[e].getChar();)
                                e = s[r._random.generate(32)];
                            o += e,
                            e in n.getChildren() || n.setChildren(e, new f),
                                n = n.getChildren()[e]
                        }),
                            n.setChar(t),
                            this._inter[t] = o
                    }
                }, {
                    key: "decode",
                    value: function (t) {
                        for (var e = "", r = 4; r < t.length;)
                            if ("=" !== t[r]) {
                                for (var n = this._head; t[r] in n.getChildren();)
                                    n = n.getChildren()[t[r]],
                                        r++;
                                e += n.getChar()
                            } else
                                e += "=",
                                    r++;
                        return e
                    }
                }]),
                    e
            }();
            e.default = l
        }
        , function (module, exports, __webpack_require__) {
            var __WEBPACK_AMD_DEFINE_ARRAY__, __WEBPACK_AMD_DEFINE_RESULT__, ya, za;
            ya = "undefined" != typeof self ? self : "undefined" != typeof window ? window : "undefined" != typeof global ? global : this,
                za = function (global) {
                    "use strict";
                    global = global || {};
                    var _Base64 = global.Base64, version = "2.5.1", buffer;
                    if (void 0 !== module && module.exports)
                        try {
                            buffer = eval("require('buffer').Buffer")
                        } catch (t) {
                            buffer = void 0
                        }
                    var b64chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
                        , b64tab = function (t) {
                            for (var e = {}, r = 0, n = t.length; r < n; r++)
                                e[t.charAt(r)] = r;
                            return e
                        }(b64chars)
                        , fromCharCode = String.fromCharCode
                        , cb_utob = function (t) {
                            if (t.length < 2)
                                return (e = t.charCodeAt(0)) < 128 ? t : e < 2048 ? fromCharCode(192 | e >>> 6) + fromCharCode(128 | 63 & e) : fromCharCode(224 | e >>> 12 & 15) + fromCharCode(128 | e >>> 6 & 63) + fromCharCode(128 | 63 & e);
                            var e = 65536 + 1024 * (t.charCodeAt(0) - 55296) + (t.charCodeAt(1) - 56320);
                            return fromCharCode(240 | e >>> 18 & 7) + fromCharCode(128 | e >>> 12 & 63) + fromCharCode(128 | e >>> 6 & 63) + fromCharCode(128 | 63 & e)
                        }
                        , re_utob = /[\uD800-\uDBFF][\uDC00-\uDFFFF]|[^\x00-\x7F]/g
                        , utob = function (t) {
                            return t.replace(re_utob, cb_utob)
                        }
                        , cb_encode = function (t) {
                            var e = [0, 2, 1][t.length % 3]
                                ,
                                r = t.charCodeAt(0) << 16 | (1 < t.length ? t.charCodeAt(1) : 0) << 8 | (2 < t.length ? t.charCodeAt(2) : 0);
                            return [b64chars.charAt(r >>> 18), b64chars.charAt(r >>> 12 & 63), 2 <= e ? "=" : b64chars.charAt(r >>> 6 & 63), 1 <= e ? "=" : b64chars.charAt(63 & r)].join("")
                        }
                        , btoa = global.btoa ? function (t) {
                                return global.btoa(t)
                            }
                            : function (t) {
                                return t.replace(/[\s\S]{1,3}/g, cb_encode)
                            }
                        ,
                        _encode = buffer ? buffer.from && Uint8Array && buffer.from !== Uint8Array.from ? function (t) {
                                    return (t.constructor === buffer.constructor ? t : buffer.from(t)).toString("base64")
                                }
                                : function (t) {
                                    return (t.constructor === buffer.constructor ? t : new buffer(t)).toString("base64")
                                }
                            : function (t) {
                                return btoa(utob(t))
                            }
                        , encode = function (t, e) {
                            return e ? _encode(String(t)).replace(/[+\/]/g, function (t) {
                                return "+" == t ? "-" : "_"
                            }).replace(/=/g, "") : _encode(String(t))
                        }
                        , encodeURI = function (t) {
                            return encode(t, !0)
                        }
                        , re_btou = new RegExp(["[À-ß][-¿]", "[à-ï][-¿]{2}", "[ð-÷][-¿]{3}"].join("|"), "g")
                        , cb_btou = function (t) {
                            switch (t.length) {
                                case 4:
                                    var e = ((7 & t.charCodeAt(0)) << 18 | (63 & t.charCodeAt(1)) << 12 | (63 & t.charCodeAt(2)) << 6 | 63 & t.charCodeAt(3)) - 65536;
                                    return fromCharCode(55296 + (e >>> 10)) + fromCharCode(56320 + (1023 & e));
                                case 3:
                                    return fromCharCode((15 & t.charCodeAt(0)) << 12 | (63 & t.charCodeAt(1)) << 6 | 63 & t.charCodeAt(2));
                                default:
                                    return fromCharCode((31 & t.charCodeAt(0)) << 6 | 63 & t.charCodeAt(1))
                            }
                        }
                        , btou = function (t) {
                            return t.replace(re_btou, cb_btou)
                        }
                        , cb_decode = function (t) {
                            var e = t.length
                                , r = e % 4
                                ,
                                n = (0 < e ? b64tab[t.charAt(0)] << 18 : 0) | (1 < e ? b64tab[t.charAt(1)] << 12 : 0) | (2 < e ? b64tab[t.charAt(2)] << 6 : 0) | (3 < e ? b64tab[t.charAt(3)] : 0)
                                , o = [fromCharCode(n >>> 16), fromCharCode(n >>> 8 & 255), fromCharCode(255 & n)];
                            return o.length -= [0, 0, 2, 1][r],
                                o.join("")
                        }
                        , _atob = global.atob ? function (t) {
                                return global.atob(t)
                            }
                            : function (t) {
                                return t.replace(/\S{1,4}/g, cb_decode)
                            }
                        , atob = function (t) {
                            return _atob(String(t).replace(/[^A-Za-z0-9\+\/]/g, ""))
                        }
                        ,
                        _decode = buffer ? buffer.from && Uint8Array && buffer.from !== Uint8Array.from ? function (t) {
                                    return (t.constructor === buffer.constructor ? t : buffer.from(t, "base64")).toString()
                                }
                                : function (t) {
                                    return (t.constructor === buffer.constructor ? t : new buffer(t, "base64")).toString()
                                }
                            : function (t) {
                                return btou(_atob(t))
                            }
                        , decode = function (t) {
                            return _decode(String(t).replace(/[-_]/g, function (t) {
                                return "-" == t ? "+" : "/"
                            }).replace(/[^A-Za-z0-9\+\/]/g, ""))
                        }
                        , noConflict = function () {
                            var t = global.Base64;
                            return global.Base64 = _Base64,
                                t
                        };
                    if (global.Base64 = {
                        VERSION: version,
                        atob: atob,
                        btoa: btoa,
                        fromBase64: decode,
                        toBase64: encode,
                        utob: utob,
                        encode: encode,
                        encodeURI: encodeURI,
                        btou: btou,
                        decode: decode,
                        noConflict: noConflict,
                        __buffer__: buffer
                    },
                    "function" == typeof Object.defineProperty) {
                        var noEnum = function (t) {
                            return {
                                value: t,
                                enumerable: !1,
                                writable: !0,
                                configurable: !0
                            }
                        };
                        global.Base64.extendString = function () {
                            Object.defineProperty(String.prototype, "fromBase64", noEnum(function () {
                                return decode(this)
                            })),
                                Object.defineProperty(String.prototype, "toBase64", noEnum(function (t) {
                                    return encode(this, t)
                                })),
                                Object.defineProperty(String.prototype, "toBase64URI", noEnum(function () {
                                    return encode(this, !0)
                                }))
                        }
                    }
                    return global.Meteor && (Base64 = global.Base64),
                        void 0 !== module && module.exports ? module.exports.Base64 = global.Base64 : (__WEBPACK_AMD_DEFINE_ARRAY__ = [],
                            __WEBPACK_AMD_DEFINE_RESULT__ = function () {
                                return global.Base64
                            }
                                .apply(exports, __WEBPACK_AMD_DEFINE_ARRAY__),
                        void 0 === __WEBPACK_AMD_DEFINE_RESULT__ || (module.exports = __WEBPACK_AMD_DEFINE_RESULT__)),
                        {
                            Base64: global.Base64
                        }
                }
                ,
                module.exports = za(ya)
        }
        , function (t, e, r) {
            "use strict";
            Object.defineProperty(e, "__esModule", {
                value: !0
            });
            var n, o = function () {
                function n(t, e) {
                    for (var r = 0; r < e.length; r++) {
                        var n = e[r];
                        n.enumerable = n.enumerable || !1,
                            n.configurable = !0,
                        "value" in n && (n.writable = !0),
                            Object.defineProperty(t, n.key, n)
                    }
                }

                return function (t, e, r) {
                    return e && n(t.prototype, e),
                    r && n(t, r),
                        t
                }
            }(), u = r(2), a = (n = r(1)) && n.__esModule ? n : {
                default: n
            }, i = function (t) {
                var e = t.charCodeAt();
                return 65 <= e ? e - 65 : e - 65 + 41
            }, f = function () {
                function r() {
                    !function (t, e) {
                        if (!(t instanceof r))
                            throw new TypeError("Cannot call a class as a function")
                    }(this)
                }

                return o(r, null, [{
                    key: "_checkVersion",
                    value: function (t) {
                        return ((32 * i(t[0]) + i(t[1])) * i(t[2]) + i(t[3])) % 32 <= 1
                    }
                }, {
                    key: "d",
                    value: function (t) {
                        if (!this._checkVersion(t))
                            return "";
                        var e = new a.default;
                        e.init(t.substr(0, 4));
                        var r = e.decode(t);
                        return u.Base64.decode(r)
                    }
                }]),
                    r
            }();
            e.default = f,
                t.exports = f
        }
        , function (t, e, r) {
            "use strict";
            Object.defineProperty(e, "__esModule", {
                value: !0
            });
            var n = function () {
                function n(t, e) {
                    for (var r = 0; r < e.length; r++) {
                        var n = e[r];
                        n.enumerable = n.enumerable || !1,
                            n.configurable = !0,
                        "value" in n && (n.writable = !0),
                            Object.defineProperty(t, n.key, n)
                    }
                }

                return function (t, e, r) {
                    return e && n(t.prototype, e),
                    r && n(t, r),
                        t
                }
            }()
                , o = function () {
                function r() {
                    !function (t, e) {
                        if (!(t instanceof r))
                            throw new TypeError("Cannot call a class as a function")
                    }(this)
                }

                return n(r, null, [{
                    key: "get",
                    value: function (t) {
                        return t >>> 0
                    }
                }, {
                    key: "xor",
                    value: function (t, e) {
                        return this.get(this.get(t) ^ this.get(e))
                    }
                }, {
                    key: "and",
                    value: function (t, e) {
                        return this.get(this.get(t) & this.get(e))
                    }
                }, {
                    key: "mul",
                    value: function (t, e) {
                        var r = ((4294901760 & t) >>> 0) * e
                            , n = (65535 & t) * e;
                        return this.get((r >>> 0) + (n >>> 0))
                    }
                }, {
                    key: "or",
                    value: function (t, e) {
                        return this.get(this.get(t) | this.get(e))
                    }
                }, {
                    key: "not",
                    value: function (t) {
                        return this.get(~this.get(t))
                    }
                }, {
                    key: "shiftLeft",
                    value: function (t, e) {
                        return this.get(this.get(t) << e)
                    }
                }, {
                    key: "shiftRight",
                    value: function (t, e) {
                        return this.get(t) >>> e
                    }
                }, {
                    key: "mod",
                    value: function (t, e) {
                        return this.get(this.get(t) % e)
                    }
                }]),
                    r
            }();
            e.default = o
        }
        , function (t, e, r) {
            "use strict";
            Object.defineProperty(e, "__esModule", {
                value: !0
            });
            var n = function () {
                function n(t, e) {
                    for (var r = 0; r < e.length; r++) {
                        var n = e[r];
                        n.enumerable = n.enumerable || !1,
                            n.configurable = !0,
                        "value" in n && (n.writable = !0),
                            Object.defineProperty(t, n.key, n)
                    }
                }

                return function (t, e, r) {
                    return e && n(t.prototype, e),
                    r && n(t, r),
                        t
                }
            }()
                , o = a(r(0))
                , u = a(r(4));

            function a(t) {
                return t && t.__esModule ? t : {
                    default: t
                }
            }

            var i = function () {
                function r() {
                    !function (t, e) {
                        if (!(t instanceof r))
                            throw new TypeError("Cannot call a class as a function")
                    }(this),
                        this._status = [],
                        this._mat1 = 0,
                        this._mat2 = 0,
                        this._tmat = 0
                }

                return n(r, [{
                    key: "seed",
                    value: function (e) {
                        var r = this;
                        o.default.loop(4, function (t) {
                            e.length > t ? r._status[t] = u.default.get(e.charAt(t).charCodeAt()) : r._status[t] = u.default.get(110)
                        }),
                            this._mat1 = this._status[1],
                            this._mat2 = this._status[2],
                            this._tmat = this._status[3],
                            this._init()
                    }
                }, {
                    key: "_init",
                    value: function () {
                        var e = this;
                        o.default.loop(7, function (t) {
                            e._status[t + 1 & 3] = u.default.xor(e._status[t + 1 & 3], t + 1 + u.default.mul(1812433253, u.default.xor(e._status[3 & t], u.default.shiftRight(e._status[3 & t], 30))))
                        }),
                        0 == (2147483647 & this._status[0]) && 0 === this._status[1] && 0 === this._status[2] && 0 === this._status[3] && (this._status[0] = 66,
                            this._status[1] = 65,
                            this._status[2] = 89,
                            this._status[3] = 83),
                            o.default.loop(8, function () {
                                return e._next_state()
                            })
                    }
                }, {
                    key: "_next_state",
                    value: function () {
                        var t = void 0
                            , e = void 0;
                        e = this._status[3],
                            t = u.default.xor(u.default.and(this._status[0], 2147483647), u.default.xor(this._status[1], this._status[2])),
                            t = u.default.xor(t, u.default.shiftLeft(t, 1)),
                            e = u.default.xor(e, u.default.xor(u.default.shiftRight(e, 1), t)),
                            this._status[0] = this._status[1],
                            this._status[1] = this._status[2],
                            this._status[2] = u.default.xor(t, u.default.shiftLeft(e, 10)),
                            this._status[3] = e,
                            this._status[1] = u.default.xor(this._status[1], u.default.and(-u.default.and(e, 1), this._mat1)),
                            this._status[2] = u.default.xor(this._status[2], u.default.and(-u.default.and(e, 1), this._mat2))
                    }
                }, {
                    key: "generate",
                    value: function (t) {
                        this._next_state();
                        var e, r = void 0;
                        return r = this._status[3],
                            e = u.default.xor(this._status[0], u.default.shiftRight(this._status[2], 8)),
                            r = u.default.xor(r, e),
                        (r = u.default.xor(u.default.and(-u.default.and(e, 1), this._tmat), r)) % t
                    }
                }]),
                    r
            }();
            e.default = i
        }
    ])
})


var t = "4XHALP73T2NMOHPAAJDXTC6VFYZT6VW6WXMDFI4XTWG73FYZTD3FHBW7NNFFHZ4QLV5BTV5FFFYZTDJW6SY2NFIW6BW7NFF4XT2NFHLP73T2OFH2ON4NFW6FIUDBWMARE7NWGREBWN4FIFHVHN4FIMO734QLLP73TXTFH2O6UD6VJWXVGD34XTWGAA4AA6VAAW6BWTFIW6RE7NFIVJYUDNFMDZ4QL4XT46VV5BTB3D6V5ICD6V5BT5MVV5BT7KQLV5I7KQLN4BT7KUSV5IP6VV5IP6VDQFFP6VJDXTP6V4AA6VAAMAWX7KAAJDAATXTMDSY7W7CMOZ4NX4VHTFIVJFIUD2NVJZ4QL4SYYNFW6WXYNF4AA6VAAMO2OUD6UFHSY7KAAJDVHNXAAW6RE7WBUMAWXUD6GMDWXD66GFHSYYD6VJ7F4QL4XT4L6V5FFMO2LN4IBU2OW6XTMVL6VJSYYNFV5FFBUD3N4IB373VJBTMVL6VJEYXTN4ITXTVJIW6BW4AA6VAAW6RE7WBUMAWXUD6GMDWXD66GMDRETNXMO734QLWX73TWGMDH7N6VMOFFWGDJFY2O6UFIVJEFINFFYWXY6UVJEFIDJV57FVGAAW6REFIBUFHAAVGXTFH2OD3DJW6WXTXTREBW56UW6FIUDNFMDWX7N2NFH73KTFFVJWXW66UW6BTN4BUN4IBUVGV5BTMDBUN4WXVJBUN4BT7NAAN4XTV5VGW6BTB3VGN4BT7K6VN4ITXTV5AAVGFIVJEV56UJDBTNFAAV5WXN4FIW6WXV5VGV5XTN4SYJDBT7KFFV5FFCFFN4IP73VJBTV5BWVJI7WNFN473VGD6MOIV5AAFYZTWGMDH7N6VMOFFWGDJFY2O6UFIVJEFINFFYWXY6UVJEFIDJV57FVGAAW6REFIBUFHAAVGXTFH2OD3DJW6WXTXTREBW56UW6FIUDNFMDWX7N2NFH73KTFFVJWXW66UW6BTN4BUN4IBUVGV5BTMDBUN4WXVJBUN4BT7NAAN4XTV5VGW6BTB3VGN4BT7K6VN4ITXTV5AAVGFIVJEV56UJDBTNFAAV5WXN4FIW6WXV5VGV5XTN4SYJDBT7KFFV5FFCFFN4IP73VJBTV5BWVJI7WNFN473VGD6MOIV5AARE7F6VAAW6RE7WBUMAWXUD6GMDREN46GFHSYYD6VJ7F4QL4SYCBWVJBTW6FFV52OMV73JDI7WSYJDIV52LV5IV56VV5E7NFIJDBTBU2OV5EN4FIV5SY4D3V5FFW6D34AA6VAAW6RE7WBUMAWXUD6GMDREN46GMDRETNXMO734QLWX73TWGMDH7N6VMOFFWGDJFY2O6UFIVJEFINFFYWXY6UVJEFIDJV57FVGAAW6REFIBUFHAAVGXTFH2OD3DJW6WXTXTREBW56UW6FIUDNFMDWX7N2NFH73KTBWV5SY7KD3VJBTMO6UN4XTW6BWVJXTMV2LN4E473V5FFMDXTJDEN4XTJDEYFIW62OYFIW62OYAAVJ7FL62LN4IFIFIV52OVJNFV5BTVJFIW6SY7K2ON4ITNFW62OW6FFV5FFVJFIV5I5SYN4EV52LJDIMO2LVJAAVGD6MOIV5AAFYZTWGMDH7N6VMOFFWGDJFY2O6UFIVJEFINFFYWXY6UVJEFIDJV57FVGAAW6REFIBUFHAAVGXTFH2OD3DJW6WXTXTREBW56UW6FIUDNFMDWX7N2NFH73KTBWV5SY7KD3VJBTMO6UN4XTW6BWVJXTMV2LN4E473V5FFMDXTJDEN4XTJDEYFIW62OYFIW62OYAAVJ7FL62LN4IFIFIV52OVJNFV5BTVJFIW6SY7K2ON4ITNFW62OW6FFV5FFVJFIV5I5SYN4EV52LJDIMO2LVJAAVGD6MOIV5AARE7F6VAAMARE5NFREBW7WGB4XTWGAA4AA6VAAMARE5NFREBW7WFF4XTWGAA4VHD3NX4VHN4D3W6RE7N6UMO734QLV5Z6VAAMDRE5BUW6RE7NFIVJYUDNFMDZ4QL4XT46VV5XTPD6V5IV5D6V5I7WMVV5IMVQLV5IBUQLV5XTW6USV5IP6VV5IP6VDQFFP6VJDXTP6V4AA6VAAMDSYUDXTW6WXT6GMDHFI6VVJ7F4QLV5736VAAMD2OUD73VJZ4QL4SYMDDJFH2O7KB3W6WXVJD3VJRETUSFH2OUDUS4AA6VAAMO2O7WUSMO2O7WFF4XT2NFHLP73TXTMOSY7WNFMDE7WBURE2OYD34XTWGAAV5XTP2LJDZD36VV573D373V5Y7K6VJDIWG6VN4FFWG6UV5AAL66UV5BTW6BWN4I7KGBV5IPQLV5IPAAFYZTBUVJWXVJ2NFHSYFID3MAWXUDUSRE2ON4US4XTWGAAU4U4734VGFYAAFYVGW62O4QLDQLP5QLVJ2OAAVG2NLP2OVGVG7FWGQLDQDDD6U4U473TVGFYAAFYVGW62O4VGMAWXUD4AA6VAAVJE7WSYMAWXVG2NMDEFIDJFHFIUDFIFHAA4QL4AA4NX4SY7N2NW6BW7N2NFH2OVGNFMOVHFI6GMAWX7KAAJDAATFIVJREFI2OMD7F4NX4SY7WL6MDYUDFILPEYD6MOE2LFIRE2OFIBUMO734QLFHVH7WNXFHZ6VAAMAWX7KAAJDAATAAMOBW7N6UMO2O6VAAFYZT6VFHBWV5AAJDAAT2NFHVH7KUS4AA6VAAMO2O7W2LMDWX7WUSW62OMVAAJDXTW6BWN4XT42LFYZTFFFHBW7WUSVJZ4QLLP73TNFMDWX7N2NFH6UUDBUVJWXVJ6GW62OVG6GFHSYYD6VJ7F4QL4SYYAAW66UUD6VMDWXT6GW6RE7WBUMAWXKTDJN4EN4BUV5IBU6VW6BTNFXTN4IYXTV5FFPL6N4IB3FFN4IV573V5WXV52LVJWXC2OJDI7K73N4XTMOUSN4EN4BUV5IBU6VW6BTNFXTN4IYXTV5FFPL6N4IB3FFN4IV573V5WXV52LVJWXC2OJDI7K73N4XTMOUSW6WXYXT4AA6VAAW6RE7WBUMAWXUD6GVJE7WSYRE2ON4USREBW7W73FHZ4QL4SYNFD3MDH5FFJDAAKTDJFHWX7WBUMAWXCD6W6RE7WBUMAWXKT2LFYSYTNFLPWX7NUSFYSYN4DJFH7FUDNFW6SYN46GMOH7WAARE2OY6UVJEFIDJFYFF7NXTVJIPVGV5ECL6W6FF7K2LW6FFV56VJDI7KL6V5FF7KFFV5XTYXTV5WX7WNFN4XTB3D3V5XTW6BWFYXT7NXTVJIPVGV5ECL6W6FF7K2LW6FFV56VJDI7KL6V5FF7KFFV5XTYXTV5WX7WNFN4XTB3D3V5XTW6BWFYSYYNFW6734NX4SYY6UVJEFIDJREBW7WGBRE2OVGNFFHWXMVAAJDAA4AAFYZTNFMDWX7N2NFH6UUD6UMA6UUD6UMOSY2LFF4XT2NFHRE7F6VAAW6RE7WBUMAWXUD6GMDREN46GFHSYYD6VJ7F4QL4AA4NX4SYY6UVJEFIDJREBW7WFFREBW7W73FHHV5AAJDFID6MDFYZT2NMOEY6GMDWXNXAAJDAA4AAFYZT2NMOEY6GMDREV5AAJDAA4AA6G7F6VAAMDRE5BUW6RE7NFIVJYUDNFMDZ4QL4XT46VV5XTPD6V5IBUD6V5BT7NMVV5BTCQLV5BTBUQLV5I7KUSJDIMOBWV5FFMVFFDQFFP6VJDXTP6V4AA6VAAMDSYUDXTW6WXT6UFHEY73LP7WUD2NVJZ4QL4SYN42OVJWX2N6V4VH6UMDFYZT2OFH2ON4NFW6VH7WNXW6RETVGRE2OFIBU4XTWGAAW6BWVJFIMAVHPAA6GRED3NXLP73T2OFH2ON4NFW6FIUDBWMARE7NWGREBWN4FIFHVHN4FIMO734QLLP73TXTFH2O6UD6VJWXVGD34XTWGAA4AA6VAAW6BWTFIW6RE7NFIVJYUDNFMDZ4QL4XT46VV5BTB3D6V5ICD6V5BT5MVV5BT7KQLV5I7KQLN4BT7KUSV5IP6VV5IP6VDQFFP6VJDXTP6V4AA6VAAMAWX7KAAJDAATAAMDEN46UVJE6VAAFYZT73VJWXVJ6GMAWX7KAAJDAATNFW6WXYNFW67F4NX4VHN4DJMDWXVGBU4XT2NU44SYY6UVJEFIDJREBW7WGBRE2OVGNFFHWXMVAAJDAA4D3W6XTMO2OV5FFV5D3N4WX4BWJDEVJBUVJXTV573N4E7KBWV52OV56VV5IBU73W6SY7K73JDEVJXTW6734NX4SYY6UVJEFIDJREBW7WGBREBW7W73FHHV5AAJDFINXAAMAH7ND3MOHV5QLFY73UDD6VJWX7N2NW67F6UNFMDWX7N2NFHFFCUSW6SYYVGVJEL6USW62OUDD6FY2OYAAW66UUD6VMDWXT6GW6RE7WBUMAWXKTDJV5BTMVFFVJIV573N4EMV6VN4XT46VV5XT5NFW62ON4NFV5BTMOBWW6XT7NBUVJXT42OW6SY7KD3VJIPUSVJWXV5BWV5FFYXTV5BT7NFIJDWXV5VGV5WXVJAAW6XTCL6W6BT5AAN4BT7WNFN4SYMVFFV5BT7KL6JDICUSFHREPFF4AA6VAAMAH7ND3MOHV5QLFY73UDD6VJWX7N2NW67F6UNFMDWX7N2NFHFFCUSW6SYYVGVJEL6USW62OUDD6FY2OYAAW66UUD6VMDWXT6GW6RE7WBUMAWXKTDJV5BTMVFFVJIV573N4EMV6VN4XT46VV5XT5NFW62ON4NFV5BTMOBWW6XT7NBUVJXT42OW6SY7KD3VJIPUSVJWXV5BWV5FFYXTV5BT7NFIJDWXV5VGV5WXVJAAW6XTCL6W6BT5AAN4BT7WNFN4SYMVFFV5BT7KL6JDICUSFHREPFF4FID3NX4SYY6UVJEFIDJREBW7WFFRE2OVGNFFHWXMVAAJDAATBUV52OV5VGVJWX7WBUV5ITAAJDBTB3D3W6XTNFSYVJINFNFVJWXVJSYV5EW62ON4XTYSYVJECL6N4Z4NX4SYY6UVJEFIDJREBW7WFFREBW7W73FHHV5AAJDFINXAAMAH7ND3MOHV5QLFY73UDD6VJWX7N2NW67F6UNFMDWX7N2NFHFFCUSW6SYYVGVJEL6USW62OUDD6FY2OYAAW66UUD6VMDWXT6GW6RE7WBUMAWXKTDJN4SY7KBWW6XT7KD3N4IYXTV5E7WAAN4E7NBUVJBT5XTN4E7K2LVJBTBU2OVJI7WFIN4BTP6VV5I7KUSW6FFMO2LN4I7K6VV52O7NSYV5XT7KL6N4XTTNFW6WX7WFIN4IW6FFV52OV56VVJIB3BWVJXT7WNFN4FF7KUSFHREPFF4AA6VAAMAH7ND3MOHV5QLFY73UDD6VJWX7N2NW67F6UNFMDWX7N2NFHFFCUSW6SYYVGVJEL6USW62OUDD6FY2OYAAW66UUD6VMDWXT6GW6RE7WBUMAWXKTDJN4SY7KBWW6XT7KD3N4IYXTV5E7WAAN4E7NBUVJBT5XTN4E7K2LVJBTBU2OVJI7WFIN4BTP6VV5I7KUSW6FFMO2LN4I7K6VV52O7NSYV5XT7KL6N4XTTNFW6WX7WFIN4IW6FFV52OV56VVJIB3BWVJXT7WNFN4FF7KUSFHREPFF4FID3NX4SYFI6VW67WUD6UMA734QL4SYD6NX73VJHFYBUHV5AAFYZT2NMOEY6GMDREV5AAJDAATGBFHV5JDSYMO73TUDFYZTFFMDEYD3MDREV5AAJDXTPNX4VH7W6VVJEYD3VJWX7N6GW6RE7KAAJDAA473V5I46VFYBTPFFFYBTP6U7WIPD3JDXT7KD3JDXTV52LFYXTP6VV5IP6VV5ZNX6VV5IWG6VV5Z4NX4VHVJDJW62OYAAREBW7NVGMOEMVAAJDXTPNX4VHMDDJMOSY7KAAJDAATXTFHEYFFMO734NX4VHN4FIFHVHN4FIMO734QLWXBWNXAAW6BWTFIW6RE7NFIVJYUDNFMDZ4QL4XT46VV5BTBUD6V5ICD6V5XTYMVV5BTPQLN4I4QLV5FFB3USV5IC2ON4FFMVFFDQFFP6VJDXTP6V4AA6VAAVJE7WSYMAWXVG2NMDEFIDJFHFIUDXTFHAA4QL4USAADJDJUSDDKTSYDDDDKTAAJDWXD62NUSMAB3WGLPSYHXTJDLPMANFJDDDKTAALPLP6FGBLPDDKTSYDDSYW6D6USLPQL2NDDDDKTXTJDSYW6D6USWX2LB3AA4NX4SY7NFIVJSYFIUSMARE7N2NFH2OVG6GVJWXL6AAJDAA4AAFYZTBUMAWXN4D3MAWXUDUSW6RETVGRE2OFIBU4XTWGAAMASYD67CMOEBUAAFYZTFILPH7N6GVJRENFNFFHRE5NXVJ7WUD2NVJHV5AAJDSYVG6UFHE6VNX4SYFIBU4XTWGAAFHEFI6VVJVHB3AAFYZT6VFHBWV5AAJDAATUSFYAA4NX4VHN4FIMORE7WFIFHSYN4FI4XTWG6UV5FF7KFFN4FFBUD3FYZTFFFHBW7WUSVJZ4QLLP73TNFMDWX7N2NFH6UUDBUVJWXVJ6GW62OVG6GFHSYYD6VJ7F4QL4SYYAAW66UUD6VMDWXT6GW6RE7WBUMAWXKTDJV5IW6D3N4ICFFVJE7NFIN4XT7WAAN4XTB3BWV5IYAAW62OTSYW6XTVJNFV5FF4L6V5XT7K6UVJXTMOUSV5IW6D3N4ICFFVJE7NFIN4XT7WAAN4XTB3BWV5IYAAW62OTSYW6XTVJNFV5FF4L6V5XT7K6UVJXTMOUSW6WXYXT4AA6VAAW6RE7WBUMAWXUD6GVJE7WSYRE2ON4USREBW7W73FHZ4QL4SYNFD3MDH5FFJDAAKTDJFHWX7WBUMAWXCD6W6RE7WBUMAWXKT2LFYSYTNFLPWX7NUSFYSYN4DJFH7FUDNFW6SYN46GMOH7WAARE2OY6UVJEFIDJFYFFP2ON4I7K2LV52O7NBUVJBTW66UW6XTW6L6N4FFP2LW6SYN4AAVJSY42OW6BTV573JDI4D3N4WXW6BWFYXTP2ON4I7K2LV52O7NBUVJBTW66UW6XTW6L6N4FFP2LW6SYN4AAVJSY42OW6BTV573JDI4D3N4WXW6BWFYSYYNFW6734NX4SYY6UVJEFIDJREBW7WGBRE2OVGNFFHWXMVAAJDAA4AAFYZTNFMDWX7N2NFH6UUD6UMA6UUD6UMOSY2LFF4XT2NFHRE7F6VAAW6RE7WBUMAWXUD6GMDREN46GFHSYYD6VJ7F4QL4AA4NX4SYY6UVJEFIDJREBW7WFFREBW7W73FHHV5AAJDFID6MDFYZT2NMOEY6GMDWXNXAAJDAA4AAFYZT2NMOEY6GMDREV5AAJDAA4AA6G7F6VAAMDRE5BUW6RE7NFIVJYUDNFMDZ4QL4XT46VV5XTPD6V5IBUD6V5BT7NMVV5IB3QLV5FFBUQLN4IPUSN4FFBU6VN4BTC2LDQFFP6VJDXTP6V4AA6VAAMDSYUDXTW6WXT6UFHEY73LP7WUD2NVJZ4QL4SYTD3W6BW7WBUFHZTUDRE7F6VAAMDSYUDXTW6WXT6UFHEY73LP7WUD2NVJZ4QL4SYTD3W6BW7WBUFHZTUD6G7F2LU44VHVJDJW62OYAAREBWMD2NMDENF6GMO2O7WUSMO2O7WFF4XT2NU44SYN4DJFHWX6UFIFHVH7KAAJDAA4AAFYZTXTMOSY7WNFMDE7WBURE2OYD34XTWGAAV5XTP2LJDZD36VV57FD32LV5Y7K2LN4IWG6VN4IWG6UN4ZL66VV5IP6VV5IPGBV5IPQLV5IPAAFYZT2NVJZ4QL4VHYNXMDET2L4AA6VAAMOSY7WSYRE2OFIBU4XTWGAAW6WXYNFW6WXCAAFYZTFFFHBW7WUSVJZ4QLLP73TNFMDWX7N2NFH6UUD6UMA6UUDUSW6WX6UFI4XTWGAAN4XTMOL6N4XTMO6UV5BTTAAN4FFBU6VN4FFYFIN4I7NNFJDIP73N4EN4AAW6XTTXTW6BT473N4SYV5AAFYZTNFMDWX7N2NFH6UUD6UMA6UUD6UMOSY2LFF4XT2NFH4SYNFD3MDH5FFJDAAKTDJFHWX7WBUMAWXCD6W6RE7WBUMAWXKT2LFYSYTNFLPWX7NUSFYSYN4DJFH7FUDNFW6SYN46GMOH7WAARE2OY6UVJEFIDJFYFFNFXTN4SY7KBWV5FF7NFIW62OTFIN4BTYAAJDBTYAAW6XTMV73V5BTMDAAV5E46UN4SYV5D3N4BTMOL6FYXT7NFIN42O4FFW6WX7WAAN4WX7NAAN42OC6UVJWXW6BWJDIW6FFN4FFPVGJDWXC2ON4WX42LW6FFB3FFFYSY6U6VV5734NX4SYNFD3MDH5FFJDAAKTDJFHWX7WBUMAWXCD6W6RE7WBUMAWXKT2LFYSYTNFLPWX7NUSFYSYN4DJFH7FUDNFW6SYN46GMOH7WAARE2OY6UVJEFIDJFYFFNFXTN4SY7KBWV5FF7NFIW62OTFIN4BTYAAJDBTYAAW6XTMV73V5BTMDAAV5E46UN4SYV5D3N4BTMOL6FYXT7NFIN42O4FFW6WX7WAAN4WX7NAAN42OC6UVJWXW6BWJDIW6FFN4FFPVGJDWXC2ON4WX42LW6FFB3FFFYSY6U6VV573TMDFYZTNFMDWX7N2NFH6UUD6UMO6UUDUSW6WX6UFI4XTWGAAN42OC2LV5XTV5FFW62OC2LN4BTTAAVJXTMDXTVJSYN4XTV5IP73N42OYNFJDIFINFN4IMDSYVJIMOAAFYZTNFMDWX7N2NFH6UUD6UMO6UUD6UMOSY2LFF4XT2NFH4SYNFD3MDH5FFJDAAKTDJFHWX7WBUMAWXCD6W6RE7WBUMAWXKT2LFYSYTNFLPWX7NUSFYSYN4DJFH7FUDNFW6SYN46GMOH7WAARE2OY6UVJEFIDJFYFFCFFV52O7KFFN4SY7WAAV5IBU6UJDBT5SYVJXTN4AAW6FFTXTN4XTV52OV5ICD3N42OYNFVJXTTFIFYSY473JDBTMDXTW6WXW6VGN4FFP6VJDI42LV5XTPL6W6XTN4XTV5FFBUBWN4I7KFFV52O7K6UN4BTPVGFYSY6U6VV5734NX4SYNFD3MDH5FFJDAAKTDJFHWX7WBUMAWXCD6W6RE7WBUMAWXKT2LFYSYTNFLPWX7NUSFYSYN4DJFH7FUDNFW6SYN46GMOH7WAARE2OY6UVJEFIDJFYFFCFFV52O7KFFN4SY7WAAV5IBU6UJDBT5SYVJXTN4AAW6FFTXTN4XTV52OV5ICD3N42OYNFVJXTTFIFYSY473JDBTMDXTW6WXW6VGN4FFP6VJDI42LV5XTPL6W6XTN4XTV5FFBUBWN4I7KFFV52O7K6UN4BTPVGFYSY6U6VV573TMDFYZT2NMOEY6GMDWXNXAAJDAAFYFYXTV5SYNF73WG2NBUT2OTNF73MAWGAAFYZT2NMOEY6GMDREV5AAJDAAFYFYXTV5SYNF73WG2NBUT2OTNF73MAWGAA6G7F6VAAMOBW7NNFMDH7WFF4XTWG6VFYZT6UMOE7NNFMDE7WBURE2OYD34XTWGAAV5XTP73V5ZD36VV573D36VN47W7K6VN4IWG6UN4XTWGD3V573L66VV5IP6VV5IPGBV5IPQLV5IPAAFYZT2OFH2ON4NFW6FIUDD3LPRE5FI4XTWG6VFYZTBWFHBWTBU4XTWGAAVJ2OUDDJVJETVGVJ7F4NX4VHN4FIFHVHN4FIMO734QLWXBWNXAAW6BWTFIW6RE7NFIVJYUDNFMDZ4QL4XT46VV5BTBUD6V5I4D6V5XTNFMVV5IV5QLV5FFBUQLN4IB3USV5FFMO6UN4BTW62ODQFFP6VJDXTP6V4AA6VAAVJE7WSYMAWXVG2NMDEFIDJFHFIUDXTFHAA4QL4USWXEXTLPAAVHB37F4NX4SY7NFIVJSYFIUSMARE7N2NFH2OVG6GVJWXL6AAJDAA4AAFYZTBUMAWXN4D3MAWXUDUSW6"

function f(t) {
    return window.d(3).d(t)
}