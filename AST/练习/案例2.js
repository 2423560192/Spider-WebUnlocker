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
jscode = `var arr = '3,4,0,5,1,2'['split'](',')
`

let ast = parser.parse(jscode)

traverse(ast, {
    CallExpression(path) {
        let {callee , arguments} = path.node;
        let data = callee.object.value;
        let func = callee.property.value;
        let ags = arguments.value;

        var res = data[func](ags);

        path.replaceWith(types.valueToNode(res));
    }
})

let {code} = generator(ast)

console.log(code)

