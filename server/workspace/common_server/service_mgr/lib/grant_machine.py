#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-5-26

@author: Jay
"""
import datetime
import copy

from utils.meta.singleton import Singleton
from utils.comm_func import datetime_to_string
from utils.regex import IP_REGEX, TIME_STR_REGEX
from utils import logger
from utils.interfaces.common import IManager

VALIDATE_OS = [
    OS_LINUX,
    OS_WINDOWS,
] = [
    "LINUX",
    "WINDOWS"
]

class GrantMachineMgr(IManager):
    __metaclass__ = Singleton

    def __init__(self):
        self.machine_dic = {}
        self.init_data_ls = None

    def init(self, data_ls):
        self.init_data_ls = data_ls
        self.machine_dic = {}
        for machine_dic in data_ls:
            self.machine_dic[machine_dic["ip"]] = machine_dic

    def get_init_data_ls(self):
        return self.init_data_ls

    def db_unpick(self, data_ls):
        """
        db 反序列化
        :param data_ls:
        :return:
        """
        return data_ls

    def web_unpick(self, data_ls):
        """
        web 反序列化
        :param data_ls:
        :return:
        """
        unpick_ls = copy.deepcopy(data_ls)

        now_time = datetime_to_string(datetime.datetime.now())
        v_data_ls = []
        for data_dic in unpick_ls:
            if not IP_REGEX.match(data_dic['ip']):
                logger.warn("GrantMachineMgr::web_unpick invalid params:%s" % data_dic)
                continue

            if not TIME_STR_REGEX.match(data_dic['create_time']):
                data_dic['create_time'] = now_time

            if not data_dic['os'] in VALIDATE_OS:
                data_dic['os'] = OS_WINDOWS

            v_data_ls.append(data_dic)
        return v_data_ls

    def get_machine(self, ip):
        return self.machine_dic.get(ip, None)


