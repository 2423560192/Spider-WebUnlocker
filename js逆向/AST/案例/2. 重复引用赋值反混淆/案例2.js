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

function func_replace(path) {
    const node = path.node;
    if (node.declarations.length !== 3) return
    if (generator(node.declarations[0].init).code !== 'mwbxQ.$_Cg') return
    node.declarations = [node.declarations[0], node.declarations[2]]
    node.declarations[1].init = node.declarations[0].init
    path.getNextSibling().remove()
    path.getNextSibling().node.declarations[0].init = node.declarations[0].init

}

function func_replaces(path) {
    const node = path.node
    const scope = path.scope

    const leftName = node.id.name

    if (generator(node.init).code !== 'mwbxQ.$_Cg') return

    let binding_left = scope.getBinding(leftName)

    if (binding_left.referencePaths.length !== 0) {

        binding_left.referencePaths.forEach(function (path) {
            const left_path = types.identifier("mwbxQ")
            const right_path = types.identifier("$_Cg")

            const replace_path = types.memberExpression(left_path, right_path)
            path.replaceWithMultiple(replace_path)
        })


    }
    path.remove()

}


// 调用插件,处理混淆的代码
traverse(ast, {
    VariableDeclaration: func_replace
})

// 替换
traverse(ast, {
    VariableDeclarator: func_replaces
})


// 将处理后的ast转换为js代码(反混淆后的代码)
let {code} = generator(ast);
// 保存代码
fs.writeFile('decode.js', code, (err) => {
});