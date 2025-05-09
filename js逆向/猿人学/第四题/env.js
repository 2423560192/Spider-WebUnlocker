window = global

div = {
    firstChild: {
        href: 'https://match.yuanrenxue.cn/match/3'
    }
}

window.addEventListener = function () {
    
}

document = {
    _events: {},

    attachEvent: function (eventName, handler) {
        console.log("attachEvent param:", eventName);
        if (!this._events[eventName]) {
            this._events[eventName] = [];
        }
        this._events[eventName].push(handler);
    },

    // 手动触发事件（模拟 IE 行为）
    fireEvent: function (eventName) {
        const handlers = this._events[eventName] || [];
        for (let fn of handlers) {
            try {
                fn();
            } catch (e) {
                console.error(`Error in handler for ${eventName}:`, e);
            }
        }
    },

    createElement: function (param) {
        console.log("param:::", param)
        if (param === 'div') {
            return div
        }
    },
    addEventListener:function () {
        
    }
};

location = {
    search: ''
}
navigator = {}
history = {}
screen = {}

_events = {}

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

proxy_array = ['window', 'document', 'location', 'navigator', 'history', 'screen', 'div', 'parseFloat', '_events']
getEnv(proxy_array)