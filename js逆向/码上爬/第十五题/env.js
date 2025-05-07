window = global

document = {
    cookie: 'Hm_lvt_b5d072258d61ab3cd6a9d485aac7f183=1746503823,1746516380,1746529458,1746535829; HMACCOUNT=74E03469813A9187; v=QTdhbDZtdUd6WUlieTdaX1loMzNFT2M2Qi1lOTFfaThUQmt1ZlNDZnBuODBFVmhaaUdkS0lSeXJmb0x6MTc0NjU0NzIxODY4NA==; Hm_lpvt_b5d072258d61ab3cd6a9d485aac7f183=1746547222',

    getElementsByTagName: function (param) {
        console.log("param:::", param)
        if (param === 'head') {
            return {}
        }
    },
    createElement: function (param) {
        console.log("param:::", param)
        if (param === 'div') {
            return {}
        }
    },
    attachEvent: function (param) {
        console.log("param:::", param)

    },
    documentElement:function (param) {
        console.log("param:::", param)
    }
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
getEnv(proxy_array)