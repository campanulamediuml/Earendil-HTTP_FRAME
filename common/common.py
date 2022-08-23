# 通用函数放在这里
import datetime
import hashlib
import random
import string
import sys
import time

def dbg(*args):
    now_ts = time.time()
    res = ['[%s %s]' % (time_to_str(now_ts),now_ts)] + list(args)
    print(*res)

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

def get_md5(string):
    md5 = hashlib.md5(string.encode('utf-8')).hexdigest()
    return md5


def str_to_time(time_str):
    timeArray = time.strptime(str(time_str), "%Y-%m-%d %H:%M:%S")
    time_stamp = int(time.mktime(timeArray))
    return time_stamp

def create_rand_string(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def get_start_and_end_index(page,per_page):
    return [(page - 1) * per_page, per_page]

def get_page_count_by_length(per_page,length):
    max_page = 0
    if length != None:
        max_page = length / per_page
        if int(max_page) < max_page:
            max_page += 1
        if int(max_page) == 0:
            max_page += 1
    return int(max_page)