const files = require('fs');  //导入文件库，防止与fs变量名冲突
const types = require("@babel/types");
const parser = require("@babel/parser");
const template = require("@babel/template").default;
const traverse = require("@babel/traverse").default;
const generator = require("@babel/generator").default;
const NodePath = require("@babel/traverse").NodePath; //智能提示所需

//js混淆代码读取
const encodeFile = process.argv.length > 2 ? process.argv[2] : "./encode.js";  //默认的js文件
const decodeFile = process.argv.length > 3 ? process.argv[3] : encodeFile.slice(0, encodeFile.length - 3) + "ok.js";


//将源代码解析为AST
let sourceCode = files.readFileSync(encodeFile, { encoding: "utf-8" });
let ast = parser.parse(sourceCode);
console.time("处理完毕，耗时");



const DeclaratorToDeclaration =
{
	VariableDeclaration(path) {
		let { parentPath, node } = path;
		if (parentPath.isFor()) {
			return;
		}
		let { declarations, kind } = node;

		if (declarations.length == 1) {
			return;
		}

		let newNodes = [];

		for (const varNode of declarations) {
			let newDeclartionNode = types.VariableDeclaration(kind, [varNode]);
			newNodes.push(newDeclartionNode);
		}

		path.replaceWithMultiple(newNodes);

	},
}

traverse(ast, DeclaratorToDeclaration);



ast = parser.parse(generator(ast).code);





function getNextSiblingType(nextSibling, constantViolations, referencePaths) {
	let nextSiblingType = 0;

	for (let constVioPath of constantViolations) {
		if (nextSibling.isAncestor(constVioPath)) {
			nextSiblingType |= 1;
			break;
		}
	}
	for (let referPath of referencePaths) {
		if (nextSibling.isAncestor(referPath) || nextSibling == referPath) {
			nextSiblingType |= 2;
			break;
		}
	}

	return nextSiblingType;

}



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
		let { object, property } = node;

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

	if (types.isUnaryExpression(node) && node.operator != "void") {
		return isExpressionConstant(node.argument);
	}

	return false;
}



let VARNODE = template("var A = B;");

const restoreSpVarDeclarator =
{
	/**  @param  {NodePath} path */
	VariableDeclarator(path) {

		let { scope, node, parentPath } = path;
		let { id, init } = node;

		if (!types.isIdentifier(id) || init == null || !isExpressionConstant(init)) {
			return;
		}

		const binding = scope.getBinding(id.name);

		if (!binding) return;

		let { constant, referencePaths, constantViolations } = binding;

		let allNextSiblings = parentPath.getAllNextSiblings();

		if (allNextSiblings.length == 0) {
			return;
		}

		console.log(path.toString())

		for (let nextSibling of allNextSiblings) {

			let nextSiblingType = getNextSiblingType(nextSibling, constantViolations, referencePaths);

			if (nextSiblingType == 0) {
				continue;
			}

			if (nextSiblingType == 1) {
				if (nextSibling.isExpressionStatement() && nextSibling.get('expression').isAssignmentExpression()) {
					let { left, operator, right } = nextSibling.get('expression').node;
					if (types.isIdentifier(left, { "name": id.name }) && operator == "=") {
						let newNode = VARNODE({ "A": left, "B": right });
						nextSibling.replaceWith(newNode);
						path.remove();
						break;
					}
				}
				if (nextSibling.isVariableDeclaration())
				{
					path.remove();
				}
				break;
			}

			if (nextSiblingType == 2) {
				for (let referPath of referencePaths) {
					if (nextSibling.isAncestor(referPath)) {
						referPath.replaceWith(init);
					}
				}
				continue;
			}

			if (nextSiblingType == 3) {
				if (nextSibling.isExpressionStatement() && nextSibling.get('expression').isAssignmentExpression()) {
					let { left, operator, right } = nextSibling.get('expression').node;
					if (types.isIdentifier(left, { "name": id.name }) && operator == "=") {
						for (let referPath of referencePaths) {
							if (nextSibling.isAncestor(referPath)) {
								referPath.replaceWith(init);
							}
						}
						let newNode = VARNODE({ "A": left, "B": nextSibling.get('expression.right').node });
						nextSibling.replaceWith(newNode);
						path.remove();
					}
				}
				if (nextSibling.isVariableDeclaration()) {

					let initPath = nextSibling.get('declarations.0.init');

					for (let referPath of referencePaths) {
						if (initPath.isAncestor(referPath)) {
							referPath.replaceWith(init);
						}
					}
					path.remove();
				}
				break;
			}
		}
	},
}

traverse(ast, restoreSpVarDeclarator);


console.timeEnd("处理完毕，耗时");
let { code } = generator(ast, opts = {
	"compact": false,  // 是否压缩代码
	"comments": false,  // 是否保留注释
	"jsescOption": { "minimal": true },  //Unicode转义
});

files.writeFile(decodeFile, code, (err) => { });