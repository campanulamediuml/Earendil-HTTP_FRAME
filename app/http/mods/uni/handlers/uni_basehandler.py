import time

from anduin import Data
from tornado.concurrent import run_on_executor
from werkzeug.security import generate_password_hash
from app.http.handler_base import HandlerBase
from dbmodel.db_data import table
from error import error


class get_example(HandlerBase):
    @run_on_executor
    def get(self):
        reply = {
            'result':'data'
        }
        return self.send_ok(reply)

class post_example(HandlerBase):
    @run_on_executor
    def post(self):
        data = self.get_post_data()
        reply = {
            'result':'data',
            'your_post_data':data
        }
        return self.send_ok(reply)

class db_example_find(HandlerBase):
    @run_on_executor
    def post(self):
        try:
            data = self.get_post_data()
            username = data['username']
            status = data['status']
        except Exception as e:
            print(str(e))
            return self.send_faild(error.ERROR_FAIL)
        cond = [
            ('username','=',username),
            ('status','=',status)
        ]
        user_info = Data.find(table.TABLE_USER,conditions=cond)
        reply = {
            'user_info':user_info
        }
        return self.send_ok(reply)
        # 单独查找某一条数据

class db_example_select(HandlerBase):
    @run_on_executor
    def post(self):
        try:
            data = self.get_post_data()
            status = data['status']
        except Exception as e:
            print(str(e))
            return self.send_faild(error.ERROR_FAIL)
        cond = [
            ('status','=',status)
        ]
        user_info = Data.select(table.TABLE_USER,conditions=cond)
        reply = {
            'user_list': user_info
        }
        return self.send_ok(reply)
        # 批量查找满足条件的数据

class db_example_update(HandlerBase):
    @run_on_executor
    def post(self):
        try:
            data = self.get_post_data()
            username = data['username']
            status = data['status']
        except Exception as e:
            print(str(e))
            return self.send_faild(error.ERROR_FAIL)
        cond = [
            ('username', '=', username)
        ]
        params ={
            'status':status,
            'u_time':int(time.time())
        }
        Data.update(table.TABLE_USER, conditions=cond,params=params)
        reply = {}
        return self.send_ok(reply)

class db_example_insert(HandlerBase):
    @run_on_executor
    def post(self):
        try:
            data = self.get_post_data()
            username = data['username']
            passwd = data['passwd']
        except Exception as e:
            print(str(e))
            return self.send_faild(error.ERROR_FAIL)

        params ={
            'username':username,
            'pw_hash':generate_password_hash(passwd),
            'c_time':int(time.time())
        }

        Data.insert(table.TABLE_USER, params=params)
        reply = {}
        return self.send_ok(reply)