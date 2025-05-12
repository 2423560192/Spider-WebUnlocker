
import itchat
import queue
import threading

class Wchat:
    def __init__(self):
        self.msg_queue = queue.Queue()  # 消息队列，用于存储接收到的消息
        # 启动消息监听
        itchat.msg_register('Text', isGroupChat=True)(self.monitor_chatroom_content)

    def monitor_chatroom_content(self, msg):
        # if msg['User']['NickName'] == '测试':  # 替换为实际群聊名称
            # print(f"[{msg['ActualNickName']}] {msg['Content']}")  # 打印消息内容
            # 将消息放入队列
        self.msg_queue.put(msg)

    def listen_msg(self):
        itchat.auto_login(hotReload=True)
        itchat.run()  # 启动消息监听

    def get_msg(self):
        # 阻塞式获取队列中的消息
        return self.msg_queue.get()  # 从队列中获取消息



