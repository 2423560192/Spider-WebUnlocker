import gzip
import logging
import re
import ssl
import traceback

import execjs
import requests
import websocket

from CoreUtils.Encrypt import md5_encrypt
from douyin.douyin_pb2 import PushFrame, Message, Response, ChatMessage, GiftMessage, LikeMessage, MemberMessage, \
    SocialMessage, RoomUserSeqMessage, FansclubMessage, EmojiChatMessage, RoomMessage, RoomStatsMessage, \
    RoomRankMessage, ControlMessage, RoomStreamAdaptationMessage

import logging

# ========== 日志配置 ==========
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


class DouYinLive:
    def __init__(self, room_uid):
        self.headers = {
            "user-agent": "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
        }
        self.cookies = {
            "__ac_nonce": "0683ab03200786e902e82"
        }
        self.url = f"https://live.douyin.com/{room_uid}"
        self.ws = ''

    def start(self):
        room_id, ttwid = self.get_room_id()
        # 获取sign
        sign = self.get_sign(room_id)
        # 发起websocket请求
        self.send_websocket(room_id, sign, ttwid)

    def get_room_id(self):
        """获取room_id"""

        response = requests.get(self.url, headers=self.headers, cookies=self.cookies)

        data = response.text
        room_id = str(re.search(r'\\"roomId\\":\\"(\d+)\\"', data).group(1))
        logging.info(f"房间id：{room_id}")
        ttwid = response.cookies.get('ttwid')

        return room_id, ttwid

    def get_s(self, room_id):
        """获取s值"""
        param = {
            "app_name": "douyin_web",
            "version_code": "180800",
            "webcast_sdk_version": "1.0.14-beta.0",
            "update_version_code": "1.0.14-beta.0",
            "compress": "gzip",
            "device_platform": "web",
            "cookie_enabled": 'true',
            "screen_width": 1920,
            "screen_height": 1080,
            "browser_language": "zh-CN",
            "browser_platform": "Win32",
            "browser_name": "Mozilla",
            "browser_version": "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "browser_online": 'true',
            "tz_name": "Asia/Shanghai",
            "cursor": "t-1748834041134_r-7511185012226569781_d-7511185012226523137_u-1_fh-7511184045972533541",
            "internal_ext": "internal_src:dim|wss_push_room_id:7511169016510040832|wss_push_did:7506916920386848296|first_req_ms:1748834041041|fetch_time:1748834041134|seq:1|wss_info:0-1748834041134-0-0|wrds_v:7511184999341623742",
            "host": "https://live.douyin.com",
            "aid": "6383",
            "live_id": 1,
            "did_rule": 3,
            "endpoint": "live_pc",
            "support_wrds": 1,
            "user_unique_id": "7506916920386848296",
            "im_path": "/webcast/im/fetch/",
            "identity": "audience",
            "need_persist_msg_count": "15",
            "insert_task_id": "",
            "live_reason": "",
            "room_id": room_id,
            "heartbeatDuration": "0"
        }
        # 顺序
        order = [
            {
                "param_name": "live_id",
                "param_type": "string"
            },
            {
                "param_name": "aid",
                "param_type": "string"
            },
            {
                "param_name": "version_code",
                "param_type": "string"
            },
            {
                "param_name": "webcast_sdk_version",
                "param_type": "string"
            },
            {
                "param_name": "room_id",
                "param_type": "string"
            },
            {
                "param_name": "sub_room_id",
                "param_type": "string"
            },
            {
                "param_name": "sub_channel_id",
                "param_type": "string"
            },
            {
                "param_name": "did_rule",
                "param_type": "string"
            },
            {
                "param_name": "user_unique_id",
                "param_type": "string"
            },
            {
                "param_name": "device_platform",
                "param_type": "string"
            },
            {
                "param_name": "device_type",
                "param_type": "string"
            },
            {
                "param_name": "ac",
                "param_type": "string"
            },
            {
                "param_name": "identity",
                "param_type": "string"
            }
        ]

        pre_s = ''

        for i in order:
            try:
                param_name = i['param_name']
                value = param[param_name]
                pre_s += ',' + str(param_name) + '=' + str(value)
            except:
                param_name = i['param_name']
                pre_s += ',' + str(param_name) + '=' + ''
        s = md5_encrypt(pre_s[1:])

        return s

    def get_sign(self, room_id):
        """获取sign值"""
        # 获取s值
        s = self.get_s(room_id)

        # 获取sign值
        sign = execjs.compile(
            open(r'D:\projects\Spider-WebUnlocker\js逆向\项目\抖音弹幕—直播间\sign.js', encoding='utf-8').read()).call(
            'get_sign', s)

        return sign

    def send_websocket(self, room_id, sign, ttwid):
        """发起请求"""

        cookie = f"ttwid={ttwid}"
        # WebSocket 服务器地址
        ws_url = f"wss://webcast100-ws-web-lq.douyin.com/webcast/im/push/v2/?app_name=douyin_web&version_code=180800&webcast_sdk_version=1.0.14-beta.0&update_version_code=1.0.14-beta.0&compress=gzip&device_platform=web&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Mozilla&browser_version=5.0%20(Windows%20NT%2010.0;%20Win64;%20x64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/137.0.0.0%20Safari/537.36&browser_online=true&tz_name=Asia/Shanghai&cursor=u-1_fh-7511183563078362663_t-1748833761054_r-7511183809635723460_d-7511183805340712963&internal_ext=internal_src:dim|wss_push_room_id:7511169016510040832|wss_push_did:7506916920386848296|first_req_ms:1748833760959|fetch_time:1748833761054|seq:1|wss_info:0-1748833761054-0-0|wrds_v:7511183805340715817&host=https://live.douyin.com&aid=6383&live_id=1&did_rule=3&endpoint=live_pc&support_wrds=1&user_unique_id=7506916920386848296&im_path=/webcast/im/fetch/&identity=audience&need_persist_msg_count=15&insert_task_id=&live_reason=&room_id={room_id}&heartbeatDuration=0&signature={sign}"
        # 创建 WebSocket 连接
        self.ws = websocket.WebSocketApp(ws_url, header=self.headers, cookie=cookie,
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)

        self.ws.run_forever(sslopt={'cert_reqs': ssl.CERT_NONE})

    def on_error(self, ws, error):
        logging.error("WebSocket 发生错误: %s", error)
        logging.error("详细堆栈:\n%s", traceback.format_exc())

    def on_close(self, ws, close_status_code, close_msg):
        logging.info("连接关闭")

    def on_open(self, ws):
        logging.info("连接成功")
        # 发送初始化消息（取决于实际网站的协议）

    def on_message(self, ws, message):
        # 第一层
        obj = PushFrame()
        obj.ParseFromString(message)

        # 直播数据，解压缩
        payload = obj.payload
        payload_bytes = gzip.decompress(payload)
        response = Response()
        response.ParseFromString(payload_bytes)
        # 返回ack

        if response.need_ack:
            ack = PushFrame(LogID=obj.LogID, payload=response.internal_ext.encode('utf-8'),
                            payload_type='ack').SerializeToString()
            ws.send(ack, websocket.ABNF.OPCODE_BINARY)

        for msg in response.messages:
            method = msg.method
            handlers = {
                # 普通文字聊天消息（观众发送的弹幕）
                'WebcastChatMessage': self.parseChatMsg,

                # 送礼物消息（包含礼物信息、赠送者、数量等）
                'WebcastGiftMessage': self.parseGiftMsg,
                #
                # 点赞消息（用户点击“点赞”按钮）
                'WebcastLikeMessage': self.parseLikeMsg,
                # 用户进入直播间的消息
                'WebcastMemberMessage': self.parseMemberMsg,

                # 社交互动消息（如关注主播）
                'WebcastSocialMessage': self.parseSocialMsg,

                # 房间用户排序信息（可能用于显示“本场贡献榜”）
                'WebcastRoomUserSeqMessage': self.parseRoomUserSeqMsg,

                # 粉丝团相关消息（用户加入粉丝团、等级提升等）
                'WebcastFansclubMessage': self.parseFansclubMsg,

                # 控制消息（如直播暂停、关闭、权限控制等）
                'WebcastControlMessage': self.parseControlMsg,

                # 表情聊天消息（用户发送表情包而非文字）
                'WebcastEmojiChatMessage': self.parseEmojiChatMsg,

                # 直播间实时统计数据（在线人数、热度等）
                'WebcastRoomStatsMessage': self.parseRoomStatsMsg,

                # 房间基本信息消息（直播间名称、状态等）
                'WebcastRoomMessage': self.parseRoomMsg,

                # 排行榜信息消息（如打赏排行榜、活跃用户榜等）
                'WebcastRoomRankMessage': self.parseRankMsg,

                # 直播间流配置适配信息（用于调节直播流质量等）
                'WebcastRoomStreamAdaptationMessage': self.parseRoomStreamAdaptationMsg,
            }

            handler = handlers.get(method)
            if handler:
                handler(msg.payload)
            else:
                # 处理没有找到对应方法的情况，比如日志
                # logging.warning(f"No handler found for method: {method}")
                pass

    def parseChatMsg(self, payload):
        """聊天消息"""
        message = ChatMessage()
        message.ParseFromString(payload)

        user_name = message.user.nickname
        content = message.content
        logging.info(f"【聊天信息】{user_name}------>{content}")

    def parseGiftMsg(self, payload):
        """礼物消息"""
        message = GiftMessage()
        message.ParseFromString(payload)
        user_name = message.user.nickname
        gift_name = message.gift.name
        gift_cnt = message.combo_count
        logging.info(f"【礼物信息】{user_name} 送出了 {gift_name}x{gift_cnt}")

    def parseLikeMsg(self, payload):
        '''点赞消息'''
        message = LikeMessage()
        message.ParseFromString(payload)
        user_name = message.user.nickname
        count = message.count
        logging.info(f"【点赞信息】{user_name} 点了{count}个赞")

    def parseMemberMsg(self, payload):
        '''进入直播间消息'''
        message = MemberMessage()
        message.ParseFromString(payload)
        user_name = message.user.nickname
        gender = ['未知', "女", "男"][message.user.gender]
        logging.info(f"【进入信息】[{gender}]{user_name} 进入了直播间")

    def parseSocialMsg(self, payload):
        '''关注消息'''
        message = SocialMessage()
        message.ParseFromString(payload)

        user_name = message.user.nickname
        logging.info(f"【关注信息】{user_name} 关注了主播")

    def parseRoomUserSeqMsg(self, payload):
        '''直播间统计'''
        message = RoomUserSeqMessage()
        message.ParseFromString(payload)
        current = message.total
        total = message.total_pv_for_anchor
        logging.info(f"【统计信息】当前观看人数: {current}, 累计观看人数: {total}")

    def parseFansclubMsg(self, payload):
        '''粉丝团消息'''
        message = FansclubMessage()
        message.ParseFromString(payload)
        content = message.content
        logging.info(f"【粉丝团信息】 {content}")

    def parseEmojiChatMsg(self, payload):
        '''聊天表情包消息'''
        message = EmojiChatMessage()
        message.ParseFromString(payload)
        emoji_id = message.emoji_id
        user = message.user.nickname
        common = message.common
        default_content = message.default_content
        logging.info(f"【聊天表情包】 {emoji_id},user：{user},common:{common},default_content:{default_content}")

    def parseRoomMsg(self, payload):
        message = RoomMessage()
        message.ParseFromString(payload)
        common = message.common
        room_id = common.room_id
        logging.info(f"【直播间信息】直播间id:{room_id}")

    def parseRoomStatsMsg(self, payload):
        message = RoomStatsMessage()
        message.ParseFromString(payload)
        display_long = message.display_long
        logging.info(f"【直播间统计】{display_long}")

    def parseRankMsg(self, payload):
        message = RoomRankMessage()
        message.ParseFromString(payload)
        ranks_list = message.ranks
        logging.info(f"【直播间排行榜】")
        logging.info('---------------')
        for rank in ranks_list:
            logging.info(rank.user.nickname)
        logging.info('---------------')

    #
    def parseControlMsg(self, payload):
        '''直播间状态消息'''
        message = ControlMessage()
        message.ParseFromString(payload)

        if message.status == 3:
            logging.info("直播间已结束")
            self.on_close(ws=self.ws, close_msg='直播已结束', close_status_code=1000)

    def parseRoomStreamAdaptationMsg(self, payload):
        message = RoomStreamAdaptationMessage()
        message.ParseFromString(payload)
        adaptationType = message.adaptation_type
        logging.info(f'直播间adaptation: {adaptationType}')
