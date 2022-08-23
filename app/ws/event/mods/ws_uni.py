import json

from app.handler_base.ws_base import ws_base
from app.ws.relay.relay import Relay
from common.common import dbg


class user_connection(ws_base):
    route_table = {
    }
    # @gen.coroutine
    async def open(self):
        self.client_sid = id(self)
        Relay.client_connection(self)

    async def on_message(self, msg):
        await self.exec_run(msg)

    async def exec_run(self, msg):
        try:
            dbg('收到原始二进制内容',msg)
            if type(msg) == type(''):
                msg = msg.encode()
            msg_list = msg.split(b'}{')
            if len(msg_list) > 1:
                msg_list[0] = msg_list[0][1:]
                msg_list[-1] = msg_list[-1][:-1]
            else:
                msg_list[0] = msg_list[0][1:-1]
            dbg('原始二进制内容包含%s条数据包'%len(msg_list))
            count = 0
            for m in msg_list:
                count += 1
                msg_raw = b'{'+m+b'}'
                dbg('第%s条原始二进制内容'%count,msg_raw)
                msg = json.loads(b'{'+m+b'}')
                event = msg['event']
                data = msg['payload']
                if 'token' not in msg:
                    msg['token'] = ''
                token = msg['token']
                if event in user_connection.route_table:
                    dbg(self.client_sid, msg)
                    method = user_connection.route_table[event]
                    exe = method(self, event, data, token,msg)
                    await exe.execute()
        except Exception as e:
            dbg(str(e))
            raise e

    def on_close(self):
        dbg(id(self),'断开连接')
        offline(self).execute()