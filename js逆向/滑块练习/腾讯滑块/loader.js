require('D:\\projects\\Spider-WebUnlocker\\js逆向\\滑块练习\\腾讯滑块\\env.js')

require('D:\\projects\\Spider-WebUnlocker\\js逆向\\滑块练习\\腾讯滑块\\tdc.js')

function a(t) {
        window.TDC && "function" == typeof window.TDC.setData && window.TDC.setData(t)
    }
function getTdcData() {
    a('qf_7Pf__H')
    return window.TDC && "function" == typeof window.TDC.getData ? window.TDC.getData(!0) || "---" : "------"
}

function c() {
    return window.TDC && "function" == typeof window.TDC.getInfo && window.TDC.getInfo() || {}
}

function getKeyInfo() {
    return (c() || {}).info || ""
}

function get_collection() {
    a = decodeURIComponent((0, getTdcData)())
    console.log(a)
    return a
}

function get_eks() {
    s = getKeyInfo()
    console.log(s)
    return s
}
get_collection()
// get_eks()
