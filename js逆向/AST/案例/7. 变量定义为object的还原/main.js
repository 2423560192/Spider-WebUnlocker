const fs            = require('fs');
const types         = require("@babel/types");
const parser        = require("@babel/parser");
const traverse      = require("@babel/traverse").default;
const generator     = require("@babel/generator").default;


//js混淆代码读取
process.argv.length > 2 ? encodeFile = process.argv[2]: encodeFile ="./encode.js";
process.argv.length > 3 ? decodeFile = process.argv[3]: decodeFile ="./decodeResult.js";

//将源代码解析为AST
let sourceCode = fs.readFileSync(encodeFile, {encoding: "utf-8"});

let ast    = parser.parse(sourceCode);


console.time("处理完毕，耗时");



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
		}
		
		path.remove();
		
	},
}

traverse(ast, restoreVarDeclarator);




console.timeEnd("处理完毕，耗时");


let {code} = generator(ast,opts = {jsescOption:{"minimal":true}});

fs.writeFile(decodeFile, code, (err) => {});