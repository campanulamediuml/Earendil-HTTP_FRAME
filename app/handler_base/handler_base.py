import os
import threading
import time
from tornado.concurrent import run_on_executor
from tornado.escape import json_decode
from tornado.web import RequestHandler
from concurrent.futures import ThreadPoolExecutor
from app.http.relay.relay import Relay
from config import server_config
from error import error
from config.server_config import thread_pool_num
import json

# ANALYS_BASE = 'statistics'


class HandlerBase(RequestHandler):
    max_age = 1000
    long_data = 10240
    executor = ThreadPoolExecutor(thread_pool_num)

    def if_out_time(self):
        request_pid = self.request.uri
        print(request_pid)
        if request_pid in Relay.request_dict:
            print(os.getpid(),'这个请求发生过')
            try:
                if int(time.time()) - Relay.request_dict[request_pid] < 2:
                    self.request.body = json.dumps({})
                    # self.clear()
                    print(request_pid, '重复请求')
                    return True
            except:
                self.request.body = json.dumps({})
                # self.clear()
        Relay.request_dict[request_pid] = int(time.time())
        return False

    def remove_pid(self):
        request_pid = self.request.uri
        if request_pid in Relay.request_dict:
            try:
                Relay.request_dict.pop(request_pid)
            except:
                pass

    def set_default_headers(self):
        origin = self.request.headers.get('Origin')
        if origin == None:
            origin = '*'
        print('添加响应标头')
        self.set_header('Access-Control-Allow-Origin', origin)
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', HandlerBase.max_age)
        self.set_header('Access-Control-Allow-Headers', 'X-Requested-With,Origin,Content-Type')
        self.set_header('Server', server_config.server_name)
        print(self.get_remote_ip())
        thread_id = threading.currentThread().ident
        print('本次请求来自',thread_id)

    def get_remote_ip(self):
        try:
            remote_ip = self.request.headers.get('X-Forwarded-For')
        except:
            remote_ip = '0.0.0.0'
        if remote_ip == None:
            remote_ip = '127.0.0.1'
            print('<===获取到真实ip===>', remote_ip)
        return remote_ip

    # @run_on_executor
    def options(self):
        print('<---------收到跨域请求，返回空值--------->')
        self.write({})
        return

    def get_result(self):
        '''
        返回结构基本模板
        :return:
        '''
        result = {}
        result['code'] = error.ERROR_OK
        result['msg'] = ''
        result['data'] = {}
        return result


    def get_token(self):
        return self.get_argument('token')

    def send_ok(self, data=None):
        """
        正确信息返回
        :param data:
        :return:
        """
        result = self.get_result()
        result['data'] = data
        print('<---------请求成功，返回值--------->')
        if len(json.dumps(result)) > HandlerBase.long_data:
            print()
        else:
            print(result)
        # 打印日志
        self.write(result)
        self.remove_pid()

    def send_faild(self, code, err_msg=''):
        '''
        失败信息返回
        :param code:
        :return:
        '''
        result = self.get_result()
        unit = error.error_info[code]
        result['code'] = code
        if err_msg == '':
            result['msg'] = unit
        else:
            result['msg'] = err_msg
        print('<---------请求失败，返回值--------->')
        print(result)
        self.write(json.dumps(result))
        # self.remove_pid()

    def get_data(self):
        '''
        获取get请求内容
        :return:
        '''
        data = self.get_argument('data')
        if data is None:
            print('没有收到get参数')
            return data
        res = json.loads(data)
        print(data)
        return res

    def get_files(self, key):
        if key in self.request.files:
            file_metas = self.request.files[key][0]['body']
            return file_metas
        else:
            return None

    def get_post_data(self) -> dict:
        '''
        获取post请求内容
        :return:
        '''
        try:
            data = json_decode(self.request.body)
            if len(self.request.body) < HandlerBase.long_data:
                print(self.request.body)
                print('收到post数据', data)
        except Exception as e:
            print(str(e))
            print('body为空')
            return {}
        return data


