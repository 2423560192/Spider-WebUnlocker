e = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="

function e_weAtob(r) {
    if (r = String(r).replace(/[\t\n\f\r ]+/g, ""),
        !true)
        throw new TypeError("Failed to execute 'atob' on 'Window': The string to be decoded is not correctly encoded.");
    r += "==".slice(2 - (3 & r.length));
    for (var o, n, a, c = "", i = 0; i < r.length;)
        o = e.indexOf(r.charAt(i++)) << 18 | e.indexOf(r.charAt(i++)) << 12 | (n = e.indexOf(r.charAt(i++))) << 6 | (a = e.indexOf(r.charAt(i++))),
            c += 64 === n ? String.fromCharCode(o >> 16 & 255) : 64 === a ? String.fromCharCode(o >> 16 & 255, o >> 8 & 255) : String.fromCharCode(o >> 16 & 255, o >> 8 & 255, 255 & o);
    return c
}

function l(r) {
    if (!r.data || !r.data.ev || !r.data.dt)
        return r;
    var o = r.data
        , n = o.ev
        , l = (o.dt,
        n.substring(0, 2),
        parseInt(n.substring(2, 4)))
        , s = parseInt(n.substring(4, 5))
        , a = o.data.substring(l)
        , i = ""
        , t = a.length
        , u = t % l;
    0 == u && (u = l);
    for (var c = t - u, v = new Array, p = 0; ;) {
        var d = l * p;
        if (!(d < c))
            break;
        var _ = l + d
            , g = a.substring(d, _);
        v.push(g),
            p++
    }
    var f = new Array;
    p = 0;
    for (var h = v.length, x = Math.ceil(1 * h / s), w = Math.floor(1 * h / s), k = h % s, j = 0; j < s; j++) {
        var m = j < k ? x : w;
        f.push(m)
    }
    var y = new Array;
    y.push(0),
        p = 0;
    for (var b = 0; b < s - 1; b++) {
        p += f[b],
            y.push(p)
    }
    for (var C = 0; C < x; C++)
        for (var q = 0; q < s; q++) {
            var A = y[q % s] + C;
            C >= f[q % s] || (A >= v.length || (i += v[A]))
        }
    i += a.substring(c, c + u);
    var D = e_weAtob(i)
        , I = e_weAtob(D);
    return r.data = JSON.parse(I),
        r
}


