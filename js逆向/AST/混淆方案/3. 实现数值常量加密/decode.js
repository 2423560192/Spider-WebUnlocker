window["Date"]["prototype"]["format"] = function (formatStr) {
  var str = formatStr;
  var Week = ['日', '一', '二', '三', '四', '五', '六'];
  str = str["replace"](/yyyy|YYYY/, this["getFullYear"]());
  str = str["replace"](/MM/, this["getMonth"]() + (708986 ^ 708987) > (105459 ^ 105466) ? (this["getMonth"]() + (740651 ^ 740650))["toString"]() : '0' + (this["getMonth"]() + (356854 ^ 356855)));
  str = str["replace"](/dd|DD/, this["getDate"]() > (892976 ^ 892985) ? this["getDate"]()["toString"]() : '0' + this["getDate"]());
  return str;
};
console["log"](new window["Date"]()["format"]('yyyy-MM-dd'));
// 按代码逻辑，若当前环境模拟输出场景，会输出类似 2020-07-19 （实际随系统时间变化 ）