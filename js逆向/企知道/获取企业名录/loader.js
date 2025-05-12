window = global
userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'

timeStamp = window.performance.now()

addEventListener = function (a, e) {

}

location = {
    pathname: '/',
    replace(url) {

    },
    origin: {
        includes(searchString, position) {

        }
    }
}

document = {}

document.querySelector = function (e) {

}
document.createElement = function (e) {

}
document.createComment = function (e) {

}

console.log(timeStamp)

require('./mod2')

require('./mod1')

!function (e) {
    function t(t) {
        for (var a, r, s = t[0], c = t[1], u = t[2], d = 0, f = []; d < s.length; d++)
            r = s[d],
            Object.prototype.hasOwnProperty.call(o, r) && o[r] && f.push(o[r][0]),
                o[r] = 0;
        for (a in c)
            Object.prototype.hasOwnProperty.call(c, a) && (e[a] = c[a]);
        for (l && l(t); f.length;)
            f.shift()();
        return i.push.apply(i, u || []),
            n()
    }

    function n() {
        for (var e, t = 0; t < i.length; t++) {
            for (var n = i[t], a = !0, r = 1; r < n.length; r++) {
                var c = n[r];
                0 !== o[c] && (a = !1)
            }
            a && (i.splice(t--, 1),
                e = s(s.s = n[0]))
        }
        return e
    }

    var a = {}
        , r = {
        "app~d0ae3f07": 0
    }
        , o = {
        "app~d0ae3f07": 0
    }
        , i = [];

    function s(t) {
        if (a[t])
            return a[t].exports;
        var n = a[t] = {
            i: t,
            l: !1,
            exports: {}
        };
        console.log("::::", n)
        return e[t].call(n.exports, n, n.exports, s),
            n.l = !0,
            n.exports
    }

    window.loader = s
    s.e = function (e) {
        var t = [];
        r[e] ? t.push(r[e]) : 0 !== r[e] && {
            "about~31ecd969": 1
        }[e] && t.push(r[e] = new Promise((function (t, n) {
                for (var a = "static/css/" + ({
                    "about~31ecd969": "about~31ecd969"
                }[e] || e) + "." + {
                    "about~31ecd969": "b8537b22"
                }[e] + ".css", o = s.p + a, i = document.getElementsByTagName("link"), c = 0; c < i.length; c++) {
                    var u = i[c]
                        , d = u.getAttribute("data-href") || u.getAttribute("href");
                    if ("stylesheet" === u.rel && (d === a || d === o))
                        return t()
                }
                var l = document.getElementsByTagName("style");
                for (c = 0; c < l.length; c++)
                    if ((d = (u = l[c]).getAttribute("data-href")) === a || d === o)
                        return t();
                var f = document.createElement("link");
                f.rel = "stylesheet",
                    f.type = "text/css",
                    f.onload = t,
                    f.onerror = function (t) {
                        var a = t && t.target && t.target.src || o
                            , i = new Error("Loading CSS chunk " + e + " failed.\n(" + a + ")");
                        i.code = "CSS_CHUNK_LOAD_FAILED",
                            i.request = a,
                            delete r[e],
                            f.parentNode.removeChild(f),
                            n(i)
                    }
                    ,
                    f.href = o,
                    document.getElementsByTagName("head")[0].appendChild(f)
            }
        )).then((function () {
                r[e] = 0
            }
        )));
        var n = o[e];
        if (0 !== n)
            if (n)
                t.push(n[2]);
            else {
                var a = new Promise((function (t, a) {
                        n = o[e] = [t, a]
                    }
                ));
                t.push(n[2] = a);
                var i, c = document.createElement("script");
                c.charset = "utf-8",
                    c.timeout = 120,
                s.nc && c.setAttribute("nonce", s.nc),
                    c.src = function (e) {
                        return s.p + "static/js/" + ({
                            "about~31ecd969": "about~31ecd969"
                        }[e] || e) + "." + {
                            "about~31ecd969": "1f78ac0e"
                        }[e] + ".js"
                    }(e);
                var u = new Error;
                i = function (t) {
                    c.onerror = c.onload = null,
                        clearTimeout(d);
                    var n = o[e];
                    if (0 !== n) {
                        if (n) {
                            var a = t && ("load" === t.type ? "missing" : t.type)
                                , r = t && t.target && t.target.src;
                            u.message = "Loading chunk " + e + " failed.\n(" + a + ": " + r + ")",
                                u.name = "ChunkLoadError",
                                u.type = a,
                                u.request = r,
                                n[1](u)
                        }
                        o[e] = void 0
                    }
                }
                ;
                var d = setTimeout((function () {
                        i({
                            type: "timeout",
                            target: c
                        })
                    }
                ), 12e4);
                c.onerror = c.onload = i,
                    document.head.appendChild(c)
            }
        return Promise.all(t)
    }
        ,
        s.m = e,
        s.c = a,
        s.d = function (e, t, n) {
            s.o(e, t) || Object.defineProperty(e, t, {
                enumerable: !0,
                get: n
            })
        }
        ,
        s.r = function (e) {
            "undefined" != typeof Symbol && Symbol.toStringTag && Object.defineProperty(e, Symbol.toStringTag, {
                value: "Module"
            }),
                Object.defineProperty(e, "__esModule", {
                    value: !0
                })
        }
        ,
        s.t = function (e, t) {
            if (1 & t && (e = s(e)),
            8 & t)
                return e;
            if (4 & t && "object" == typeof e && e && e.__esModule)
                return e;
            var n = Object.create(null);
            if (s.r(n),
                Object.defineProperty(n, "default", {
                    enumerable: !0,
                    value: e
                }),
            2 & t && "string" != typeof e)
                for (var a in e)
                    s.d(n, a, function (t) {
                        return e[t]
                    }
                        .bind(null, a));
            return n
        }
        ,
        s.n = function (e) {
            var t = e && e.__esModule ? function () {
                        return e.default
                    }
                    : function () {
                        return e
                    }
            ;
            return s.d(t, "a", t),
                t
        }
        ,
        s.o = function (e, t) {
            return Object.prototype.hasOwnProperty.call(e, t)
        }
        ,
        s.p = "/",
        s.oe = function (e) {
            throw e
        }
    ;
    var c = window.webpackJsonp = window.webpackJsonp || []
        , u = c.push.bind(c);
    c.push = t,
        c = c.slice();
    for (var d = 0; d < c.length; d++)
        t(c[d]);
    var l = u;
    i.push([0, "chunk-vendors~253ae210"]),
        n()
}({
    0: function (e, t, n) {
        e.exports = n("cd49")
    },
    "3fa5": function (e, t, n) {
        "use strict";
        n.d(t, "d", (function () {
                return r
            }
        )),
            n.d(t, "a", (function () {
                    return i
                }
            )),
            n.d(t, "c", (function () {
                    return s
                }
            )),
            n.d(t, "b", (function () {
                    return u
                }
            ));
        var a = n("1da1");

        function r(e) {
            var t = {};
            return o(e) && (o((t = JSON.parse(e)).data) && (t.data = JSON.parse(t.data),
            o(t.data.content) && (t.data.content = JSON.parse(t.data.content)))),
                t
        }

        function o(e) {
            try {
                return JSON.parse(e),
                    !0
            } catch (e) {
                return !1
            }
        }

        function i(e, t) {
            var n = arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : "";
            return {
                conversationID: "C2C" + e,
                unreadCount: 0,
                isVirtual: !0,
                type: "C2C",
                lastMessage: {
                    lastTime: (new Date).getTime() / 1e3,
                    fromAccount: null,
                    messageForShow: "[自定义消息]",
                    type: "TIMCustomElem",
                    payload: {
                        description: "您好，请问有什么可以帮助您?",
                        data: '{"data":"{\\"content\\":\\"\\",\\"contentType\\":\\"text/plain\\"}","type":"qimmsg"}'
                    },
                    isRevoked: !1
                },
                _isInfoCompleted: !1,
                peerReadTime: 0,
                groupAtInfoList: [],
                userProfile: {
                    userID: e,
                    nick: t,
                    gender: "",
                    birthday: 0,
                    location: "",
                    selfSignature: "",
                    allowType: "AllowType_Type_AllowAny",
                    language: 0,
                    avatar: n,
                    messageSettings: 0,
                    adminForbidType: "AdminForbid_Type_None",
                    level: 0,
                    role: 0,
                    lastUpdatedTime: 0,
                    profileCustomField: []
                }
            }
        }

        function s(e, t) {
            return c.apply(this, arguments)
        }

        function c() {
            return (c = Object(a.a)(regeneratorRuntime.mark((function e(t, n) {
                    var a, r, o, i;
                    return regeneratorRuntime.wrap((function (e) {
                            for (; ;)
                                switch (e.prev = e.next) {
                                    case 0:
                                        return e.prev = 0,
                                            e.next = 3,
                                            window.$qzd_tim.getUserProfile({
                                                userIDList: [t]
                                            });
                                    case 3:
                                        o = e.sent,
                                            i = o.data,
                                            n.nick = null === (a = i[0]) || void 0 === a ? void 0 : a.nick,
                                            n.avatar = null === (r = i[0]) || void 0 === r ? void 0 : r.avatar,
                                            e.next = 13;
                                        break;
                                    case 10:
                                        e.prev = 10,
                                            e.t0 = e.catch(0);
                                    case 13:
                                    case "end":
                                        return e.stop()
                                }
                        }
                    ), e, null, [[0, 10]])
                }
            )))).apply(this, arguments)
        }

        n("96cf"),
            n("b0c0");
        var u = function (e) {
            var t = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : {};
            switch (e) {
                case "img":
                    return {
                        content: {
                            imageUrl: t.url,
                            imgWidth: t.width,
                            imgHeight: t.height,
                            originImgSize: t.size
                        },
                        type: "imgs/*"
                    };
                case "file":
                    return {
                        content: {
                            fileUrl: t.url,
                            fileName: t.name,
                            fileSize: t.size
                        },
                        type: "file/*"
                    };
                default:
                    return {}
            }
        }
    },
    "4e07": function (e, t, n) {
        n("caad"),
            n("2532");
        var a = "prod";
        location.origin.includes("qizhidao") && n("f36a").singleton({
            pid: "fyw9n1jhpf@e11f22a9894391f",
            tag: "PCIM",
            sample: 10,
            imgUrl: "https://arms-retcode.aliyuncs.com/r.png?",
            environment: a
        })
    },
    cd49: function (e, t, n) {
        "use strict";
        n.r(t);
        var a = {};
        n.r(a),
            n.d(a, "parseTimeToM", (function () {
                    return q
                }
            )),
            n.d(a, "parseTime", (function () {
                    return B
                }
            )),
            n.d(a, "parseDate", (function () {
                    return H
                }
            )),
            n.d(a, "parseDateDot", (function () {
                    return Q
                }
            )),
            n.d(a, "dateSpace", (function () {
                    return W
                }
            )),
            n.d(a, "numTofixed2", (function () {
                    return Z
                }
            )),
            n.d(a, "numTofixed2html", (function () {
                    return $
                }
            )),
            n.d(a, "emptyText", (function () {
                    return G
                }
            )),
            n("6b30"),
            n("450d");
        var r = n("c284")
            , o = n.n(r)
            , i = (n("06f1"),
            n("6ac9"))
            , s = n.n(i)
            , c = (n("f225"),
            n("89a9"))
            , u = n.n(c)
            , d = (n("e3ea"),
            n("7bc3"))
            , l = n.n(d)
            , f = (n("a7cc"),
            n("df33"))
            , p = n.n(f)
            , v = (n("be4f"),
            n("896a"))
            , m = n.n(v)
            , g = (n("10cb"),
            n("f3ad"))
            , h = n.n(g)
            , y = (n("f4f9"),
            n("c2cc"))
            , b = n.n(y)
            , w = (n("7a0f"),
            n("0f6c"))
            , C = n.n(w)
            , M = (n("1951"),
            n("eedf"))
            , I = n.n(M)
            , D = (n("0fb7"),
            n("f529"))
            , O = n.n(D)
            , T = (n("e623"),
            n("e379"),
            n("5dc8"),
            n("37e1"),
            n("159b"),
            n("b64b"),
            n("4de4"),
            n("2b0e"))
            , S = (n("eed1"),
            n("2877"))
            , U = Object(S.a)({}, (function () {
                var e = this.$createElement
                    , t = this._self._c || e;
                return t("div", {
                    attrs: {
                        id: "app"
                    }
                }, [t("router-view")], 1)
            }
        ), [], !1, null, "e1b14406", null).exports
            , L = (n("d3b7"),
            n("3ca3"),
            n("ddb0"),
            n("8c4f"));
        T.default.use(L.a);
        var x = [{
            path: "/",
            name: "pc_im_window",
            component: function () {
                return n.e("about~31ecd969").then(n.bind(null, "3a87"))
            }
        }]
            , j = new L.a({
            mode: "history",
            base: "/",
            routes: x
        })
            , R = (n("4e07"),
            n("e23e"))
            , z = n.n(R)
            , N = "1400138868";
        var F = n("2f62")
            , P = n("2909")
            , k = (n("4ec9"),
            n("99af"),
            n("fb6a"),
            n("ac1f"),
            n("5319"),
            n("ed08"))
            , E = n("3fa5")
            , Y = {
            namespaced: !0,
            state: {
                conversationList: [],
                conversationMap: new Map,
                currentConversation: {
                    userProfile: {}
                },
                initImInfo: {}
            },
            mutations: {
                updateConversationList: function (e, t) {
                    var n = t.filter((function (t) {
                            e.conversationList.forEach((function (e) {
                                    e.draft && e.conversationID === t.conversationID && (t.draft = e.draft,
                                        t.draftContent = e.draftContent)
                                }
                            ));
                            try {
                                !t.userProfile || t.userProfile.avatar || t.userProfile.nick || Object(E.c)(t.userProfile.userID, t.userProfile)
                            } catch (e) {
                            }
                            return -1 !== t.conversationID.indexOf("C2CE")
                        }
                    ));
                    n.length > 2 && (n = [n[0]].concat(Object(P.a)(Object(k.a)(n.slice(1))))),
                        e.conversationList = n,
                        e.conversationList.forEach((function (t, n) {
                                return e.conversationMap.set(t.conversationID, {
                                    index: n
                                })
                            }
                        ))
                },
                updateConversationMap: function (e, t) {
                    e.conversationMap = t
                },
                updateCurrentConversation: function (e, t) {
                    try {
                        t.conversationID !== e.currentConversation.conversationID || t.userProfile.avatar || t.userProfile.nick || (t.userProfile.avatar = e.currentConversation.userProfile.avatar,
                            t.userProfile.nick = e.currentConversation.userProfile.nick)
                    } catch (e) {
                    }
                    e.currentConversation = t || {}
                },
                updateInitImInfo: function (e) {
                    var t = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : {};
                    t.initEnd = !0,
                        e.initImInfo = t
                }
            },
            getters: {
                toAccount: function (e) {
                    if (!e.currentConversation || !e.currentConversation.conversationID)
                        return "";
                    switch (e.currentConversation.type) {
                        case "C2C":
                            return e.currentConversation.conversationID.replace("C2C", "");
                        case "GROUP":
                            return e.currentConversation.conversationID.replace("GROUP", "");
                        default:
                            return e.currentConversation.conversationID
                    }
                }
            }
        }
            , A = (n("d81d"),
            {
                namespaced: !0,
                state: {
                    historyChatRecordMap: new Map,
                    nextReqMessageID: "",
                    isCompleted: !1,
                    currentMessageList: [],
                    messageContent: "",
                    currentAudioUrl: "",
                    scrollTopInin: !0,
                    audioChangeTextMap: new Map,
                    netStatusText: "",
                    errorMessageMap: new Map,
                    fileMessageMap: new Map,
                    unreadCount: 0
                },
                mutations: {
                    uploadCurrentAudioUrl: function (e, t) {
                        e.currentAudioUrl = t
                    },
                    uploadMessageContent: function (e, t) {
                        e.messageContent = t
                    },
                    setSrollTopInin: function (e, t) {
                        e.scrollTopInin = t
                    },
                    changeState: function (e) {
                        var t = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : {};
                        e[t.key] = t.data
                    },
                    updateUnreadCount: function (e, t) {
                        e.unreadCount = t
                    }
                },
                actions: {
                    getMessageList: function (e, t) {
                        return new Promise((function (n, a) {
                                var r = t.conversationID
                                    , o = t.isFirst
                                    , i = e.state
                                    , s = i.nextReqMessageID
                                    , c = i.currentMessageList;
                                window.$qzd_tim.getMessageList({
                                    conversationID: r,
                                    nextReqMessageID: o ? null : s,
                                    count: 15
                                }).then((function (t) {
                                        var a = JSON.parse(JSON.stringify(t));
                                        if (e.state.nextReqMessageID = a.data.nextReqMessageID,
                                            e.state.isCompleted = a.data.isCompleted,
                                            a.data.messageList = a.data.messageList.map((function (e) {
                                                    e.payload.data = Object(E.d)(e.payload.data);
                                                    try {
                                                        "text/customCard" === e.payload.data.data.contentType && "2" === e.payload.data.data.content.isCommonCustomer && e.payload.data.data.content.textMsg && (e.payload.data.data.content = e.payload.data.data.content.textMsg,
                                                            e.payload.data.data.contentType = "text/plain")
                                                    } catch (e) {
                                                    }
                                                    return e
                                                }
                                            )),
                                            o) {
                                            var i = e.state.fileMessageMap.get(r);
                                            Array.isArray(i) ? e.state.currentMessageList = [].concat(Object(P.a)(a.data.messageList), Object(P.a)(i)) : e.state.currentMessageList = a.data.messageList
                                        } else
                                            e.state.currentMessageList = [].concat(Object(P.a)(a.data.messageList), Object(P.a)(c));
                                        n(t)
                                    }
                                )).catch((function (e) {
                                        a(e)
                                    }
                                ))
                            }
                        ))
                    },
                    pushCurrentMessageList: function (e, t) {
                        var n = e.state
                            , a = e.rootState;
                        if (a.conversation.currentConversation.conversationID)
                            if (Array.isArray(t)) {
                                var r = t.filter((function (e) {
                                        return e.conversationID === a.conversation.currentConversation.conversationID
                                    }
                                ));
                                r = JSON.parse(JSON.stringify(r)),
                                    n.currentMessageList = [].concat(Object(P.a)(n.currentMessageList), Object(P.a)(r.map((function (e) {
                                            e.payload.data = Object(E.d)(e.payload.data);
                                            try {
                                                "text/customCard" === e.payload.data.data.contentType && "2" === e.payload.data.data.content.isCommonCustomer && e.payload.data.data.content.textMsg && (e.payload.data.data.content = e.payload.data.data.content.textMsg,
                                                    e.payload.data.data.contentType = "text/plain")
                                            } catch (e) {
                                            }
                                            return e
                                        }
                                    ))))
                            } else if (t.conversationID === a.conversation.currentConversation.conversationID) {
                                t.payload.data = "string" == typeof t.payload.data ? Object(E.d)(t.payload.data) : t.payload.data,
                                    n.currentMessageList = [].concat(Object(P.a)(n.currentMessageList), [t]);
                                try {
                                    "text/customCard" === t.payload.data.data.contentType && "2" === t.payload.data.data.content.isCommonCustomer && t.payload.data.data.content.textMsg && (t.payload.data.data.content = t.payload.data.data.content.textMsg,
                                        t.payload.data.data.contentType = "text/plain")
                                } catch (e) {
                                }
                            }
                    }
                }
            });
        T.default.use(F.a);
        var _ = new F.a.Store({
            state: {},
            mutations: {},
            modules: {
                conversation: Y,
                message: A
            },
            actions: {}
        })
            , J = (n("daf9"),
            n("3835"))
            , V = (n("b680"),
            n("a9e3"),
            n("1276"),
            n("a15b"),
            window.moment);

        function q(e) {
            return V(new Date(e)).format("YYYY-MM-DD HH:mm")
        }

        function B(e) {
            return V(new Date(e)).format("YYYY-MM-DD HH:mm:ss")
        }

        function H(e, t) {
            return e ? V(new Date(e)).format("YYYY-MM-DD") : t || ""
        }

        function Q(e) {
            return e ? V(new Date(e)).format("YYYY.MM.DD") : ""
        }

        function W(e) {
            var t = (new Date).getTime()
                , n = Math.floor(parseInt(e) - t);
            return null === e ? "" : n <= 0 ? function (e) {
                if (null === e)
                    return "";

                function t(e) {
                    return e < 10 ? "0" + e : e
                }

                var n = new Date(e)
                    , a = n.getFullYear()
                    , r = n.getMonth() + 1
                    , o = n.getDate();
                return a + "-" + t(r) + "-" + t(o)
            }(e) + "已截止" : n > 0 && n < 864e5 ? Math.ceil(n / 36e5) + "小时后截止" : n < 2592e6 ? Math.ceil(n / 864e5) + "天后截止" : Math.floor(n / 30 / 864e5) + "个月" + Math.ceil(n % 2592e6 / 864e5) + "天后截止"
        }

        function Z(e) {
            return Number(e || 0).toFixed(2)
        }

        function $(e, t) {
            if (t) {
                var n = e;
                if (-1 !== e.indexOf("+")) {
                    var a = e.split("+")
                        , r = [];
                    return a.forEach((function (e) {
                            var t = e.split(".")
                                , n = Object(J.a)(t, 2)
                                , a = n[0]
                                , o = n[1];
                            r.push('<span style="font-size:0.32rem;"><span>'.concat(a, '.</span><span style="font-size:0.24rem;">').concat(o, "</span></span>"))
                        }
                    )),
                        r.join(" + ")
                }
                var o = n.split(".")
                    , i = Object(J.a)(o, 2)
                    , s = i[0]
                    , c = i[1];
                return '<span style="font-size:0.32rem;"><span>'.concat(s, '.</span><span style="font-size:0.24rem;">').concat(c, "</span></span>")
            }
            var u = "".concat(Number(e || 0).toFixed(2)).split(".")
                , d = Object(J.a)(u, 2)
                , l = d[0]
                , f = d[1];
            return '<span style="font-size:0.32rem;"><span>'.concat(l, '.</span><span style="font-size:0.24rem;">').concat(f, "</span></span>")
        }

        function G(e) {
            return e || "--"
        }

        n("db4d");
        var X = n("1da1")
            , K = (n("96cf"),
            !1);

        function ee(e, t) {
            var n = e.type
                , a = e.data;
            if (n && -1 !== n.indexOf("qzd") && (t || "[object Object]" !== Object.prototype.toString.call(t)))
                switch (n) {
                    case "qzd_init_imServe":
                        !function (e) {
                            te.apply(this, arguments)
                        }(a, t);
                        break;
                    case "qzd_show_imServe":
                        K = !0,
                            function () {
                                var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
                                try {
                                    var t;
                                    e.initConversationIdChange = window.$store.state.conversation.initImInfo.initConversationId !== e.initConversationId || "list" === (null == e || null === (t = e.cardInfo) || void 0 === t ? void 0 : t.sendType),
                                        e.noCreateConversation = !1,
                                        window.$store.commit("conversation/updateInitImInfo", e),
                                        window.$bus.$emit("qzd_show_imServe")
                                } catch (e) {
                                }
                            }(a, t);
                        break;
                    case "loginOut":
                        window.$qzd_tim.loginOut()
                }
        }

        function te() {
            return (te = Object(X.a)(regeneratorRuntime.mark((function e(t) {
                    var n;
                    return regeneratorRuntime.wrap((function (e) {
                            for (; ;)
                                switch (e.prev = e.next) {
                                    case 0:
                                        n = t.logLevel,
                                        t.noCreateConversation && (t.noCreateConversation = !K),
                                        n && window.$qzd_tim.setLogLevel(n),
                                            window.$store.commit("conversation/updateInitImInfo", t);
                                    case 4:
                                    case "end":
                                        return e.stop()
                                }
                        }
                    ), e)
                }
            )))).apply(this, arguments)
        }

        Object.keys(a).forEach((function (e) {
                T.default.filter(e, a[e])
            }
        )),
            T.default.prototype.$bus = new T.default,
            T.default.prototype.$store = _,
            T.default.prototype.$CopyData = function (e) {
                try {
                    return JSON.parse(JSON.stringify(e))
                } catch (t) {
                    return e
                }
            }
            ,
            T.default.prototype.$message = O.a,
            window.$store = _;
        if (function (e, t, n, a) {
            window.TIM = z.a,
                window.$bus = n,
                window.$qzd_tim = e,
                t.prototype.TIM = z.a,
                t.prototype.$qzd_tim = e
        }(function () {
            var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
            try {
                var t = e.SDKAppID
                    , n = e.logLevel
                    , a = {
                    SDKAppID: t
                }
                    , r = z.a.create(a);
                return r.setLogLevel(n || 0),
                    r
            } catch (e) {
            }
        }({
            SDKAppID: N,
            logLevel: 4
        }), T.default, T.default.prototype.$bus),
            window.addEventListener("message", (function (e) {
                    ee(e.data, T.default)
                }
            ), !1),
        "http://localhost:8101" === location.origin) {
            var ne = {
                userID: "4bfe57f6177b456d8c00e4250702b7d9",
                userSig: "eJw1jl0LgjAYhf-LrkPerX0pdFl0oUUUCN65tsnI2VIpK-rvidbl*XgO541O6TEyQ3CtQQlhMQGAxWTeTYsSRCJAs*70pQzBaZRgCoBBEuBz4rRpemfdBFBlDROWYyEUZVzLM4ChhIEAooSO-2uuGsuWar4NEt*afSHpMzvkg2g6X73cdVfnqapL-dhkvvDlevUDe*fHp5gTRhmDJf18ASwWOGo_"
            };
            ee({
                data: {
                    userID: ne.userID,
                    userSig: ne.userSig,
                    initConversationId: "E398862580510101504",
                    signature: "1W4cRt",
                    accessToken: "eyJhbGciOiJIUzUxMiJ9.ZXlKNmFYQWlPaUpFUlVZaUxDSmhiR2NpT2lKa2FYSWlMQ0psYm1NaU9pSkJNVEk0UTBKRExVaFRNalUySW4wLi45a1N4azUtazJCLU9QX1UtSzdMWXV3Llk3dlhzYkFHbngtLUR0NFd3bjA5dHRLSUxCU1BRVThEeE92RngweG1FU19Fc2lJeFlFcGt2S05hSU5CSVZSbl9hQUdna0hicUdsNVY1eFl5LXB4UW42bjQxMTdFWnBiVi1URHpVcHBnb01YcDBOdERHZTllN0U0ZzRBOVl1ZzVXY29MNjZlNXFNNVFhZGt0cXpCUS1VM0RvREJuTnJpRXQwamliYVRUaTFPZ0xGTWtUeWpSRU03U3pBazcxcURpQVJzVFNzZkNVanFSWGFzVHBKV0tTX3hmSmp0Y2VCR1hDTzFQZ1ZPMHNmdkZGblNUbU9OT0E0WE9OajFWb1dhTUV1U1Jqbzdma1R2ZlE0Y1pLTHhOd1dKV0NIM2hTdjBPQkI3UTBSVm5vNzNEQmJYd1JsQ3lPMmxRMTZnbG91elJhLjZacUpvOEQzbkhMUURHYzlmeTlhZnc.fFveyFlYb5vqgFpIEXchIWCqaKoyOH3PKH9QkQYIXUNa00iR6VwdTl-IP4hFeGSwL5LFrC4-vwtDDOsG78yAIA"
                },
                type: "qzd_init_imServe"
            }, T.default)
        }
        T.default.use(I.a),
            T.default.use(C.a),
            T.default.use(b.a),
            T.default.use(h.a),
            T.default.use(m.a),
            T.default.use(p.a),
            T.default.use(l.a),
            T.default.use(u.a),
            T.default.use(s.a),
            T.default.use(o.a),
            new T.default({
                router: j,
                store: _,
                render: function (e) {
                    return e(U)
                }
            }).$mount("#app")
    },
    daf9: function (e, t, n) {
    },
    e53a: function (e, t, n) {
    },
    ed08: function (e, t, n) {
        "use strict";
        n.d(t, "b", (function () {
                return a
            }
        )),
            n.d(t, "a", (function () {
                    return r
                }
            )),
            n.d(t, "c", (function () {
                    return o
                }
            )),
            n.d(t, "d", (function () {
                    return i
                }
            )),
            n("d3b7"),
            n("3ca3"),
            n("ddb0"),
            n("2b3d"),
            n("fb6a"),
            n("a434");
        var a = function (e) {
            return new Promise((function (t) {
                    var n = {
                        width: 200,
                        height: 200
                    }
                        , a = new FileReader(e);
                    a.readAsDataURL(e),
                        n.url = window.URL.createObjectURL(e),
                        a.onloadend = function (e) {
                            var a = e.target.result
                                , r = new Image;
                            r.src = a,
                                r.onload = function () {
                                    n.width = r.naturalWidth,
                                        n.height = r.naturalHeight,
                                        t(n)
                                }
                                ,
                                r.onerror = function () {
                                    t(n)
                                }
                        }
                }
            ))
        };

        function r(e) {
            try {
                var t, n, a, r, o, i = e.length;
                for (o = e.slice(0),
                         t = 0; t < i; t++) {
                    for (r = 0,
                             n = i - 1; n > t; n--)
                        if (o[n].lastMessage)
                            o[n].lastMessage.lastTime > o[n - 1].lastMessage.lastTime && (a = o[n],
                                o[n] = o[n - 1],
                                o[n - 1] = a,
                                r = 1);
                        else {
                            var s = o[n].splice(n, 1);
                            o.push(s)
                        }
                    if (!r)
                        return o
                }
            } catch (e) {
            }
        }

        function o(e, t, n) {
            var a, r = "";
            void 0 === e && (e = 6),
            "string" == typeof t && (n = t),
                a = t && "number" == typeof t ? Math.round(Math.random() * (t - e)) + e : e,
                n = n || "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
            for (var o = 0; o < a; o++) {
                var i = Math.round(Math.random() * (n.length - 1));
                r += n.substring(i, i + 1)
            }
            return r
        }

        function i(e) {
            var t = e.checkFn
                , n = e.time
                , a = e.timeout
                , r = null
                , o = (new Date).getTime()
                , i = a || 12e4;
            return new Promise((function (e, a) {
                    try {
                        r = setInterval((function () {
                                var n = (new Date).getTime()
                                    , a = o + i;
                                "function" == typeof t && t() ? (clearInterval(r),
                                    e(!0)) : n > a && (clearInterval(r),
                                    e(!1))
                            }
                        ), n)
                    } catch (t) {
                        e(!1)
                    }
                }
            ))
        }
    },
    eed1: function (e, t, n) {
        "use strict";
        n("e53a")
    }
});


