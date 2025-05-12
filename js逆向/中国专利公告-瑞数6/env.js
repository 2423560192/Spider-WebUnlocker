content = "myContent"

window = global

window = top = self = global

window.top = {
    location: {
        "ancestorOrigins": {},
        "href": "http://epub.cnipa.gov.cn/",
        "origin": "http://epub.cnipa.gov.cn",
        "protocol": "http:",
        "host": "epub.cnipa.gov.cn",
        "hostname": "epub.cnipa.gov.cn",
        "port": "",
        "pathname": "/",
        "search": "",
        "hash": ""
    }
}

window.attachEvent = function () {
}

div = {
    getElementsByTagName: function () {
        return []
    }
}

head = {
    removeChild: function () {
        return 2
    }
}

setInterval = function () {
}


document = {
    createElement: function (e) {
        console.log("document:::", e)
        if (e === "div") {
            return div
        }
    },
    getElementsByTagName: function (e) {
        console.log("document:::", e)
        if (e === 'script') {
            return []
        } else if (e === 'base') {
            return {}
        }
    },
    getElementById: function () {

    },
    attachEvent: function () {

    }
}

location = {
    "ancestorOrigins": {},
    "href": "http://epub.cnipa.gov.cn/",
    "origin": "http://epub.cnipa.gov.cn",
    "protocol": "http:",
    "host": "epub.cnipa.gov.cn",
    "hostname": "epub.cnipa.gov.cn",
    "port": "",
    "pathname": "/",
    "search": "",
    "hash": ""
}

navigator = {}

history = {}
screen = {}

// function getEnv(proxy_array) {
//     for (var i = 0; i < proxy_array.length; i++) {
//         handler = `{\n
//             get: function(target, property, receiver) {\n
//                    console.log('方法：get','    对象：${proxy_array[i]}','    属性：',property,'    属性类型：',typeof property,'    属性值类型：',typeof target[property]);
//                    return target[property];
//             },
//             set: function(target, property, value, receiver){\n
//                     console.log('方法：set','    对象：${proxy_array[i]}','    属性：',property,'    属性类型：',typeof property,'    属性值类型：',typeof target[property]);
//                     return Reflect.set(...arguments);
//             }
//         }`
//         eval(`
//             try {
//                 ${proxy_array[i]};
//                 ${proxy_array[i]} = new Proxy(${proxy_array[i]}, ${handler});
//             } catch (e) {
//                 ${proxy_array[i]} = {};
//                 ${proxy_array[i]} = new Proxy(${proxy_array[i]}, ${handler});
//             }
//         `)
//     }
// }
//
// proxy_array = ['window', 'document', 'location', 'navigator', 'history', 'screen', 'head']
// getEnv(proxy_array)