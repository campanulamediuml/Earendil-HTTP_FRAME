import json
import time

import requests
from anduin import Data
from tornado.concurrent import run_on_executor
from werkzeug.security import generate_password_hash

from app.handler_base.handler_base import HandlerBase
from app.http.relay.relay import Relay
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

class sync(HandlerBase):
    async def post(self):
        print(self.request.body)
        print(list(map(int,self.request.body)))
        post_data = self.get_post_data()
        url = 'https://ot-product.sucheon.com/api/manager/box/register/batch'
        header = {'verification-permission': 'sucheon.registerBox'}
        r = requests.post(url,json=post_data,headers=header)
        print(r.status_code)
        print(r.text)
        return self.send_ok({})








if __name__ == '__main__':
    # raw_data = b'xxxxxxx'
    raw_data = b'[{"UUID":"DCA6320E0502-1","boxName":"Noilyzer-v2-11384-V","eth0MAC":"DCA6320E0501","wlan0MAC":"DCA6320E0502","sshPort":11384,"attribute":2,"id":0,"type":0},{"UUID":"DCA6320E0502-2","boxName":"Noilyzer-v2-11384-S","eth0MAC":"DCA6320E0501","wlan0MAC":"DCA6320E0502","sshPort":11384,"attribute":2,"id":0,"type":0},{"UUID":"DCA6320E0502-3","boxName":"Noilyzer-v2-11384-T","eth0MAC":"DCA6320E0501","wlan0MAC":"DCA6320E0502","sshPort":11384,"attribute":2,"id":0,"type":0}]  '
    url = 'https://ot-product.sucheon.com/api/manager/box/register/batch'
    # url = 'https://ot-product.sucheon.com/api/manager/box/register'
    # url = 'http://192.168.18.56:20000/uni/sync'
    header = {'verification-permission': 'sucheon.registerBox'}
    # json_data = json.loads(raw_data)
    r = requests.post(url, data=raw_data, headers=header)
    print(r.headers)
    print(r.status_code)
    print(r.text)
    # string = [91, 123, 34, 85, 85, 73, 68, 34, 58, 34, 68, 67, 65, 54, 51, 50, 48, 69, 48, 53, 48, 50, 45, 49, 34, 44, 34, 98,
    #  111, 120, 78, 97, 109, 101, 34, 58, 34, 78, 111, 105, 108, 121, 122, 101, 114, 45, 118, 50, 45, 49, 49, 51, 56, 52,
    #  45, 86, 34, 44, 34, 101, 116, 104, 48, 77, 65, 67, 34, 58, 34, 68, 67, 65, 54, 51, 50, 48, 69, 48, 53, 48, 49, 34,
    #  44, 34, 119, 108, 97, 110, 48, 77, 65, 67, 34, 58, 34, 68, 67, 65, 54, 51, 50, 48, 69, 48, 53, 48, 50, 34, 44, 34,
    #  115, 115, 104, 80, 111, 114, 116, 34, 58, 49, 49, 51, 56, 52, 44, 34, 97, 116, 116, 114, 105, 98, 117, 116, 101,
    #  34, 58, 50, 44, 34, 105, 100, 34, 58, 48, 44, 34, 116, 121, 112, 101, 34, 58, 48, 125, 44, 123, 34, 85, 85, 73, 68,
    #  34, 58, 34, 68, 67, 65, 54, 51, 50, 48, 69, 48, 53, 48, 50, 45, 50, 34, 44, 34, 98, 111, 120, 78, 97, 109, 101, 34,
    #  58, 34, 78, 111, 105, 108, 121, 122, 101, 114, 45, 118, 50, 45, 49, 49, 51, 56, 52, 45, 83, 34, 44, 34, 101, 116,
    #  104, 48, 77, 65, 67, 34, 58, 34, 68, 67, 65, 54, 51, 50, 48, 69, 48, 53, 48, 49, 34, 44, 34, 119, 108, 97, 110, 48,
    #  77, 65, 67, 34, 58, 34, 68, 67, 65, 54, 51, 50, 48, 69, 48, 53, 48, 50, 34, 44, 34, 115, 115, 104, 80, 111, 114,
    #  116, 34, 58, 49, 49, 51, 56, 52, 44, 34, 97, 116, 116, 114, 105, 98, 117, 116, 101, 34, 58, 50, 44, 34, 105, 100,
    #  34, 58, 48, 44, 34, 116, 121, 112, 101, 34, 58, 48, 125, 44, 123, 34, 85, 85, 73, 68, 34, 58, 34, 68, 67, 65, 54,
    #  51, 50, 48, 69, 48, 53, 48, 50, 45, 51, 34, 44, 34, 98, 111, 120, 78, 97, 109, 101, 34, 58, 34, 78, 111, 105, 108,
    #  121, 122, 101, 114, 45, 118, 50, 45, 49, 49, 51, 56, 52, 45, 84, 34, 44, 34, 101, 116, 104, 48, 77, 65, 67, 34, 58,
    #  34, 68, 67, 65, 54, 51, 50, 48, 69, 48, 53, 48, 49, 34, 44, 34, 119, 108, 97, 110, 48, 77, 65, 67, 34, 58, 34, 68,
    #  67, 65, 54, 51, 50, 48, 69, 48, 53, 48, 50, 34, 44, 34, 115, 115, 104, 80, 111, 114, 116, 34, 58, 49, 49, 51, 56,
    #  52, 44, 34, 97, 116, 116, 114, 105, 98, 117, 116, 101, 34, 58, 50, 44, 34, 105, 100, 34, 58, 48, 44, 34, 116, 121,
    #  112, 101, 34, 58, 48, 125, 93]
    # for i in string:
    #     print(bytes([i]))

