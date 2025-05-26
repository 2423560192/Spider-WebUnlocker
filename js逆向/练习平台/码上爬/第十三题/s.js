const CryptoJs = require("crypto-js")

function _0x1e5c29() {
    const hexChars = "0123456789abcdef";
    const arr = [];

    for (let i = 0; i < 32; i++) {
        arr[i] = hexChars[Math.floor(Math.random() * 16)];
    }

    return arr.join('');
}


function get_s(page){
    var pageString = '{"page":"' + page + '"}';
    var uu = _0x1e5c29()
    var tt = Date.parse(new Date());

    var r = pageString + uu + tt
    console.log(pageString.length)
    console.log(uu.length)
    console.log(tt.toString().length)
    console.log(r.length)
    console.log(r)
    return [r , tt.toString()]
}

console.log(get_s());

console.log(CryptoJs.MD5('123456').toString())