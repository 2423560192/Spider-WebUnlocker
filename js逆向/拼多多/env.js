// window = global;
//
// delete Buffer
// delete global
//
// function browser_proxy(obj) {
//     return new Proxy(obj, {
//         get: function (target, property1) {
//             console.log('获取对象-->', obj, '属性-->', property1, '值-->', target[property1])
//             debugger
//             return Reflect.get(target, property1)
//         },
//         set: function (target, property1, value) {
//             console.log('设置对象-->', obj, '属性-->', property1, '值-->', target[property1])
//             debugger
//             Reflect.set(target, property1, value)
//         }
//     })
// }
//
// document = {
//     ontouchstart: "",
//     documentElement: {
//         scrollTop: 1
//     }
// }
//
// document.addEventListener = function () {
//
// }
//
// screen = {
//     availHeight: 1032,
//     availLeft: 1707,
//     availTop: 0,
//     availWidth: 1920,
//     width: 1920,
//     height: 1080
// }
//
// navigator = {
//     webdriver: false,
//     userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
//
// }
//
// history = {
//     back: ""
// }
//
// location = {
//     href: 'https://www.pinduoduo.com/home/3c/'
// }
//
// // window = browser_proxy(window)
// document = browser_proxy(document)
// screen = browser_proxy(screen)
// navigator = browser_proxy(navigator)
// history = browser_proxy(history)
// location = browser_proxy(location)


window = global;

delete global;
delete Buffer;

document = {
    addEventListener: function () {
    },
    cookie: '_nano_fp=XpmonpCql0Xqn5XJno_Ut7MFFzjHDdTjr3Ho7S6a'

}
screen = {
    availWidth: 1728,
    availHeight: 1085,
}
navigator = {
    appCodeName: "Mozilla",
    appName: "Netscape",
    appVersion: "5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    webdriver: false,
    userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

history = {}
history.back = function () {
}

location = {
    hash: "",
    host: "www.pinduoduo.com",
    hostname: "www.pinduoduo.com",
    href: "https://www.pinduoduo.com/home/baby/",
    origin: "https://www.pinduoduo.com",
    pathname: "/home/baby/",
    port: "",
    protocol: "https:",
}


/*function browser_proxy(obj) {

    return new Proxy(obj, {
        get: function (target, property, receiver) {
            //debugger;
            console.log("get: ", obj, property,target[property]);
            return target[property];
        },
        set: function (target, property, value) {
            //debugger;
            console.log("set: ", obj, property);
            return Reflect.set(...arguments);
        },
    })
}

window = browser_proxy(window);
document = browser_proxy(document);
navigator = browser_proxy(navigator);
screen = browser_proxy(screen);
history = browser_proxy(history);
location = browser_proxy(location);*/
