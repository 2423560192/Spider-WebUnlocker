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


function isBaseLiteral(path) {
    if (path.isLiteral()) {
        return true;
    }
    if (path.isUnaryExpression({operator: "-"}) ||
        path.isUnaryExpression({operator: "+"})) {
        return isBaseLiteral(path.get('argument'));
    }

    return false;
}

const resolveParams =
    {
        CallExpression(path) {
            let callee = path.get('callee');
            let arguments = path.get('arguments');
            if (!callee.isFunctionExpression() || arguments.length == 0) {
                return;
            }
            let scope = callee.scope;
            let params = callee.get('params');

            if (params.length < arguments.length) {
                return;  //形参格式不能小于实参个数，防止后面的代码报错
            }

            for (let i in arguments) {
                let paramsPath = params[i];
                let argumentPath = arguments[i];
                const binding = scope.getBinding(paramsPath.node.name);
                if (!binding || !binding.constant) {
                    continue;
                }

                let canRemoved = true;

                for (let referPath of binding.referencePaths) {
                    if (argumentPath.isIdentifier() || isBaseLiteral(argumentPath)) {
                        referPath.replaceWith(argumentPath.node);
                    } else if (argumentPath.isArrayExpression()) {
                        let parentPath = referPath.parentPath
                        if (!parentPath.isMemberExpression()) {
                            canRemoved = false;
                            continue;
                        }
                        let {property} = parentPath.node;
                        if (!types.isNumericLiteral(property)) {
                            canRemoved = false;
                            continue;
                        }
                        let index = property.value;
                        if (index > argumentPath.node.elements.length) {
                            canRemoved = false;
                            continue;
                        }
                        parentPath.replaceWith(argumentPath.node.elements[index]);
                    } else {
                        canRemoved = false;
                        break;
                    }
                }
                if (canRemoved) {
                    paramsPath.remove();
                    argumentPath.remove();
                }
            }

            let {body} = callee.node.body;
                if (body.length === 1 && types.isReturnStatement(body[0])) {
                    console.log(body[0].argument)
                    path.replaceWith(body[0].argument);
                }
        },
    }
traverse(ast, resolveParams)


// 将处理后的ast转换为js代码(反混淆后的代码)
let {code} = generator(ast);
// 保存代码
fs.writeFile('decode.js', code, (err) => {
});