var arry = ["5pel", "5LiA", "5LqM", "5LiJ", "5Zub", "5LqU", "5YWt", "cmVwbGFjZQ==", "Z2V0RnVsbFllYXI=", "Z2V0TW9udGg=", "dG9TdHJpbmc=", "MA==", "Z2V0RGF0ZQ==", "bG9n", "eXl5eS1NTS1kZA==", "RGF0ZQ==", "cHJvdG90eXBl", "Zm9ybWF0"];
(function (myArr, num) {
  // 定义混淆函数，将数组元素循环左移
  var xiaojianbang = function (nums) {
    while (--nums) {
      myArr.push(myArr.shift()); // 把数组第一个元素移到末尾
    }
  };

  // 立即调用混淆函数，初始左移 16 次（0x10 = 16）
  xiaojianbang(num);

  // 返回修改后的数组（虽然这里没有返回值，但函数内部已经修改了数组）
})(arry, 0x10); // 传入 arr 数组和初始移动次数 16
window[atob(arry[0])][atob(arry[1])][atob(arry[2])] = function (formatStr) {
  var str = formatStr;
  var Week = [atob(arry[3]), atob(arry[4]), atob(arry[5]), atob(arry[6]), atob(arry[7]), atob(arry[8]), atob(arry[9])];
  str = str[atob(arry[10])](/yyyy|YYYY/, this[atob(arry[11])]());
  str = str[atob(arry[10])](/MM/, this[atob(arry[12])]() + (588917 ^ 588916) > (652812 ^ 652805) ? (this[atob(arry[12])]() + (792441 ^ 792440))[atob(arry[13])]() : atob(arry[14]) + (this[atob(arry[12])]() + (225132 ^ 225133)));
  str = str[atob(arry[10])](/dd|DD/, this[atob(arry[15])]() > (389064 ^ 389057) ? this[atob(arry[15])]()[atob(arry[13])]() : atob(arry[14]) + this[atob(arry[15])]());
  return str;
};
console[atob(arry[16])](new window[atob(arry[0])]()[atob(arry[2])](atob(arry[17])));
// 按代码逻辑，若当前环境模拟输出场景，会输出类似 2020-07-19 （实际随系统时间变化 ）