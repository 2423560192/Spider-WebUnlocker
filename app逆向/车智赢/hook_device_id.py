
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
    let SPUtils = Java.use("com.che168.autotradercloud.util.SPUtils");
    SPUtils["getDeviceId"].implementation = function () {
    console.log(`SPUtils.getDeviceId is called`);
    let result = this["getDeviceId"]();
    console.log(`SPUtils.getDeviceId result=${result}`);
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