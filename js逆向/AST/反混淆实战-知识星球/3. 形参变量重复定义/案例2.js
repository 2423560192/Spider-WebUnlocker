

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

//
// function getRandomName(length) {
//
// 	let initArr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'];
// 	let puzzleArr = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];
// 	let ranInx = Math.floor(Math.random() * initArr.length);
// 	let randomName = initArr[ranInx];
//
// 	for (var i = 1; i < length; i++) {
// 		ranInx = Math.floor(Math.random() * puzzleArr.length);
// 		randomName += puzzleArr[ranInx];
// 	}
//
// 	return randomName;
// }
//
//
// let allNewNames = new Map();  //定义一个全局变量，保存需要处理的函数
//
// function getUnusedIdentifier() {//获取未被使用的名称,返回 Identifier 类型。
// 	do {
// 		var newName = "$CJ_" + getRandomName(3);
//
// 	} while (allNewNames.has(newName))
//
// 	return newName;
//
// }
//
//
// let paramsList = ['n', 't', 'r', 'e', 'a', 'u', 'c' , 'p'];
//
// const renameSameNameOfParams =
// {
// 	VariableDeclarator(path) {
// 		let { scope, node } = path;
// 		let { id, init } = node;
//
// 		if (!paramsList.includes(id.name)) {
// 			return;
// 		}
//
// 		const binding = scope.getBinding(id.name);
//
// 		if (!binding) {
// 			return;
// 		}
//
// 		let newName = getUnusedIdentifier();
//
// 		allNewNames.set(newName, id.name);
//
// 		scope.rename(id.name, newName);
//
// 		id.name = newName;
//
// 		scope.crawl();
//
// 	}
// }
//
//
//
//
//
// traverse(ast, renameSameNameOfParams);


// 删除重复定义且未被改变初始值的变量
const deleteRepeatDefine = {
	"VariableDeclarator"(path) {
		let { node, scope } = path;
		let { id, init } = node;
		if (!types.isIdentifier(init) || !paramsList.includes(init.name)) {
			return;
		}

		const binding = scope.getBinding(id.name);

		if (!binding || !binding.constant) return;


		for (let referPath of binding.referencePaths) {
			referPath.replaceWith(init);
		}

		path.remove();//没有被引用，或者替换完成，可直接删除


	},

}

traverse(ast, deleteRepeatDefine);



// 将处理后的ast转换为js代码(反混淆后的代码)
let {code} = generator(ast);
// 保存代码
fs.writeFile('decode.js', code, (err)=>{});