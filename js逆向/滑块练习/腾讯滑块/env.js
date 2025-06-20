window = global;
delete global;
delete Buffer;

screen = {
    "colorDepth": 24,
    "availHeight": 912,
    "availLeft": 0,
    "availTop": 0,
    "availWidth": 1707,
    "height": 960,
    "isExtended": false,
    "onchange": null,
    "orientation": {
        "angle": 0,
        "type": "landscape-primary",
        "onchange": null
    },
    "pixelDepth": 24,
    "width": 1707,
    "deviceXDPI": {},
    "logicalXDPI": {},
    "fontSmoothingEnabled": {}

}

style = {
    innerHTML: ""
}

div = {
    appendChild: function (param) {

    },
    cloneNode: function (param) {
    },
    insertBefore: function (param) {
    },
    outerHTML: '<div></div>',
    innerHTML: ''
}

WebGLRenderingContext = {
    getSupportedExtensions: {
        "canvas": "canvas",
        "drawingBufferColorSpace": "srgb",
        "drawingBufferFormat": 32856,
        "drawingBufferHeight": 150,
        "drawingBufferWidth": 300,
        "unpackColorSpace": "srgb"
    }

}
CanvasRenderingContext2D = {
    "canvas": "canvas",
    "direction": "ltr",
    "fillStyle": "#000000",
    "filter": "none",
    "font": "10px sans-serif",
    "fontKerning": "auto",
    "fontStretch": "normal",
    "fontVariantCaps": "normal",
    "globalAlpha": 1,
    "globalCompositeOperation": "source-over",
    "imageSmoothingEnabled": true,
    "imageSmoothingQuality": "low",
    "lang": "inherit",
    "letterSpacing": "0px",
    "lineCap": "butt",
    "lineDashOffset": 0,
    "lineJoin": "miter",
    "lineWidth": 1,
    "miterLimit": 10,
    "shadowBlur": 0,
    "shadowColor": "rgba(0, 0, 0, 0)",
    "shadowOffsetX": 0,
    "shadowOffsetY": 0,
    "strokeStyle": "#000000",
    "textAlign": "start",
    "textBaseline": "alphabetic",
    "textRendering": "auto",
    "wordSpacing": "0px",
    fillRect: function () {

    },
    fillText: function () {

    }

}


canvas = {
    getContext: function (params) {
        if (params === 'webgl') {
            return WebGLRenderingContext
        } else if (params === '2d') {
            return CanvasRenderingContext2D
        }
        console.log("canvas.getContext", '---->', params)
    },
    toDataURL: function () {
    }
}

body = {}

span = {
    setAttribute: function (param) {
        if (param === 'id') {
            return
        }
        console.log("span.setAttribute" + '----->' + param)
    },
    removeAttribute: function (param) {
        console.log("span.removeAttribute" + '----->' + param)
    },
    removeChild: function (param) {
        console.log("span.removeChild" + '----->' + param)
    },
}
iframe = {
    style: style
}
p = {}
head = {}
h1 = {}
document = {
    head: head,
    createElement: function (param) {
        if (param === 'canvas') {
            return canvas
        } else if (param === 'div') {
            return div
        } else if (param === 'span') {
            return span
        } else if (param === 'iframe') {
            return iframe
        } else if (param === 'p') {
            return p
        } else if (param === 'style') {
            return style
        } else if (param === 'h1') {
            return h1
        }
        console.log("document.createElement" + '----->' + param)
    },
    addEventListener: function (param) {
        if (param === 'touchmove') {
            return {}
        } else if (param === "mousemove") {
            return {}
        } else if (param === 'h1') {
            return h1
        }
        console.log("document.addEventListener" + '----->' + param)

    },
    getElementById: function (param) {
        if (param === 'tCaptchaDyContent') {
            return null
        }
        console.log("document.getElementById" + '----->' + param)

    },
    documentElement: function (param) {
        console.log("document.documentElement" + '----->' + param)

    },
    body: body,
    URL: 'https://turing.captcha.gtimg.com/1/template/drag_ele.html',
    location: {
        "ancestorOrigins": {
            "0": "https://cloud.tencent.com"
        },
        "href": "https://turing.captcha.gtimg.com/1/template/drag_ele.html",
        "origin": "https://turing.captcha.gtimg.com",
        "protocol": "https:",
        "host": "turing.captcha.gtimg.com",
        "hostname": "turing.captcha.gtimg.com",
        "port": "",
        "pathname": "/1/template/drag_ele.html",
        "search": "",
        "hash": ""
    },
    cookie: '',
    documentMode: '',
    charset: 'UTF-8',
    characterSet: 'UTF-8',
}
window.TCaptchaReferrer = 'https://cloud.tencent.com/product/captcha'
window.webkitRTCPeerConnection = function (param) {
    console.log("window.webkitRTCPeerConnection" + '----->' + param)

}

