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

const restoreVarDeclarator = {

	VariableDeclarator(path)
	{
		let {node,scope} = path;
		let {id,init} = node;
		if (!types.isIdentifier(id) || init == null)
		{
			return;
		}
		let initPath = path.get("init");

		if (initPath.isUnaryExpression({operator:"+"}) ||
		    initPath.isUnaryExpression({operator:"-"}))
		{// -5或者 +"3" 也可以算作是字面量
			if (!types.isLiteral(init.argument))
			{
				return;
			}
		}

		else if (initPath.isIdentifier())
		{//全局属性可以还原。
			if (typeof astGlb[init.name] == 'undefined')
			{
				return;
			}
		}

		else if (initPath.isMemberExpression())
		{
			let name = init.object.name;
			if (typeof astGlb[name] == 'undefined' || name == 'window')
			{//注意object为window时，可能会还原出错
				return;
			}
		}

		else if (!initPath.isLiteral())
		{
			return;
		}

		const binding = scope.getBinding(id.name);

		if (!binding || !binding.constant) return;


		for (let referPath of binding.referencePaths)
		{
			referPath.replaceWith(init);
            console.log(id.name,init.value)
		}

		path.remove();

	},
}
traverse(ast, restoreVarDeclarator);

// 将处理后的ast转换为js代码(反混淆后的代码)
let {code} = generator(ast);
// 保存代码
fs.writeFile('decode.js', code, (err)=>{});