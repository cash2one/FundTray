#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-5-26

@author: Jay
"""
import copy

from utils.meta.singleton import Singleton
from utils import logger
from utils.interfaces.common import IManager


class ServiceGrpMgr(IManager):
    __metaclass__ = Singleton

    def __init__(self):
        self.id_to_dic = {}
        self.type_to_dic = {}
        self.init_data_ls = None

    def init(self, data_ls):
        self.init_data_ls = data_ls
        self.id_to_dic = {}
        for dic in data_ls:
            self.id_to_dic[dic['id']] = dic

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

        v_data_ls = []
        for data_dic in unpick_ls:
            if not data_dic['id']:
                logger.warn("ServiceGrpMgr::web_unpick invalid params:%s" % data_dic)
                continue
            v_data_ls.append(data_dic)
        return v_data_ls

    def get_service_grp(self, service_grp_id):
        return self.id_to_dic.get(service_grp_id, {})

    def get_service_grps(self):
        return self.id_to_dic.keys()

    def get_visible(self, viewer):
        """
        根据查看者获取可查看的服务组列表
        :param viewer:
        :return:
        """
        visibles = []

        for sgid, sginfo in self.id_to_dic.items():
            invisible = sginfo.get("invisible", [])
            if invisible is None or viewer not in invisible:
                visibles.append(sgid)

        return visibles
