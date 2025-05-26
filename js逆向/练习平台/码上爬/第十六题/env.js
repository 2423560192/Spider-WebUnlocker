window = global;

document = {
    all:[],
    createElement: function (param) {

    },
    documentElement: function () {
    },
    createEvent: function () {
    },
    querySelector: function () {
    }

}

window.__JDWEBSIGNHELPER_$DATA__ = {
    "loader.utils#loadRacScriptOnce": {
        "https://storage.360buyimg.com/webcontainer/main/js-security-v3-rac.js?v=20250507": {}
    },
    "main.sign#__detecting": {}
}


navigator = {
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
}

window.localStorage = {
    "hexin-v": "QXhITTA5RWtFcVA0NG5FdXk3eFlrZVNqSUJhdWZvVVVMX01wQlBPbkRKYjNoejlJTzg2VndMOUNPZGVBMTc0NjU3NzY0MjAxMA==",
    "Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183": "1778165358591|1746577481,1746582669,1746616149,1746629278",
    "WQ_dy1_vk": "{\"5.0\":{\"b5216\":{\"e\":31536000,\"v\":\"rdppprd9wsc3dpa2\",\"t\":1746594471975}}}",
    "JDst_rac_last_update": "{\"v\":1746630053258,\"t\":1746630053258,\"e\":31536000}",
    "WQ_gather_wgl1": "{\"v\":\"0e919b7bd4768ad94d99f107081430a5\",\"t\":1746594472028,\"e\":31536000}",
    "_nano_fp": "XpmYn5d8nqmJXpEbnC_uphO7sVYXWszj8oBunmms",
    "WQ_gather_cv1": "{\"v\":\"f7e0a65a7204897f9e74ef4e891e8b51\",\"t\":1746594472013,\"e\":31536000}",
    "isWhitelist": "false",
    "loglevel": "SILENT",
    "WQ_dy1_tk_algo": "{\"rdppprd9wsc3dpa2\":{\"b5216\":{\"v\":\"eyJ0ayI6InRrMDN3ODZmNjFiNDYxOG4xczdtMjIxcm52OGdzOTcwaUpoSHFDaHpKZ0hKUkhDMGlNNXV3cHdKWFg4MmVWZ2RzM3AtZDRhX3BGYS1HT01NOU9IQmpSWlRhMWlZIiwiYWxnbyI6ImZ1bmN0aW9uIHRlc3QodGssZnAsdHMsYWksYWxnbyl7dmFyIHJkPScydzNUajZPdWdhM0UnO3ZhciBzdHI9XCJcIi5jb25jYXQodGspLmNvbmNhdChmcCkuY29uY2F0KHRzKS5jb25jYXQoYWkpLmNvbmNhdChyZCk7cmV0dXJuIGFsZ28uTUQ1KHN0cik7fSJ9\",\"e\":86400,\"t\":1746594472396}}}"
}

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

proxy_array = ['window', 'document', 'location', 'navigator', 'history', 'screen', 'div', 'parseFloat']
// getEnv(proxy_array)