location = {
    "ancestorOrigins": {
        "0": "https://cloud.tencent.com"
    },
    "href": "https://turing.captcha.gtimg.com/1/template/drag_ele.html",
    "origin": "https://turing.captcha.gtimg.com",
    "protocol": "https:",
    "host": "turing.captcha.gtimg.com",
    "hostname": "turing.captcha.gtimg.com",
    "port": "",
    "pathname": "/1/template/drag_ele.html",
    "search": "",
    "hash": ""
}

navigator = {
    appCodeName: "Mozilla",
    appName: "Netscape",
    appVersion: "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    hardwareConcurrency: 16,
    languages: [
        "zh-CN",
        "zh"
    ],
    cookieEnabled: true,
    platform: 'Win32',
    webdriver: false,
    vendor: 'Google Inc.',
}
localStorage = {
    getItem(key) {
        if (key === 'TDC_itoken') {
            return "1147249477:1750066358"
        }
        console.log("localStorage.getItem" + '----->' + key)
    }
}

message = {}
load = {}
window.addEventListener = function (param) {
    if (param === 'message') {
        return message
    } else if (param === 'load') {
        return load
    } else if (param === 'mousemove') {
        return []
    }
    console.log("window.addEventListener" + '----->' + param)
}
window.DeviceOrientationEvent = function (param) {
    console.log("window.DeviceOrientationEvent" + '----->' + param)
}
RTCPeerConnection = {
    createDataChannel: function (param) {
    }
}
window.RTCPeerConnection = function (param) {
    return RTCPeerConnection
}
window.mozRTCPeerConnection = function (param) {
    console.log("window.mozRTCPeerConnection" + '----->' + param)
}
window.msRTCPeerConnection = function (param) {
    console.log("window.msRTCPeerConnection" + '----->' + param)
}

window.matchMedia = function (param) {
    if (param === "(prefers-color-scheme: dark)") {
        return {
            "media": "(prefers-color-scheme: dark)",
            "matches": false,
            "onchange": null
        }
    } else if (param === "(prefers-reduced-motion: reduce)") {
        return {
            "media": "(prefers-reduced-motion: reduce)",
            "matches": false,
            "onchange": null
        }
    } else if (param === "(prefers-reduced-motion: no-preference)") {
        return {
            "media": "(prefers-reduced-motion: no-preference)",
            "matches": true,
            "onchange": null
        }
    } else if (param === "(prefers-color-scheme: light)") {
        return {
            "media": "(prefers-color-scheme: light)",
            "matches": true,
            "onchange": null
        }
    }

    console.log("window.matchMedia" + '----->' + param)
}
CSS = {
    supports: function (propertyName, value) {
        if (propertyName == "overscroll-behavior") {
            return true
        } else {
            return false
        }
        console.log("CSS.supports" + '----->' + propertyName, value)
    }
}
window.CSS = CSS
window.innerWidth = 1707
window.innerHeight = 150
sessionStorage = {}
history = {}

function getEnv(proxy_array) {
    for (var i = 0; i < proxy_array.length; i++) {
        handler = `{\n
            get: function(target, property, receiver) {\n
                   console.log('方法：get','    对象：${proxy_array[i]}','    属性：',property,'    属性类型：',typeof property,'    属性值类型：',typeof target[property]);
                   return target[property];
            }, 
            set: function(target, property, value, receiver){\n
                    console.log('方法：set','    对象：${proxy_array[i]}','    属性：',property,'    属性类型：',typeof property,'    属性值类型：',typeof target[property]);
                    return Reflect.set(...arguments);
            }
        }`
        eval(`
            try {
                ${proxy_array[i]};
                ${proxy_array[i]} = new Proxy(${proxy_array[i]}, ${handler});
            } catch (e) {
                ${proxy_array[i]} = {};
                ${proxy_array[i]} = new Proxy(${proxy_array[i]}, ${handler});
            }
        `)
    }
}

proxy_array = ['window','document', 'location', 'navigator', 'history', 'screen', 'div', 'sessionStorage', "iframe"]
// proxy_array = ["location", "navigator", "history", "screen", "localStorage", "sessionStorage",'document']
// proxy_array = ['document', 'div', 'body', 'head', 'canvas', "span", 'h1', 'iframe', 'WebGLRenderingContext', 'CanvasRenderingContext2D', "location", "navigator", "history", "screen", "localStorage", "sessionStorage", 'style']
getEnv(proxy_array)