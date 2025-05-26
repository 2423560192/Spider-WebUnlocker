window = global

var ts = new Date()['getTime']()

function J(b, f, p) {
    return b ^ (f >> (p % 8))
}

function B(b, f, p) {
    return b ^ (f << (p % 8))
}

function Y(b, f) {
    return (b = b + f - f) ^ f;
}

p = function (N) {
    let W = 0;
    for (let L = 0; L < N['length']; L++) {
        var O = N['charCodeAt'](L);
        for (let y = 0; y < 20; y++)
            switch (y % 3) {
                case 0:
                    W = B.apply(null, [W, O, y]);
                    break;
                case 1:
                    W = J.apply(null, [W, O, y]);
                    break;
                case 2:
                    W = Y.apply(null, [W, O]);
            }
    }
    return W;
}("123456")
'dasdasdarqwdasdasqwdasda' + ts

console.log(p)