window = global

delete __dirname
delete __filename

top = self = window = global


content = "metaContent"


div = {
    getElementsByTagName: function () {
        return []
    },
    innerHTML: ''
}

meta = {
    0: {},
    1: {
        content: content,
        parentNode: {
            removeChild() {
            }
        }
    },
    length: 2
}

window.XMLHttpRequest = function () {
}
window.addEventListener = function () {

}

window.HTMLFormElement = function () {
}

delete global
delete Buffer


script = {
    length: 2,
    1: {
        getAttribute: function () {

        },
        parentElement: {
            removeChild: function () {

            }
        }
    },
    0: {
        getAttribute: function () {

        },
    }
}

//

document = {
    createElement: function (e) {
        console.log("document:::", e);
        if (e === "div") {
            return div
        }
    },
    getElementsByTagName: function (e) {
        console.log("document:::", e)
        if (e === "meta") {
            return meta
        } else if (e === 'base') {
            return []
        } else if (e === 'script') {
            return script
        }
    },
    getElementById: function (e) {

    },
    addEventListener: function () {
    },
    documentElement: {
        addEventListener: function () {
        }
    }
}


location = {
    "ancestorOrigins": {},
    "href": "https://sugh.szu.edu.cn/Html/News/Columns/7/3.html",
    "origin": "https://sugh.szu.edu.cn",
    "protocol": "https:",
    "host": "sugh.szu.edu.cn",
    "hostname": "sugh.szu.edu.cn",
    "port": "",
    "pathname": "/Html/News/Columns/7/3.html",
    "search": "",
    "hash": ""
}

setInterval = function () {
}
setTimeout = function () {
}

navigator = {
    "appCodeName": "Mozilla",
    "appName": "Netscape",
    "appVersion": "5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}

history = {}
screen = {}

'ts_js'
'auto_js'

function get_cookie() {
    return document.cookie
}





