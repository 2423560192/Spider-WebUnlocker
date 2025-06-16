(function(n, t) {
  console.log(n); // 5
  console.log(t); // 10

  var n = 20;  // 重新赋值给参数 n

  console.log(n); // 20
})(5, 10);
