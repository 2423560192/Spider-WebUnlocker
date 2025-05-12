API_KEY = "a2c903cc-b31e-4547-9299-b6d07b7631ab"
s = 1111111111111
window = global

var o = {
    mathRandom: function () {
        return Math.random()
    },
    cryptoRandom: function (e) {
        var t = e || {}
            , n = t.bytesLength
            , i = void 0 === n ? 1 : n
            , o = t.UnitArray
            , a = new (void 0 === o ? Uint32Array : o)(i);
        return r.getRandomValues(a)
    }
}

function encryptApiKey() {
    var e = API_KEY
        , t = e.split("")
        , n = t.splice(0, 8);
    return e = t.concat(n).join("")
}

function encryptTime(e) {
    var t = (1 * e + s).toString().split("")
        , n = parseInt(10 * o.mathRandom(), 10)
        , r = parseInt(10 * o.mathRandom(), 10)
        , i = parseInt(10 * o.mathRandom(), 10);
    return t.concat([n, r, i]).join("")
}

function comb(e, t) {
    var n = "".concat(e, "|").concat(t);
    return window.btoa(n)
}

function u() {
    var e = (new Date).getTime()
        , t = encryptApiKey();
    return e = encryptTime(e),
        comb(t, e)
}

console.log(u())