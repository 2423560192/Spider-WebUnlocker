
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
    let SecurityUtil = Java.use("com.autohome.ahkit.utils.SecurityUtil");
SecurityUtil["encode3Des"].implementation = function (context, str) {
    console.log(`SecurityUtil.encode3Des is called: context=${context}, str=${str}`);
    let result = this["encode3Des"](context, str);
    console.log(`SecurityUtil.encode3Des result=${result}`);
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