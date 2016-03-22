#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2016-1-9

@author: Jay
"""
from utils.interfaces.common import IManager
from utils.meta.singleton import Singleton
from mmm_da.db import DBHistoryNoticeInst
import time


class HistoryNoticeMgr(IManager):
    """
    历史通知管理器
    """
    __metaclass__ = Singleton

    def __init__(self):
        pass

    def get_all_notice(self):
        """
        获取所有的公告
        :return:
        """
        return DBHistoryNoticeInst.query_all()

    def add_notice(self, notice):
        """
        添加公告
        :param notice: 公告
        :return:
        """
        DBHistoryNoticeInst.insert_ls([{"notice": notice, "time": time.time()}])
