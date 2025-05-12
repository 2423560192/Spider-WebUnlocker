const Crypt = require('crypto-js')

function get_pwd(e) {
    t = undefined
    var n = Crypt.enc.Utf8.parse(t || "46cc793c53dc451b")
        , r = Crypt.enc.Utf8.parse(e);
    return Crypt.AES.encrypt(r, n, {
        mode: Crypt.mode.ECB,
        padding: Crypt.pad.Pkcs7
    }).toString()
}

console.log(get_pwd('213'))