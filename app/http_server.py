# import asyncio
from app.http.relay.relay import Relay
from app.http import mods
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from common.Scheduler import Scheduler
from config import server_config

settings = {'debug' : server_config.IS_DEBUG}


class HttpServer(object):
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._apps = self.register_handles()
        Relay.init(self)

    def register_handles(self):
        res = mods.route_list
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
