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
jscode = `将下面的代码进行合并
var h = {};
k.aBjoq = "hello AST!";
k.wrOjg = function(P, Q) {
    return P | Q;
};
var k = h;
`

let ast = parser.parse(jscode)

traverse(ast, {
    Identifier(path) {
        let {node} = path

        let {confident, value} = path.evaluate(node);
        if (confident) {
            path.replaceWith(types.valueToNode(value))
        }
    }
})

let {code} = generator(ast)

console.log(code)

