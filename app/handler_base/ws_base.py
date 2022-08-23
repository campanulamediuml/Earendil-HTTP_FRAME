from tornado import websocket

class ws_base(websocket.WebSocketHandler):

    def check_origin(self, origin):
        '''重写同源检查 解决跨域问题'''
        # print(self.get_compression_options())
        return True