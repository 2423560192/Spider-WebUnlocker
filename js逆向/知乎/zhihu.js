var tp = {}

function t5(tt) {
    return Array.from(tt).reduce(function (tt, te) {
        var tr = te[0]
            , ti = te[1];
        return tt[tr] = ti,
            tt
    }, {})
}

console.log(t5(tp));