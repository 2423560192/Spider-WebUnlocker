window = global;
delete global;


window._$ = {
    'ajax': function () {
        // console.log(arguments)
    },
    'extend':function(){
        console.log(arguments['2']['url'])
        window.pp = arguments['2']['url']
    }
}

div = {
    setAttribute: function (param) {
        // console.log("param:::", param)
    }
}

screen = {
    width:1707,
    height:960
}

document = {
    createElement: function (param) {
        // console.log("param:::", param)
        if (param === 'canvas') {
            return {
                width: 300,
                height: 150,
                getContext: function (type) {
                    if (type === '2d') {
                        return {
                            fillRect: function (x, y, w, h) {
                                // console.log(`模拟 fillRect(${x}, ${y}, ${w}, ${h})`);
                            },
                            drawImage: function () {
                            },
                            fillText: function () {
                            },
                            getImageData: function () {
                                return {data: []};  // 模拟 imageData 返回值
                            },
                            // 可以继续加需要的方法
                        };
                    } else {
                        throw new Error('仅支持 "2d" context');
                    }
                },
                toDataURL: function () {
                    return 'data:image/png;base64,MOCKED_CANVAS_DATA';
                }
            };
        }

        if (param === 'div') {
            return div
        }
    }
}
navigator = {
    webdriver:false
}

location = {}
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

proxy_array = ['window', 'document', 'location', 'navigator', 'history', 'screen', 'div', 'parseFloat' , '_$' ]
// getEnv(proxy_array)