var C = window.loader("6062")
console.log(C)


function s(A) {
    for (var e = 1; e < arguments.length; e++) {
        var n = null != arguments[e] ? arguments[e] : {};
        e % 2 ? r(Object(n), !0).forEach((function (e) {
                t(A, e, n[e])
            }
        )) : Object.getOwnPropertyDescriptors ? Object.defineProperties(A, Object.getOwnPropertyDescriptors(n)) : r(Object(n)).forEach((function (e) {
                Object.defineProperty(A, e, Object.getOwnPropertyDescriptor(n, e))
            }
        ))
    }
    return A
}

o = function (e, t) {
    return Object.prototype.hasOwnProperty.call(e, t)
}

d = function (e, t, n) {
    o(e, t) || Object.defineProperty(e, t, {
        enumerable: !0,
        get: n
    })
}

function n(e) {
    var t = e && e.__esModule ? function () {
                return e.default
            }
            : function () {
                return e
            }
    ;
    return d(t, "a", t),
        t
}

B = n(C)

console.log("B():::", B())

function D(A, e) {
    var n = function (A, e, n) {
        var t, r = "";
        void 0 === A && (A = 6),
        "string" == typeof e && (n = e),
            t = e && "number" == typeof e ? Math.round(Math.random() * (e - A)) + A : A,
            n =  "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
        for (var s = 0; s < t; s++) {
            var i = Math.round(Math.random() * (n.length - 1));
            r += n.substring(i, i + 1)
        }
        console.log("n:::" , n)
        return r
    }()

        , t =  B()(n);
    return new B()(t + A + e) + "." + n
}

