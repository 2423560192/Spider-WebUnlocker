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


function isBaseLiteral(node) {

    let literalList = ['window', 'document', 'navigator', 'location', 'history', 'screen',];

    if (types.isLiteral(node) && node.value != null) {//null可能有坑
        return true;
    }

    if (types.isIdentifier(node) && literalList.includes(node.name)) {
        return true;
    }

    if (types.isIdentifier(node) && typeof globalThis[node.name] != "undefined") {
        return true;
    }

    if (types.isUnaryExpression(node) && ["+", "-", "!"].includes(node.operator)) {
        return isBaseLiteral(node.argument);
    }

    return false;
}

const decodeObjectofValue =
    {
        VariableDeclarator(path) {
            let {node, scope} = path;

            const {id, init} = node;

            if (!types.isObjectExpression(init)) return;

            let properties = init.properties;

            if (properties.length == 0)
                return;

            let binding = scope.getBinding(id.name);

            if (!binding) return;

            let {constant, referencePaths, constantViolations} = binding;

            if (!constant) {//新版本的babel库，在循环里面的变量定义，默认非常量
                if (constantViolations.length != 1 || constantViolations[0] != path) //旧版本屏蔽该行即可
                {
                    return;
                }
            }

            let newMap = new Map();

            for (const property of properties) {
                let {key, value} = property;

                if (!isBaseLiteral(value)){
                    continue
                }

                let KeyName = types.isIdentifier(key) ? key.name : key.value;

                if (!KeyName || KeyName.length != 5) {
                    //  continue; //仅针对ob混淆
                }
                newMap.set(KeyName, value);
            }

            let canBeRemoved = true;

            for (const referPath of referencePaths) {

                let {parentPath} = referPath;

                if (!parentPath.isMemberExpression()) {
                    canBeRemoved = false;
                    break;
                }

                let AncestorPath = parentPath.parentPath;

                if (AncestorPath.isAssignmentExpression({"left": parentPath.node})) {
                    canBeRemoved = false;
                    break;
                }
                if (AncestorPath.isUpdateExpression() && ['++', '--'].includes(AncestorPath.node.operator)) {
                    canBeRemoved = false;
                    break;
                }

                let {property} = parentPath.node;


                let curKey = types.isIdentifier(property) ? property.name : property.value;

                if (!newMap.has(curKey)) {
                    canBeRemoved = false;
                    continue;
                }

                parentPath.replaceWith(newMap.get(curKey));
            }

            canBeRemoved && path.remove();

            newMap.clear();
        },
    }

traverse(ast, decodeObjectofValue);


// 将处理后的ast转换为js代码(反混淆后的代码)
let {code} = generator(ast);
// 保存代码
fs.writeFile('decode.js', code, (err) => {
});