t = {
    "code": 1, "msg": "ok", "time": "1742819344", "data": {
        "data": "ZjRiZWQ4NTNhYTYzMWZXlKc2FYTjBJanBiZXeGtaWElpT2pBc0luVnT1RVMU5Td2lkWEpzSWVTFJaXdpYVdOdmJpSTY0Z3dmFXMW5YQzk0WTQlRZMmh2YjJ3Z2JHbGSW5SNWNHVWlPaUp5YjOTNiM0prWEM5bmNtOTTDJka2JDNTBaVzVzWlY2lmU3g3SW5ScGRHeGSWpvd0xDSjFjMlZmYkY3NJblZ5YkNJNklsd3SW1samIyNGlPaUpvZEbHRaMXd2ZUdONFhDOTWlc1a2N5SXNJbWx6WDSnliM2NpTENKc1oybGY205MWNEOXNaMmxrUFNXNaV0Z5Ymk1amJsd3ZEd4bElqb2lWVzVwZEOXNhWE4wSWpvd0xDSjWEM5d1lXZGxjMXd2ZDaDBkSEJ6T2x3dlhDOWTDNWdWFYUXVjRzVuSWVTFOQ3dpWjNKdmRYQmY0Y5a1pYWnBZMlZmYVSTZJbHgxTlRNeE4xeDZFRSbE1HRW9NalJjZFWnZiR1JsY2lJNk1Dd2Ym5RaU9qSXdMQ0prWlNWthV2xwWVhCd0xtTnY0djaUxDSnphR0Z5WlSTZNQ3dpY21Wc1lYUmZFhCZmFXUWlPakFzSWaDBkSEJ6T2x3dlhDOWWlY5MGFXMWxJam9pTWMWxJam9pTWpBeU5DMHWlNJNklseDFOR1V3TUeDFPREJqWTF4MU5UTTTURoY2RUVTVNamRjZFSXdYSFUzTWpRNEtTSXWVhCd0xtTnZiVnd2YWlKMGFYUnNaU0k2SWxWpaVjlzYVhOMElqb3dMpvaVhDOXdZV2RsYzF3ZJbWgwZEhCek9sd3ZYNoY0wzVnVhWFF1Y0c11aU0lzSW1selgyWnZiNjaUxDSnNaMmxrSWpvFjRDlzWjJsa1BUazFOdGeWJpNWpibHd2WVhCxJam9pVlc1cGRDQXpJdsemRDSTZNQ3dpZEhsZjR0ZuWlhOY0wzZHZjhSd2N6cGNMMXd2WjJSFibWwwTG5CdVp5SjlMJadmJHUmxjaUk2TUN3tJam81TlRVNExDSjFjRrMU5UZ2lMQ0pwWTI5ZZWEJ3WEM5cGJXZGNMNBMUlFMTVJR2h2YldVBlWEJsSWpvaWNtOTNJI5eVpGd3ZaM0p2ZFhB5aR3d1ZEdWdWJHVmhj4xZExDSmxiblJ5ZVNJZkR0ZuSWpvaVltOXZhdRaU9qQXNJbkJoY21WFOV1V3T0Z4MU5Ua3lORZMVlqQmNkVGN5TkRnlkWE5sWDJ4cGMzUWlPhSaGFXd2lPaUlpTENKZiVnd2YW1saGIyTmhhY5cFkyOXVJam9pSWl3xYMmxrSWpvd0xDSnBj5CcGJtUjFYMk5zWVhO5aR3d1WkdscGFXRndjpBeU5DMHdPUzB5TUNBhNQzB3T1NBeE56bzBNZ4MU9HUTNOMXgxTkdZFOVngxT0dKalpGeDFORSbE1EbGNkVGhrTnpjNJbWx0WVdkbFZYSnNJ1saGIyTmhhVnd2ZDF3dWFYUWdNU0JHWVcxcGQ0owZVhCbElqb2ljbTdmQyOXlaRnd2WjNKdmQzluWkd3dWRHVnViR1bkluMHNleUowYVhSc1R1JsY2lJNk1Dd2lkWENU5UVTJMQ0oxY213aUVFlpTENKcFkyOXVJamd1hDOXBiV2RjTDNoamRXhsWVhKdWFXNW5JaXd1pTSTZJbkp2ZHlJc0bVJjTDJkeWIzVndQMnc0xuUmxibXhsWVhKdUSHNpZEdsMGJHVWlPaUaWRYTmxYMnhwYzNRaUbXdpT2lKY0wzQmhaMldUlqb2lhSFIwY0hNNlM2hqZUZ3dmRXNXBkQzaUxDSnBjMTltYjJ4a1aXdpYkdkcFpDSTZPVFL2JHZHBaRDA1TlRVNUbTR1WTI1Y0wyRndjRnNmV5SnNaV0Z5Ymw5bmMTlwWkY4eE1ERTFOVEdWRGOXBaQ0k2TUN3aVMXgxTkdVd09WeDFPR1cElpd2ljMjl5ZEY5cFakFzSW5kdmNtUnpJamcFkyOXVJam9pYUhSMGVnd2ZDF3dlkyOTJaWEaWRHOXdhV01pT2lJaUMTl3ZFdKc2FXTWlPakelgybGtJam93TENKaVQzVqYjIxY0wyUnBZM1eE5Eb3lNem95TUNJc0am94TWlKOUxDSnphR0M1pseDFOelV5T0Z4MUV0kyTmx4MU5HVTJNQ0Z1hIVTBaVEE1WEhVMFam9pYUhSMGNITTZYQzdlkyOTJaWEpjTHpFd0JIa2lMQ0pwYzE5bWIykzSWl3aWJHZHBaQ0k2RYQS9iR2RwWkQwNU5UZoY200dVkyNWNMMkZ3pTSTZJbFZ1YVhRZ01p5sWDJ4cGMzUWlPakFz9pSmNMM0JoWjJWelhD9pYUhSMGNITTZYQzljVGd3ZkVzVwZEM1d2JtdpYVhOZlptOXNaR1Z5lteG5hV1FpT2prMU5UhuYVdROU9UVTFOeUlzxtTnVYQzloY0hCY0wypWYm1sMElEUWdSbkpw9qQXNJblI1Y0dVaU9pZ6WEM5M2IzSmtYQzluhDOWNMMmRrYkM1MFpXV3Ym1jaWZTeDdJblJwpYSWlPakFzSW5WelpWUxT1N3aWRYSnNJam9plpd2lhV052YmlJNkltd2YVcxblhDOTRZM2hjNtOTFjRjlwWkNJNk9UlpTENKbWNtOXRYMkZ3ozSnZkWEJmYm1GdFpTEzTnlCY2RUUmxNRGxjpIZ2lPakFzSW1selgy9pSWl3aWQyOXlaRjlqNITTZYQzljTDJka2JDpjTHpFd01UVTFNaTVxxDSnVaV1ZrWDNCeWJ5VzSW14cGJtdGZaM0p2lYTmxYM1Z5YkNJNkltJjTHlJc0ltTnlaV0YwluVndaR0YwWlY5MGFXZ5WlNJNmV5SjBhWFJz9EUmtaRngxTmpBeFpGJjZFRVek1UZGNkVFZspUQmhLREkwWEhVMk5XljTDJka2JDNWthV2xw1UVTFNaTVxY0djaWZYMD0=",
        "ev": "10184",
        "dt": "v1"
    }
}
console.log(l(t))