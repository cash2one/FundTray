#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2016-2-26

@author: Jay
"""
from utils import logger
import sys

class DataFilter(object):
    # 数据过滤器

    def __init__(self):
        self._src_data_ls_fun = None
        self._des_data_ls_fun = None
        self._params = {}

    def init(self, src_data_ls_fun, des_data_ls_fun, params):
        """
        初始化数据源
        :param src_data_ls_fun: 源数据获取函数
        :param des_data_ls_fun: 目标数据回调函数
        :param params:   其他参数
        :return:
        """
        self._src_data_ls_fun = src_data_ls_fun
        self._des_data_ls_fun = des_data_ls_fun
        self._params = params

    def prepare(self):
        """
        数据准备
        :return:
        """
        return self._src_data_ls_fun()

    def filter(self):
        """
        匹配函数
        :return:
        """
        src_data_ls = self.prepare()

        matched_data_ls = filter(self._src_filter, src_data_ls)
        cb_data_ls = map(self._des_mapper, matched_data_ls)
        logger.warn("%s::%s!!! matched:%s" % (self.__class__.__name__, sys._getframe().f_code.co_name, cb_data_ls))
        [self._des_data_ls_fun(cb_data) for cb_data in cb_data_ls]

    def _src_filter(self, data):
        """
        源数据过滤函数
        :param data:
        :return:
        """
        return data

    def _des_mapper(self, data):
        """
        目标数据映射函数
        :param data:
        :return:
        """
        return data
