import json
import time

from utils import common
from utils.common import dbg
from error.error import error_info


class event_base(object):
    def __init__(self,connection,event='',data=None,token='',pac_msg=None):
        self.pac_msg = pac_msg
        self.return_event = event
        self.connection = connection
        self.event = event
        self.data = data
        self.return_data = {
            'status':False,
            'msg':''
        }
        self.token = token
        # Relay.call_back_data[self.token] = self.data

    async def send_return_data(self,data=None):
        res = {
            'event':self.return_event,
            'token':self.token,
            'c_time':int(time.time())
        }
        if data is None:
            res['payload'] = self.return_data
        else:
            res['payload'] = data
        message = json.dumps(res)
        dbg('来自event.send行为',res)
        dbg('本次发送字节原始数据', message)
        try:
            self.connection.write_message(message)
        except:
            dbg('connection已经关闭')
        return
        # 发送返回信息

    async def send_fail(self,event,err_code,msg = ''):
        self.return_event = event
        self.return_data['status'] = err_code
        if msg == '':
            self.return_data['msg'] = error_info[err_code]
        else:
            self.return_data['msg'] = msg
        await self.send_return_data()

    async def send_ok(self,event,data):
        self.return_event = event
        self.return_data = data
        await self.send_return_data()