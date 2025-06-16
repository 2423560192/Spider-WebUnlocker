const files = require('fs');
const types = require("@babel/types");
const parser = require("@babel/parser");
const traverse = require("@babel/traverse").default;
const generator = require("@babel/generator").default;
const template = require("@babel/template");

//js混淆代码读取
let encodeFile = process.argv.length > 2 ? process.argv[2] : "./step1.js";
let decodeFile = process.argv.length > 3 ? process.argv[3] : encodeFile.replace(".js", "_ok.js")

//将源代码解析为AST
let sourceCode = files.readFileSync(encodeFile, { encoding: "utf-8" });
let ast = parser.parse(sourceCode);

//以下代码勿动。。。

let decryptCode = files.readFileSync("decodeFunc.js", { encoding: "utf-8" });
if (decryptCode.length == 0 || !decryptCode.includes("function")) {


  console.log("\n请抠出解密函数至 decodeFunc.js文件后再次运行！\n");

  process.exit(1);

}

console.time("处理完毕，耗时");


//判断节点是否为字面量，插件地址 https://t.zsxq.com/09CvEE1FY
function isNodeLiteral(node) {
  if (Array.isArray(node)) {
    return node.every(ele => isNodeLiteral(ele));
  }

  if (types.isThisExpression(node)) {
    return true;
  }

  if (types.isLiteral(node)) {
    if (node.value == null) {
      return false;
    }
    return true;
  }
  if (types.isBinaryExpression(node)) {
    return isNodeLiteral(node.left) && isNodeLiteral(node.right);
  }
  if (types.isUnaryExpression(node, {
    "operator": "-"
  }) || types.isUnaryExpression(node, {
    "operator": "+"
  })) {
    return isNodeLiteral(node.argument);
  }

  if (types.isObjectExpression(node)) {
    let { properties } = node;
    if (properties.length == 0) {
      return true;
    }

    return properties.every(property => isNodeLiteral(property));

  }
  if (types.isArrayExpression(node)) {
    let { elements } = node;
    if (elements.length == 0) {
      return true;
    }
    return elements.every(element => isNodeLiteral(element));
  }

  return false;
}


function getDecryptFuncNames(decryptCode) {
  let funcNames = [];

  let decryptAst = parser.parse(decryptCode);

  traverse(decryptAst, {
    "FunctionDeclaration"(path) {
      let { parentPath, node } = path;
      if (!parentPath.isProgram()) {
        return;//非全局函数不作处理
      }

      let { id, params, body } = node;
      let length = body.body.length;
      if (params.length == 0 || length == 0 || !types.isReturnStatement(body.body[length - 1])) {
        return;
      }

      funcNames.push(id.name);
    },
  });

  return funcNames;
}


let funcNames = getDecryptFuncNames(decryptCode); //自动获取解密函数名




const collectAllSimplieFunc =
{
  FunctionDeclaration(path) {
    let name = path.node.id.name;

    if (!funcNames.includes(name)) {
      return;
    }

    let scope = path.parentPath.scope;

    scope.traverse(scope.block, {//在scope内收集符合ob混淆特征的解密函数
      "FunctionDeclaration"(path) {
        let { id, body, params } = path.node;
        if (params.length < 2) {
          return;
        }
        body = body.body;
        if (!body || body.length != 1 ||
          !types.isReturnStatement(body[0])) {
          return;
        }
        let argument = body[0].argument;
        if (!types.isCallExpression(argument) ||
          !types.isIdentifier(argument.callee)) {
          return;
        }
        decryptCode += path.toString();
        funcNames.push(id.name);
      },
    })
  },
}

traverse(ast, collectAllSimplieFunc);


let evalAst = parser.parse(decryptCode);

decryptCode = generator(evalAst, opts = { compact: true }).code;

eval(decryptCode);


let removeFlag = false;

