require('./env')
var _N = function () {
    document.cookie = '__jsl_clearance=1589175086.234|0|' + (function () {
        var _t = [function (_N) {
                return eval('String.fromCharCode(' + _N + ')')
            },
                (function () {
                    var _N = document.createElement('div');
                    _N.innerHTML = '<a href=\'/\'>_1H</a>';
                    _N = 'https://match.yuanrenxue.cn/match/3';
                    var _t = _N.match(/https?:\/\//)[0];
                    _N = _N.substr(_t.length).toLowerCase();
                    return function (_t) {
                        for (var _1H = 0; _1H < _t.length; _1H++) {
                            _t[_1H] = _N.charAt(_t[_1H])
                        }
                        ;
                        return _t
                    }
                })()],
            _1H = [114, 115, 97, 104, 100, 114, 111, 105, 100, 120, 114, 105, 122, 121, 114, 114, 105, 97, 99, 122, 120, 101, 99, 114, 105, 97];
        for (var _N = 0; _N < _1H.length; _N++) {
            _1H[_N] = _t.reverse()[(-~[] + [] + [[]][0])](_1H[_N])
        }
        ;
        return _1H.join('')
    })() + ';Expires=Mon, 11-May-20 06:31:26 GMT;Path=/;'
};
if ((function () {
    try {
        return !!window.addEventListener;
    } catch (e) {
        return false;
    }
})()) {
    document.addEventListener('DOMContentLoaded', _N, false)
} else {
    document.attachEvent('onreadystatechange', _N)
}

_N()
console.log(document.cookie)