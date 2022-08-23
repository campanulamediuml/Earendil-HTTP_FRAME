class Relay():
    server = None
    request_dict = {}
    #{
        # request_id:request_time
    # }

    @staticmethod
    def init(server):
        Relay.server = server
    # 初始化服务器

    @staticmethod
    def get_server_host():
        return Relay.server.get_server_host()
    # 获取服务器地址

    @staticmethod
    def get_server_port():
        return Relay.server.get_server_port()
    # 获取服务器端口
    @staticmethod
    def client_connection(connection):
        return

    @staticmethod
    def disconnect(sid):
        return