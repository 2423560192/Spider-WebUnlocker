/****************************************************************
变量定义还原，当变量定义为字面量或者Identifier，
并且变量值没有被更改时，可进行还原。
var a = 123;
const b = -5;
let c = window;
function d()
{
  var f = c.btoa("hello,AST!");
	return a + b + f ;
}
===>
function d() {
  var f = window.btoa("hello,AST!");
  return 123 + -5 + f;
}

注:该插件在浏览器上运行效果更佳。

***************************************************************/


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


let astGlb = typeof window != 'undefined'? window : global;

const simplifyLiteral = {//还原十六进制数字或字符串及Unicode
	NumericLiteral({node}) {
		if (node.extra && /^0[obx]/i.test(node.extra.raw)) {
			node.extra = undefined;
		}
  },
  StringLiteral({node})
  {
  	if (node.extra && /\\[ux]/gi.test(node.extra.raw)) {
  		node.extra = undefined;
    }
  },
}


traverse(ast,simplifyLiteral);


const keyToLiteral = {//将所有的key值字符串化，方便统一处理。
   MemberExpression:
   {
      exit({node})
      {
         const prop = node.property;
         if (!node.computed && types.isIdentifier(prop))
         {
            node.property = types.StringLiteral(prop.name);
            node.computed = true;
         }
    }
  },
  ObjectProperty:
  {
      exit({node})
      {
         const key = node.key;
         if (!node.computed && types.isIdentifier(key))
         {
            node.key = types.StringLiteral(key.name);
         }
      }
   },
}

traverse(ast, keyToLiteral);



function isBaseLiteral(node) {
    if (types.isLiteral(node)) {
        return true;
    }
    if (types.isUnaryExpression(node, {operator: "-"}) ||
        types.isUnaryExpression(node, {operator: "+"})) {
        return isBaseLiteral(node.argument);
    }

    return false;
}


const decodeValueOfObject =
{                               //当一个object里面的value全部为字面量时的还原，没有考虑单个key重新赋值的情况。
    VariableDeclarator(path) {
        let { node, scope } = path;
        const { id, init } = node;
        if (!types.isObjectExpression(init)) return;

        let properties = init.properties;

        if (properties.length == 0 || !properties.every(property => isBaseLiteral(property.value)))
            return;

        let binding = scope.getBinding(id.name);

        let { constant, referencePaths } = binding;
        if (!constant) return;

        let newMap = new Map();
        for (const property of properties) {
            let { key, value } = property;
            newMap.set(key.value, value);
        }

        let canBeRemoved = true;
        // 遍历该对象的所有引用
        for (const referPath of referencePaths) {
            // referPath是obj ， 那么parentPath就是obj.a整个
            let { parentPath } = referPath;
            if (!parentPath.isMemberExpression()) {
                canBeRemoved = false;
                return;
            }

            let AncestorPath = parentPath.parentPath;

            if (AncestorPath.isAssignmentExpression({"left":parentPath.node}))
            {
            	  canBeRemoved = false;
                return;
            }
            if (AncestorPath.isUpdateExpression() && ['++','--'].includes(AncestorPath.node.operator))
            {
            	  canBeRemoved = false;
                return;
            }

            let curKey = parentPath.node.property.value;

            if (!newMap.has(curKey)) {
                canBeRemoved = false;
                break;
            }

            // 替换新值
            parentPath.replaceWith(newMap.get(curKey));
        }
        canBeRemoved && path.remove();
        newMap.clear();
    },
}


traverse(ast, decodeValueOfObject);


// 将处理后的ast转换为js代码(反混淆后的代码)
let {code} = generator(ast);
// 保存代码
fs.writeFile('decode.js', code, (err)=>{});