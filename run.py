import datetime
import os
import time
import sys
# from utils.utils import time_to_str
from utils.common import time_to_str
from config.server_config import log_path, interpreter

doc = """Error - 指令缺失
命令提示:
check  查看运行进程
clean  清除日志
shutdown pid 关闭进程
start name 启动进程
"""
# script_list = ['server_main']

# query = 'ps -x | grep /usr/bin/python3'
# running_proc = os.popen(query).readlines()
# for i in running_proc:
#     os.system('kill -9 %s'%i.split()[0])

def start():
    # try:
    # query = 'nohup uwsgi --socket 0.0.0.0:7777 --protocol=http -w main:main >> server.log 2>&1 &'
    if len(sys.argv) < 3:
        print('缺少脚本名称')
        return

    script = sys.argv[2]
    name = log_path+script+ time_to_str(int(time.time())).replace(' ','-').replace(':','x')+'.log'
    query = 'mv '+script+'.log'+' '+name
    os.system(query)
    print('上一份日志备份到',name)
    time.sleep(1)
    query = 'nohup %s -u '%interpreter+script+'.py > '+script+'.log 2>&1 &'
    os.system(query)
    print('运行'+script+'.py成功, 日志位置>> '+script+'.log')
        # else:
        #     print('非法指令')

    print('start done!')
    open_log = 'cat '+script+'.log'
    time.sleep(0.5)
    os.system(open_log)
    return

def clean():
    query = "rm server.log"
    os.system(query)
    print('clean server.log done!')

def check():
    query = 'ps -x | grep %s'%interpreter
    os.system(query)
    return

def kill():
    # print('长度为',len(sys.argv))
    if len(sys.argv) < 3:
        print('缺少脚本名称')
        return

    script = sys.argv[2]
    # if script not in script_list:
    #     return print('这个进程无法通过运维脚本杀死...')
    query = 'ps -x | grep %s'%interpreter
    running_proc = os.popen(query).readlines()
    for line in running_proc:
        # print(line)
        line_info = line.split()
        # print(line_info)
        if len(line_info) > 6:
            if script in line_info[6]:
                pid = line.split()[0]
                # print(pid)
                query = 'kill '+str(pid)
                os.system(query)
                print('杀死',script,pid,'完毕')
    return

def execute_command(command):

    if command == 'clean':
        clean()
        return

    if command == 'start':
        start()
        return

    if command == 'kill':
        kill()
        return

    if command == 'restart':
        print('restarting...')
        kill()
        start()
        print('restart_done!')
        return

    if command == 'check':
        check()
        return


def main():
    if len(sys.argv) == 1:
        print(doc)
        return
    command = sys.argv[1]
    if command not in ['clean','start','restart','check','kill']:
        print('command error!')
        return
    else:
        execute_command(command)


main()
