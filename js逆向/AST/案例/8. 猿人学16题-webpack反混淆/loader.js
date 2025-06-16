//AST核心组件的导入/加载

// fs模块 用于操作文件的读写
const fs = require("fs");
// @babel/parser 用于将JavaScript代码转换为ast树
const parser = require("@babel/parser");
// @babel/traverse 用于遍历各个节点的函数
const traverse = require("@babel/traverse").default;
// @babel/types 节点的类型判断及构造等操作
const types = require("@babel/types");
// @babel/generator 将处理完毕的AST转换成JavaScript源代码
const generator = require("@babel/generator").default;

// 混淆的js代码文件
const encode_file = "./encode.js"
// 反混淆的js代码文件
const decode_file = "./decode.js"

// 读取混淆的js文件
let jsCode = fs.readFileSync(encode_file, {encoding: "utf-8"});
// 将javascript代码转换为ast树
let ast = parser.parse(jsCode)

// 源码
var r,o,a,s;_0x34e7=["AqLWq","0zyxwvutsr","TKgNw","eMnqD","thjIz","btoa","MNPQRSTWXY","oPsqh","niIlq","evetF","LVZVH","fYWEX","kmnprstwxy","aYkvo","tsrqpomnlk","HfLqY","aQCDK","lGBLj","test","3210zyxwvu","QWK2Fi",'return /" ',"hsJtK","jdwcO","SlFsj","OWUOc","LCaAn","[^ ]+)+)+[","FAVYf","2Fi+987654","floor","join","EuwBW","OXYrZ","charCodeAt","SkkHG","iYuJr","GwoYF","kPdGe","cVCcp","INQRH","INVALID_CH","charAt","push","apply","lalCJ","kTcRS",'+ this + "',"ykpOn","gLnjm","gmBaq","kukBH","dvEWE","SFKLi","^([^ ]+( +","qpomnlkjih","^ ]}","pHtmC","length","split","ABHICESQWK","FKByN","U987654321","lmHcG","dICfr","Szksx","Bgrij","iwnNJ","jihgfdecba","GfTek","gfdecbaZXY","constructo","QIoXW","jLRMs"],a=_0x34e7,s=function(e){for(;--e;)a.push(a.shift())},(o=(r={data:{key:"cookie",value:"timeout"},setCookie:function(e,o,t,r){r=r||{};for(var n=o+"="+t,i=0,u=e.length;i<u;i++){var a=e[i];n+="; "+a;var c=e[a];e.push(c),u=e.length,!0!==c&&(n+="="+c)}r.cookie=n},removeCookie:function(){return"dev"},getCookie:function(e,o){var t,r=(e=e||function(e){return e})(new RegExp("(?:^|; )"+o.replace(/([.$?*|{}()[]\/+^])/g,"$1")+"=([^;]*)"));return t=133,s(++t),r?decodeURIComponent(r[1]):void 0},updateCookie:function(){return new RegExp("\\w+ *\\(\\) *{\\w+ *['|\"].+['|\"];? *}").test(r.removeCookie.toString())}}).updateCookie())?o?r.getCookie(null,"counter"):r.removeCookie():r.setCookie(["*"],"counter",1);var l=function(e,o){return _0x34e7[e-=188]};
var l = function (e, o) {
    return _0x34e7[e -= 188]
};

const visitor = {
    CallExpression(path) {
        let {node} = path
        name = node.callee.name

        if (!types.isIdentifier(node.callee) || node.arguments.length != 1) return ;
        if (['u', 'l', 'e', 't'].includes(name) && types.isNumericLiteral(node.arguments[0])                                            ) {
            node_v = node.arguments[0].value
            let value = l(node_v)
            console.log(name, node_v)
            path.replaceWith(types.valueToNode(value))
        }
    }
}


// 调用插件,处理混淆的代码
traverse(ast, visitor)


// 将处理后的ast转换为js代码(反混淆后的代码)
let {code} = generator(ast);
// 保存代码
fs.writeFile('decode.js', code, (err) => {
});