e = undefined

a = "eyJhbGciOiJIUzUxMiJ9.ZXlKNmFYQWlPaUpFUlVZaUxDSmhiR2NpT2lKa2FYSWlMQ0psYm1NaU9pSkJNVEk0UTBKRExVaFRNalUySW4wLi5sSl9BclRKNTVtNEhRLTNkWVNZVjZRLm9GRTFaeWNKcjRiZFRsQm1HcEo3UTROcEpOS25ONWZ6VlY1ODYwQ0RlUE01a01aOHlva1dETTFSVGgxSDdKeUF5Ykh4QVhUUXAzNWVoX0FSWjEtWUwxdEZxb2ZZUkZaYzM1VXl5bzZDZGt0cDh4YmlJcjhnc3pDeVZnRFAtS29HQ1F1dnRpY0tlcEd1NUwyeDl2OVRFakpkN19JYjEweFVFcHItYldnVWRmOUtMMU9xMmwxZkJRQmVaajVod2FyMzAyUkpKVjRsM2JidXFUTWRzbDFEZzNpeV9ackNLODRrcGZhRWFCT2tKOWMuc3lISUdhWkE3T1ZKTUtvTEtEMVFFQQ.F5QzUtNQm-ipdIhayHg90yJKKFcaMUgbaJ7-q69yFx-HqYPLXY82rPaxSlZEDiDD290s5oe0URWEDnLjEsoXmw"

console.log(D(a, e))