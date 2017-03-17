#! /user/bin/python3
# -*- utf-8 -*-
# author: vin

import subprocess
import re

def run_cmd(cmd):
	"""执行CMD命令"""
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
	return [i.decode() for i in p.communicate()[0].splitlines()]

def get_apk_info():
    """获取apk的package，activity名称

    :return: list  eg ['com.android.calendar', 'com.meizu.flyme.calendar.AllInOneActivity']
    """
    result = run_cmd("adb shell dumpsys activity top")
    for line in result:
        if line.strip().startswith('ACTIVITY'):
            return line.split()[1].split('/')

def get_mem_using(package_name=None):
    """查看apk的总内存占用

    :param package_name:
    :return: 单位KB
    """
    if not package_name:
        package_name = get_apk_info()[0]
    result = run_cmd("adb shell dumpsys meminfo {}".format(package_name))
    info = re.search('TOTAL\W+\d+', str(result)).group()
#    info = re.search('Native\w+\d+\d+', str(result)).group()
#   info = re.match('^Native Heap(.*?)', str(result))
    mem = ''
    try:
        mem = info.split()
    except Exception as e:
        print(info)
        print(e)
    return mem[-1]

def get_mem_native_dalvik(package_name=None):
    """查看apk的内存占用
    返回JNI层和Java层的内存分配情况：Native/Dalvik Heap
    :return: 单位KB
    """
    result = run_cmd("adb shell dumpsys meminfo {}".format(package_name))
    native = 'Native'
    dalvik = 'Dalvik'
    for i in result:
        if native in i:
          native = i
        if dalvik in i:
            dalvik = i
    try:
        mem_native = native.split()
        mem_dalvik = dalvik.split()

    except Exception as e:
        print(native,dalvik)
        print(e)
    else:
        mem = mem_native[-3:]+ mem_dalvik[-3:]
        return mem


