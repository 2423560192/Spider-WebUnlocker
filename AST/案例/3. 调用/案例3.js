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

function func_decrypt_str(ast) {
    //将一个空字符串解析成ast抽象树，此时body节点下是空的
    let newAst = parser.parse('')
    //将ast也就是slide.js代码的ast树body下的前5个节点（包含了mwbxQ.$_Cg函数和其他几个函数定义节点）取出赋值给newAst的body。取出的节点尽量多一点，满足函数的调用关系，可以为5,6,7,8,9都行。
    newAst.program.body = ast.program.body.slice(0, 5)
    //将newAst转换为js代码
    let stringDecryptFunc = generator(newAst, {compact: true,}).code
    //执行转换后的js代码（表示将mwbxQ.$_Cg函数定义的代码执行了）
    eval(stringDecryptFunc)

    //获取解密函数的名字
    const stringDecryptFuncAst = ast.program.body[2]//定位到mwbxQ.$_Cg函数节点
    //提取出该函数函数名左侧部分（对象名）：mwbxQ
    const DecryptLeftFuncName = stringDecryptFuncAst.expression.left.object.name
    //提取出该函数函数名右侧部分（属性名）：$_Cg
    const DecryptRightFuncName = stringDecryptFuncAst.expression.left.property.name

    //调用函数获取返回值替换到函数调用位置
    traverse(ast, {
        //定位CallExpression函数调用类型节点
        CallExpression(path) {
            //进行一系列判断，目的是定位到名为mwbxQ.$_Cg的函数调用
            /*
            types.isMemberExpression(path.node.callee)用于判断 path.node.callee 是否为成员表达式的函数。callee为函数节点对象。
            */
            if (types.isMemberExpression(path.node.callee) &&
                //判断callee函数对象的对象名是否等于DecryptLeftFuncName
                path.node.callee.object.name &&
                path.node.callee.object.name === DecryptLeftFuncName &&
                //判断callee函数对象的属性名是否等于DecryptRightFuncName
                path.node.callee.property.name &&
                path.node.callee.property.name === DecryptRightFuncName) {
                //将函数调用结果替换函数调用
                path.replaceWith(types.valueToNode(eval(path.toString())))
            }
        }
    })
    return ast
}


func_decrypt_str(ast)


// 将处理后的ast转换为js代码(反混淆后的代码)
let {code} = generator(ast);
// 保存代码
fs.writeFile('decode.js', code, (err) => {
});Wang18323152080