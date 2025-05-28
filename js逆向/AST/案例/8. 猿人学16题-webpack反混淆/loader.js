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


function isExpressionConstant(PathOrNode) {

    let node = PathOrNode.node || PathOrNode;

    let BrowList = ['window', 'document', 'navigator', 'location', 'history', 'screen',];

    if (types.isLiteral(node) && node.value != null) {
        return true;
    }

    if (types.isIdentifier(node) && BrowList.includes(node.name)) {
        return true;
    }

    if (types.isIdentifier(node) && typeof globalThis[node.name] != "undefined") {
        return true;
    }

    if (types.isMemberExpression(node)) {
        let {object, property} = node;

        if (types.isIdentifier(object) && typeof globalThis[object.name] != "undefined") {
            let properName = types.isIdentifier(property) ? property.name : property.value;
            if (typeof globalThis[object.name][properName] != "undefined") {
                return true;
            }
        }

        if (types.isMemberExpression(object)) {
            return isExpressionConstant(object);
        }

    }

    if (types.isUnaryExpression(node) && ["+", "-", "!", "typeof", "~"].includes(node.operator)) {
        return isExpressionConstant(node.argument);
    }

    return false;
}

const visitor = {
    VariableDeclarator(path) {
        let scope = path.scope;
        let {id, init} = path.node;

        if (!types.isIdentifier(id) || init == null || !isExpressionConstant(init)) {
            return;
        }

        const binding = scope.getBinding(id.name);

        if (!binding) return;

        let {constant, referencePaths, constantViolations} = binding;

        if (constantViolations.length > 1) {
            return;
        }

        if (constant || constantViolations[0] == path) {
            for (let referPath of referencePaths) {
                referPath.replaceWith(init);
            }
        }
    },
}


// 调用插件,处理混淆的代码
traverse(ast, visitor)


const cons = {
    "BinaryExpression|UnaryExpression|ConditionalExpression"(path) {
        if (path.isUnaryExpression({operator: "+"}) || path.isUnaryExpression({operator: "void"})) {
            return;
        }

        const {confident, value} = path.evaluate();
        if (!confident || value === "Infinity") return;
        if (typeof value === "number" && isNaN(value)) return;

        path.replaceWith(types.valueToNode(value));
    }
};


// 调用插件,处理混淆的代码
traverse(ast, cons)

// 将处理后的ast转换为js代码(反混淆后的代码)
let {code} = generator(ast);
// 保存代码
fs.writeFile('decode.js', code, (err) => {
});