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

// JS 转 ast语法树
jscode = `var a = 0x25,b = 0b10001001,c = 0o123456,
d = "\x68\x65\x6c\x6c\x6f\x2c\x41\x53\x54",
e = "\u0068\u0065\u006c\u006c\u006f\u002c\u0041\u0053\u0054";
`

let ast = parser.parse(jscode)

traverse(ast, {
    NumericLiteral({node}) {
        if (node.extra && /^0[obx]/i.test(node.extra.raw)) {
            //移除了数字字面量节点的编码类型信息。
            node.extra = undefined;
        }
    },
    StringLiteral({node}) {
        //如果节点存在extra属性且raw是以\u或者\x
        //g 表示全局匹配,意味着在整个字符串中查找所有匹配项，而不仅仅是找到第一个匹配就停止。
        if (node.extra && /\\[ux]/gi.test(node.extra.raw)) {
            //移除了数字字面量节点的编码类型信息。
            node.extra = undefined;
        }
    }
})

let {code} = generator(ast)

console.log(code)

