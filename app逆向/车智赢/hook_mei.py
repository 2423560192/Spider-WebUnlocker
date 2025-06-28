
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
    let AppUtils = Java.use("com.che168.autotradercloud.util.AppUtils");
AppUtils["getIMEI"].implementation = function (ctx) {
    console.log(`AppUtils.getIMEI is called: null=${ctx}`);
    let result = this["getIMEI"](null);
    console.log(`AppUtils.getIMEI result=${result}`);
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