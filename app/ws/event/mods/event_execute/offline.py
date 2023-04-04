from app.ws.event.event_base import event_base
from app.ws.relay.relay import Relay
from utils.common import dbg


class devset_offline(event_base):
    def execute(self):
        sid = id(self.connection)
        dbg(id(self.connection),'断开连接')
        return Relay.disconnect(sid)