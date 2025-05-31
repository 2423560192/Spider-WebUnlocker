d = {
    'iRmDq': function (i, j) {
        return i(j);
    },
    'GQcTJ': function (i, j) {
        return i / j;
    },
    'wUWKM': function (i, j, k) {
        return i(j, k);
    },
    'Saaxu': function (i, j) {
        return i(j);
    }
}

function b(f, g) {
    f = f - 0x90;
    let h = e[f];
    if (b['MZrkWY'] === undefined) {
        var i = function (n) {
            const o = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/=';
            let p = ''
                , q = '';
            for (let r = 0x0, s, t, u = 0x0; t = n['charAt'](u++); ~t && (s = r % 0x4 ? s * 0x40 + t : t,
            r++ % 0x4) ? p += String['fromCharCode'](0xff & s >> (-0x2 * r & 0x6)) : 0x0) {
                t = o['indexOf'](t);
            }
            for (let v = 0x0, w = p['length']; v < w; v++) {
                q += '%' + ('00' + p['charCodeAt'](v)['toString'](0x10))['slice'](-0x2);
            }
            return decodeURIComponent(q);
        };
        const m = function (n, o) {
            let p = [], q = 0x0, r, t = '';
            n = i(n);
            let u;
            for (u = 0x0; u < 0x100; u++) {
                p[u] = u;
            }
            for (u = 0x0; u < 0x100; u++) {
                q = (q + p[u] + o['charCodeAt'](u % o['length'])) % 0x100,
                    r = p[u],
                    p[u] = p[q],
                    p[q] = r;
            }
            u = 0x0,
                q = 0x0;
            for (let v = 0x0; v < n['length']; v++) {
                u = (u + 0x1) % 0x100,
                    q = (q + p[u]) % 0x100,
                    r = p[u],
                    p[u] = p[q],
                    p[q] = r,
                    t += String['fromCharCode'](n['charCodeAt'](v) ^ p[(p[u] + p[q]) % 0x100]);
            }
            return t;
        };
        b['ygIwjZ'] = m,
            c = arguments,
            b['MZrkWY'] = !![];
    }
    const j = e[0x0]
        , k = f + j
        , l = c[k];
    return !l ? (b['dcXJGV'] === undefined && (b['dcXJGV'] = !![]),
        h = b['ygIwjZ'](h, g),
        c[k] = h) : h = l,
        h;
}

function callEncryptFunction(c, d) {
    const g = window['exports']['encrypt'](c, d);
    return g;
}


let e = parseInt(Date.now() / 1000);
c = 2

console.log(e)


console.log(d['wUWKM'](callEncryptFunction, c, e));