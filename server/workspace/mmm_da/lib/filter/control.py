#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2016-2-26

@author: Jay
"""

from utils.meta.singleton import Singleton
from model import DataFilter
import time

class AcceptReqFilter(DataFilter):
    """
    接受帮助请求过滤器
    """
    __metaclass__ = Singleton

    def _src_filter(self, data):
        """
        源数据过滤函数
        :param data:
        :return:
        """
        days_diff_fun = self._params['days_diff_fun']
        accept_match_min_days = self._params['accept_match_min_days']
        return days_diff_fun(time.time(), data['accept_req_time']) >= accept_match_min_days

    def _des_mapper(self, data):
        """
        目标数据映射函数
        :param data:
        :return:
        """
        return data['id']


class ApplyReqFilter(DataFilter):
    """
    接受帮助请求过滤器
    """
    __metaclass__ = Singleton

    def _src_filter(self, data):
        """
        源数据过滤函数
        :param data:
        :return:
        """
        days_diff_fun = self._params['days_diff_fun']
        apply_match_min_days = self._params['apply_match_min_days']
        return days_diff_fun(time.time(), data['apply_req_time']) >= apply_match_min_days

    def _des_mapper(self, data):
        """
        目标数据映射函数
        :param data:
        :return:
        """
        return data['id']


class ApplyPayFilter(DataFilter):
    """
    申请帮助支付检测匹过滤器
    """
    __metaclass__ = Singleton

    def _src_filter(self, data):
        """
        源数据过滤函数
        :param data:
        :return:
        """
        days_diff_fun = self._params['days_diff_fun']
        apply_pay_max_days = self._params['apply_pay_max_days']
        return days_diff_fun(time.time(), data['apply_mtime']) >= apply_pay_max_days

    def _des_mapper(self, data):
        """
        目标数据映射函数
        :param data:
        :return:
        """
        return data['apply_sorder']


class ApplyWaitFilter(DataFilter):
    """
    申请帮助等待过滤器，如果等待时间到，没有申请帮助，封号
    """
    __metaclass__ = Singleton

    def _src_filter(self, data):
        """
        源数据过滤函数
        :param data:
        :return:
        """
        hours_diff_fun = self._params['hours_diff_fun']
        apply_aft_accept_hour = self._params['apply_aft_accept_hour']
        return hours_diff_fun(time.time(), data['apply_wait_time']) >= apply_aft_accept_hour

    def _des_mapper(self, data):
        """
        目标数据映射函数
        :param data:
        :return:
        """
        return data['apply_wait_uid']

