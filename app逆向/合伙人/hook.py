import frida
import sys
# 连接手机设备
rdev = frida.get_remote_device()

# 包名：com.che168.autotradercloud
# 车智赢+
session = rdev.attach("油联合伙人")
scr = """
Java.perform(function () {
    //找到类 反编译的首行+类名：com.autohome.ahkit.utils下的
    var SecurityUtil = Java.use("com.yltx.oil.partner.utils.Md5");

    //替换类中的方法
    SecurityUtil.md5.implementation = function(str){
        console.log("参数：",str);
        str = '123456'
        var res = this.md5(str); //调用原来的函数
        console.log("返回值：",res);
        return str;
    }
});
"""

script = session.create_script(scr)

def on_message(message, data):
    print(message, data)

script.on("message", on_message)
script.load()
sys.stdin.read()