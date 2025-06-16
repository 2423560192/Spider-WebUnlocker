//AST核心组件的导入/加载

// fs模块 用于操作文件的读写
const fs = require("fs");
// @babel/parser 用于将JavaScript代码转换为ast树
const parser = require("@babel/parser");
// @babel/traverse 用于遍历各个节点的函数
const traverse = require("@babel/traverse").default;
// @babel/types 节点的类型判断及构造等操作
const types = require("@babel/types");
const {TYPES} = require("@babel/types");
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


let visitor = {
    MemberExpression(path) {
        let {node} = path
        name = node.property.name
        t_node = types.StringLiteral(name)
        node.property = t_node
        node.computed = true
    }
}

traverse(ast, visitor)

// 2.
// 2.
visitor_2 = {
    Identifier(path) {
        let {node} = path
        let name = node.name
        const RegExplArray = ['eval', 'parseInt', 'encodeURIComponent', 'Object', 'Function', 'Boolean', 'Number', 'Math', 'Date', 'String', 'Math.replaceWith'];

        if (RegExplArray.indexOf(name) != -1) {
            new_node = types.MemberExpression(types.Identifier("window"), types.stringLiteral(name), true)
            path.replaceWith(new_node)
        }


    }
}

traverse(ast, visitor_2)

// 3.
const visitor_3 = {
    NumericLiteral(path) {
        let {node} = path
        let value = node.value
        let key = parseInt(Math.random() * (999999 - 100000) + 100000, 10);
        let cripy_num = value ^ key
        path.replaceWith(types.binaryExpression(
            "^",
            types.numericLiteral(cripy_num),
            types.numericLiteral(key)
        ));
        path.skip();
    }
}

traverse(ast, visitor_3)


// 4.
function b64_encode(str) {
    return Buffer.from(str).toString("base64")
}

const visitor_4 = {
    StringLiteral(path) {
        let {node} = path;
        let value = node.value
        path.replaceWith(types.callExpression(
            types.identifier("atob"),
            [types.stringLiteral(b64_encode(value))]
        ))
        path.skip()
    }
}

traverse(ast, visitor_4)


// 5.
function b64_encode(str) {
    return Buffer.from(str).toString("base64")
}

var arry = []
const visitor_5 = {
    StringLiteral(path) {
        let {node} = path;
        let value = node.value
        let index = arry.indexOf(value)
        if (index == -1) {
            let length = arry.push(value)
            index = length - 1
        }
        // 构造节点
        path.replaceWith(types.memberExpression(
            types.identifier("arry"),
            types.numericLiteral(index),
            true
        ))
    }
}

traverse(ast, visitor_5)

console.log("乱序前：", arry, typeof arry)

// 数组乱序
// 6.
!(function (myArr, num) {
    // 定义一个函数用于循环右移数组元素
    var xiaojianbang = function (nums) {
        while (--nums) {
            myArr.unshift(myArr.pop()); // 将数组最后一个元素移到开头
        }
    };
    // 立即调用该函数，初始右移 16 次（0x10 是 16 的十六进制表示）
    xiaojianbang(num);

    // 返回修改后的数组
    return myArr;
})(arry, 0x10); // 传入 bigArr 数组和初始右移次数

console.log("乱序后：", arry)

// 还原代码
js_fonts = `(function(myArr, num) {
    // 定义混淆函数，将数组元素循环左移
    var xiaojianbang = function(nums) {
        while (--nums) {
            myArr.push(myArr.shift()); // 把数组第一个元素移到末尾
        }
    };
    
    // 立即调用混淆函数，初始左移 16 次（0x10 = 16）
    xiaojianbang(num);
    
    // 返回修改后的数组（虽然这里没有返回值，但函数内部已经修改了数组）
})(arry, 0x10); // 传入 arr 数组和初始移动次数 16`


ast2 = parser.parse(js_fonts)

ast.program.body.unshift(ast2.program.body[0])


bigArry = types.variableDeclarator(types.identifier("arry"), types.arrayExpression(arry.map(function (item) {
    return types.stringLiteral(item)
})))
bigArry = types.variableDeclaration("var", [bigArry])
// 把数组放到被混淆代码的AST最前面
ast.program.body.unshift(bigArry);

// 7.
function hexEnc(code) {
    for (var hexStr = [], i = 0, s; i < code.length; i++) {
        s = code.charCodeAt(i).toString(16);
        hexStr += "\\x" + s;
    }
    return hexStr;
}

const visitor_7 = {
    MemberExpression(path) {
        if (types.isIdentifier(path.node.property)) {
            path.node.property = types.stringLiteral(hexEnc(path.node.property.name))
        }
        path.node.computed = true
    }
}
traverse(ast, visitor_7)

// 9.

function generatorIdentifier(decNum) {
    let flag = ['0', 'o', '0'];
    let retval = [];
    while (decNum > 0) {
        retval.push(decNum % 3);
        decNum = parseInt(decNum / 3);
    }
    let Identifier = retval.reverse().map(function (v) {
        return flag[v]
    }).join('');
    Identifier.length < 6 ? (Identifier = ('OOOOOO' + Identifier).substr(-6)) :
        Identifier[0] == '0' && (Identifier = '0' + Identifier);
    return Identifier;
}

function renameOwnBinding(path) {
    let globalBinding = {}, ownbinding = {}, i = 0;
    path.traverse({
        Identifier(path) {
            let name = path.node.name
            let binding = path.scope.getOwnBinding(name)
            binding ? (ownbinding[name] = binding) : (globalBinding[name] = 1)
        }
    })
    for (oldName in ownbinding) {
        do {
            newName = generatorIdentifier(i++)
        } while (ownbinding[newName])
        ownbinding[oldName].scope.rename(oldName, newName)
    }
}

const visitor_8 = {
    'Program|FunctionExpression|FunctionDeclaration'(path) {
        renameOwnBinding(path);
    }
}
traverse(ast, visitor_8)


// 10.
const visitor_10 = {
    BinaryExpression(path) {
        let {node} = path
        let op = node.operator
        let left = node.left
        let right = node.right

        // 构建函数
        // 参数
        let a = types.identifier('a'), b = types.identifier("b")
        let newfuncName = path.scope.generateUidIdentifier("xxx")
        let func = types.functionDeclaration(
            newfuncName,
            [a, b],
            types.blockStatement(
                [types.returnStatement(
                    types.binaryExpression(op, a, b)
                )]
            )
        )
        // 替换
        path.replaceWith(
            types.callExpression(
                newfuncName,
                [left, right]
            )
        )
        let lastBlock = path.findParent(p => p.isBlockStatement())
        lastBlock.node.body.unshift(func)
    }
}
traverse(ast, visitor_10)


// 将处理后的ast转换为js代码(反混淆后的代码)
let {code} = generator(ast);

code = code.replace(/\\\\x/g, '\\x')


// 保存代码
fs.writeFile('decode.js', code, (err) => {
});