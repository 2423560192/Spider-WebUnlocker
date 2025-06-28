
# 不会重启应用，直接hook进去
import frida
import sys
# 连接手机设备
rdev = frida.get_remote_device()

# 包名：com.che168.autotradercloud
# 车智赢+
session = rdev.attach("车智赢+")
scr = """
Java.perform(function () {
    let SignManager = Java.use("com.che168.atclibrary.base.SignManager");
    SignManager["signByType"].implementation = function (signType, paramMap) {
    console.log(`SignManager.signByType is called: signType=${signType}, paramMap=${paramMap}`);
    let result = this["signByType"](signType, paramMap);
    console.log(`SignManager.signByType result=${result}`);
    return result;
};
});
"""

script = session.create_script(scr)

def on_message(message, data):
    print(message, data)

script.on("message", on_message)
script.load()
sys.stdin.read()