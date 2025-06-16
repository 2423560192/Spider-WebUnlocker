

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

const deleteRepeatOfObject = {

    "VariableDeclarator"(path) {
        let { node, scope } = path;
        let { id, init } = node;

        if (!types.isObjectExpression(init)) {
            return;
        }

        let oldId = id;
        let name = id.name;

        const binding = scope.getBinding(name);
        if (!binding || !binding.constant) {
            return;
        }

        scope.traverse(scope.block, {
            VariableDeclarator(path) {
                let { node, scope } = path;
                let { id, init } = node;
                if (!types.isIdentifier(init, { name: name })) {
                    return;
                }

                const binding = scope.getBinding(id.name);

                if (!binding || !binding.constant)//如果被更改则不能进行替换
                    return;

                for (let referPath of binding.referencePaths) {
                    referPath.replaceWith(oldId);//使用replaceWith函数比rename函数更快。
                }
                path.remove();
                scope.crawl();
            },
        })
    },
}

traverse(ast,deleteRepeatOfObject);

const keyToLiteral = {
    MemberExpression:
    {
        exit({ node }) {
            const prop = node.property;
            if (!node.computed && !types.isArrayExpression(prop)) {
				node.property = types.stringLiteral(prop.name);
				node.computed = true;
            }
        }
    },
    // ObjectProperty:
    // {
    //     exit({ node }) {
    //         const key = node.key;
	//
    //         if (!node.computed && types.isIdentifier(key)) {
    //             node.key = types.StringLiteral(key.name);
    //             return;
    //         }
    //         if (node.computed && types.isStringLiteral(key)) {
    //             node.computed = false;
    //         }
    //     }
    // },
}

traverse(ast, keyToLiteral);

const preDecodeObject = {
    VariableDeclarator({ node, parentPath, scope }) {
        const { id, init } = node;
        if (!types.isObjectExpression(init)) return;
        let name = id.name;

        let properties = init.properties;
        let allNextSiblings = parentPath.getAllNextSiblings();
        for (let nextSibling of allNextSiblings) {
            if (!nextSibling.isExpressionStatement()) break;

            let expression = nextSibling.get('expression');
            if (!expression.isAssignmentExpression({ operator: "=" })) break;

            let { left, right } = expression.node;
            if (!types.isMemberExpression(left)) break;

            let { object, property } = left;
            if (!types.isIdentifier(object, { name: name }) ||
                !types.isStringLiteral(property)) {
                break;
            }

            properties.push(types.ObjectProperty(property, right));
            nextSibling.remove();
        }
        scope.crawl();
    },
}

traverse(ast,preDecodeObject);




// 将处理后的ast转换为js代码(反混淆后的代码)
let {code} = generator(ast);
// 保存代码
fs.writeFile('decode.js', code, (err)=>{});