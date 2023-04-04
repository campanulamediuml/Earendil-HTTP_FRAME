import asyncio
import sys

if sys.platform != 'win32':
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    print(sys.platform, '操作系统，自动加载uvloop策略')
else:
    print(sys.platform, '操作系统，无法加载uvloop策略，采用默认策略')

from app.http.relay.relay import Relay as HTTP_Relay
from app.http.relay.relay import Relay as WS_Relay
from app.http import mods as http_mods
from app.ws import event as ws_mods
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from utils.Scheduler import Scheduler
from config import server_config




settings = {'debug' : server_config.IS_DEBUG}


class ServerHandler(object):
    def __init__(self, host, port,server_type='http'):
        self.server_type = server_type
        self._host = host
        self._port = port
        self._apps = self.register_handles()
        if server_type == 'http':
            HTTP_Relay.init(self)
        if server_type == 'ws':
            WS_Relay.init(self)

    def register_handles(self):
        if self.server_type == 'http':
            res = http_mods.route_list
        else:
            res = ws_mods.route_list
        return res

    def get_server_host(self):
        return self._host

    def get_server_port(self):
        return self._port

    def run(self):
        # asyncio.set_event_loop(asyncio.new_event_loop())
        print("start server")
        print(self._host + ":" + str(self._port))
        tornado.options.parse_command_line()
        http_server = tornado.httpserver.HTTPServer(tornado.web.Application(self._apps, **settings))
        http_server.bind(self._port, self._host)
        http_server.start(server_config.PROC_NUM)
        # 启动多个线程进行操作
        tornado.ioloop.PeriodicCallback(Scheduler.run, 500).start()
        # Scheduler.run(True)
        tornado.ioloop.IOLoop.current().start()
