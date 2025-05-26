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


// 替换字符
function decrypt_str(ast) { //1.字符解码
    traverse(ast, {
        //遍历字符串节点和数字节点（数字编码or字符编码）
        'StringLiteral|NumericLiteral'(path) {
            //删除节点中的extra属性
            delete path.node.extra.raw
            //或者：path.node.extra = undefined
        }
    })
    return ast
}


ast = decrypt_str(ast)

// 执行函数
function resolveFunctionCode(scope, name) {
    let seen = new Set(); // 防止循环引用

    while (true) {
        if (seen.has(name)) break;
        seen.add(name);

        const binding = scope.getBinding(name);
        if (!binding) break;

        const node = binding.path.node;

        if (
            types.isVariableDeclarator(node)
        ) {
            const init = node.init;

            // 如果直接是函数
            if (types.isFunctionExpression(init) || types.isArrowFunctionExpression(init)) {
                return generator(init).code;
            }

            // 如果是继续指向另一个变量
            if (types.isIdentifier(init)) {
                name = init.name;
                continue;
            }

            // 如果是 window['xx'] 或 object['xx'] 也可以手动 patch
            if (types.isMemberExpression(init)) {
                // 可选扩展支持：全局对象调用，如 window['xxx']
                const code = generator(init).code;
                const value = eval(code);
                if (typeof value === 'function') {
                    return value.toString();
                }
            }
        }

        break;
    }

    return null;
}

function func_decrypt_str(ast) {
    // 第一阶段：找到解密函数并执行
    traverse(ast, {
        Identifier(path) {
            if (path.node.name === '_0x1426e3') {
                const binding = path.scope.getBinding('_0x1426e3')
                console.log('biding:' , binding)
                if (binding) {
                    const funcCode = resolveFunctionCode(path.scope, '_0x1426e3');
                    console.log('funcode' , funcCode)
                    if (funcCode) {
                        eval(`var _0x1426e3 = ${funcCode}`);
                    } else {
                        throw new Error('解密函数定义无法解析');
                    }
                    path.stop();
                }
            }
        }
    });

    // 第二阶段：替换函数调用
    traverse(ast, {
        CallExpression(path) {
            const node = path.node;
            if (node.callee.name === '_0x1426e3') {
                const args = node.arguments;
                if (
                    types.isNumericLiteral(args[0]) &&
                    types.isStringLiteral(args[1])
                ) {
                    const result = _0x1426e3(args[0].value, args[1].value);
                    path.replaceWith(types.valueToNode(result));
                }
            }
        }
    });

    return ast;
}


func_decrypt_str(ast)

// 将处理后的ast转换为js代码(反混淆后的代码)
let {code} = generator(ast);
// 保存代码
fs.writeFile('decode.js', code, (err) => {
});