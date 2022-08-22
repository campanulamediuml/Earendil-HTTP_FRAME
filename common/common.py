# 通用函数放在这里
import datetime
import hashlib
import sys
import time


def get_sys_info():
    os_info = sys.platform
    return os_info


def print_processing_name():
    # print(sys.argv)
    try:
        server_name = sys.argv[0].split('.')[0]
        return server_name
    except:
        return

def time_to_str(times=time.time()):
    if times == 0:
        return '2019-09-24 00:00:00'
    date_array = datetime.datetime.utcfromtimestamp(times + (8 * 3600))
    return date_array.strftime("%Y-%m-%d %H:%M:%S")


def get_sha1(string):
    sha1 = hashlib.sha1(string.encode(encoding='UTF-8')).hexdigest()
    return sha1


def str_to_time(time_str):
    timeArray = time.strptime(str(time_str), "%Y-%m-%d %H:%M:%S")
    time_stamp = int(time.mktime(timeArray))
    return time_stamp

