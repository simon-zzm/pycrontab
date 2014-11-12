#!/bin/env python
# -*- coding:utf-8 -*-
# Filename:
# Revision:  
# Date:        2014-11-10
# Author:      simonzhang
# web:         www.simonzhang.net
# Email:       simon-zzm@163.com
### END INIT INFO
import re
import sys
import time

# 时间范围。格式为：分、小时、日、月、周
time_frame = [[0, 60], [0, 24], [1, 32], [1, 13], [0, 7]]

# 检查时间是否满足运行条件
def check_time(set_time, now_time, time_frame_num):
    # 初始化数据
    _skip = 1
    _time = []
    _status = "NO"
    _start_time = time_frame[time_frame_num][0]
    _end_time = time_frame[time_frame_num][1]
    # 按优先级处理标示符
    # 处理时间分组
    for list_time in set_time.split(','):
        # 处理判断间隔
        if list_time.find('/') > -1:
            _skip = int(list_time.split('/')[1])
        time_loop = list_time.split('/')[0]
        # 处理时间范围
        if time_loop.find('-') > -1:
            cut_time = time_loop.split('-')
            fri_time = int(cut_time[0])
            sec_time = int(cut_time[1])
            if fri_time > sec_time:
                for add_time_1 in xrange(fri_time, _end_time, _skip):
                    _time.append(add_time_1)
                for add_time_2 in xrange(_start_time, sec_time, _skip):
                    _time.append(add_time_2)
            else:
                for add_time_3 in xrange(fri_time, sec_time, _skip):
                    _time.append(add_time_3)
        else:
            # 如果为*放在最后判断
            if str(time_loop) != "*":
                _time.append(int(time_loop))
    if (int(now_time) in _time) or (str(set_time) == "*"):
        _status = "OK"
    return _status


# 运行命令行
def run_comm(comm_line):
    cut_comm_line = comm_line.split()
    # 组装运行命令
    _run_comm_line = ""
    for lo in xrange(5,len(cut_comm_line)):
        _run_comm_line = "%s %s" % (_run_comm_line, cut_comm_line[lo])
    from os import system
    system(_run_comm_line)


def loop_pycrontab_line(pycrontab_lines):
    # 初始化当前时间 
    get_now_time_list = []
    get_now_time = time.localtime()
    get_now_mon = get_now_time[1]
    get_now_day = get_now_time[2]
    get_now_hou = get_now_time[3]
    get_now_min = get_now_time[4]
    get_now_sec = get_now_time[5]
    get_now_wek = get_now_time[6]+1
    if get_now_wek == 7:
        get_now_wek = 0
    get_now_time_list = [get_now_min, \
                         get_now_hou, \
                         get_now_day, \
                         get_now_mon, \
                         get_now_wek]
    # 循环处理每条定时任务
    for single_line in pycrontab_lines:
        run_status = "OK"
        # 判断回车
        if single_line[-1] == '\n':
            single_line = single_line[:-1]
        # 判断每行时间格式是否正确
        split_pycrontab_line = single_line.split()
        for single_char in xrange(5):
            if len(re.findall("[\*|0-9|\/|\,|-]{0,20}", split_pycrontab_line[single_char])) > 2:
                run_status = "Error"
        if run_status == "OK":
            # 判断是否需要执行
            for lo in xrange(5):
                if check_time(split_pycrontab_line[lo], get_now_time_list[lo], lo) == "NO":
                    run_status = "NO"
            # 判断是否运行
            if run_status == "OK":
                run_comm(single_line)
        else:
            print "Error %s" % single_line
 

def main():
    # 
    try:
        with open("pycrontab.conf") as pycrontab_conf_file:  
            pycrontab_conf = pycrontab_conf_file.readlines()
    except:
        print "pycrontab.conf file ERROR!"
        sys.exit(1)
    loop_pycrontab_line(pycrontab_conf)



if __name__ == "__main__":
    main()