function calcCallExpression(name, path) {
  let { scope, node } = path;

  if (!funcNames.includes(name)) {
    return;
  }

  let binding = undefined;
  if (path.isVariableDeclarator()) {
    binding = scope.getBinding(node.id.name);
    if (!binding || binding.constantViolations.length > 1) {
      return;
    }

    if (binding.constantViolations.length == 1 && binding.constantViolations[0] != path) {
      return;
    }
  }
  else if (path.isAssignmentExpression() && path.get('left').isIdentifier()) {
    binding = scope.getBinding(node.left.name);
    if (!binding || binding.constantViolations.length != 1) {
      return;
    }
  }

  if (!binding) return;

  for (let referPath of binding.referencePaths) {

    let { parentPath, node } = referPath;

    if (parentPath.isVariableDeclarator({ "init": node }) || parentPath.isAssignmentExpression({ "right": node })) {
      calcCallExpression(name, parentPath);
    }

    if (!parentPath.isCallExpression({ "callee": node })) {
      continue;
    }

    let { arguments } = parentPath.node;

    if (arguments.length == 0 || !isNodeLiteral(arguments)) {
      continue;
    }

    parentPath.node.callee.name = name;
    let value = eval(parentPath.toString());
    console.log(parentPath.toString(), "--->", value);
    parentPath.replaceWith(types.valueToNode(value));
    removeFlag = true;
  }

}


const callToString = {

  FunctionDeclaration(path) {
    let name = path.node.id.name;

    if (!funcNames.includes(name)) {
      return;
    }

    let scope = path.parentPath.scope;
    let binding = scope.getBinding(name);

    for (let referPath of binding.referencePaths) {

      if (path.isAncestor(referPath)) {
        continue;
      }

      let { parentPath, node } = referPath;

      if (parentPath.isVariableDeclarator({ "init": node }) || parentPath.isAssignmentExpression({ "right": node })) {
        calcCallExpression(name, parentPath);
        continue;
      }

      if (!parentPath.isCallExpression({ "callee": node })) {
        continue;
      }

      let { arguments } = parentPath.node;

      if (arguments.length == 0 || !isNodeLiteral(arguments)) {
        continue;
      }
      let value = eval(parentPath.toString());
      console.log(parentPath.toString(), "--->", value);
      parentPath.replaceWith(types.valueToNode(value));
    }
  },
}

traverse(ast, callToString);


if (removeFlag) {
  const removeRepeatFunc =
  {
    VariableDeclarator(path) {
      let { scope, node } = path;
      let { id, init } = node;
      if (!types.isIdentifier(init)) {
        return;
      }
      let binding = scope.getBinding(node.id.name);
      if (!binding || binding.constantViolations.length > 1) {

        return;
      }

      if (binding.constantViolations.length == 1 && binding.constantViolations[0] != path) {
        return;
      }

      if (!binding.referenced) {
        console.log(path.toString());
        path.remove();
        traverseFlag = true;
      }
    },
    AssignmentExpression(path) {
      let { scope, node, parentPath } = path;
      let { left, operator, right } = node;
      if (!types.isIdentifier(left) || operator != "=" ||
        !types.isIdentifier(right)) {
        return;
      }
      let binding = scope.getBinding(left.name);
      if (!binding || binding.constantViolations.length != 1) {
        return;
      }
      if (!binding.referenced) {
        if (parentPath.isExpressionStatement() || parentPath.isSequenceExpression()) {
          console.log(path.toString());
          path.remove();
          traverseFlag = true;
        }
      }

    },
  }

  do {
    var traverseFlag = false;
    ast = parser.parse(generator(ast).code);
    traverse(ast, removeRepeatFunc);
  } while (traverseFlag);

}



const removeDeadFunctionDeclaration =
{
  FunctionDeclaration(path) {
    let { parentPath, node } = path;
    let name = node.id.name;

    if (!funcNames.includes(name)) {
      return;
    }

    let binding = parentPath.scope.getBinding(node.id.name);
    if (!binding) return;

    let isReferenced = false;
    for (let referPath of binding.referencePaths) {
      if (!path.isAncestor(referPath)) {
        isReferenced = true;
        break;
      }
    }

    if (!isReferenced) {
      console.log(path.toString());
      path.remove();
      traverseFlag = true;
    }
  }
}

do {
  var traverseFlag = false;
  ast = parser.parse(generator(ast).code);
  traverse(ast, removeDeadFunctionDeclaration);
} while (traverseFlag);


const constantFold = {
  "BinaryExpression|UnaryExpression"(path) {
    if (path.isUnaryExpression({ operator: "-" }) ||
      path.isUnaryExpression({ operator: "void" })) {
      return;
    }
    const { confident, value } = path.evaluate();
    if (!confident)
      return;
    if (typeof value == 'number' && (!Number.isFinite(value))) {
      return;
    }
    path.replaceWith(types.valueToNode(value));
  },
}

traverse(ast, constantFold);



console.timeEnd("处理完毕，耗时");


let { code } = generator(ast, opts = {
  "compact": false,  // 是否压缩代码
  "comments": false,  // 是否保留注释
});

files.writeFile(decodeFile, code, (err) => { });