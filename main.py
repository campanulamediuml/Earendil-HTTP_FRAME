from app.server_handler import ServerHandler
from utils import common
import time

from config.config import server_config


def main():
    host = server_config['host']
    port = server_config['port']
    print('server_running', host, port)
    print('服务器操作系统', common.get_sys_info())
    server = ServerHandler(host, port)
    print('[' + common.time_to_str(int(time.time())) + ']Server Run')
    server.run()

main()
