# 写hook脚本
import frida
import sys

rdev = frida.get_remote_device()
session = rdev.attach("爱安丘")
scr = """
Java.perform(function () {
    var EncryptUtil = Java.use("com.iqilu.core.util.EncryptUtil");
    EncryptUtil.getMD5.implementation = function(str){
        console.log("参数是：",str);
        var res = this.getMD5(str);
        console.log("返回值：",res);
        return res
    }
});
"""
script = session.create_script(scr)


def on_message(message, data):
    print(message, data)


script.on("message", on_message)
script.load()
sys.stdin.read()
