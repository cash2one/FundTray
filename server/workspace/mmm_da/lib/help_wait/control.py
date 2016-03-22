#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2016-2-20

@author: Jay
"""
from utils import logger
from utils.interfaces.common import IManager
from utils.meta.singleton import Singleton
from utils.data.cache.dirty import DirtyDictProcess
from mmm_da.lib.filter.control import ApplyWaitFilter
from mmm_da.db import DBApplyHelpWaitInst
from mmm_da.lib.server_info import ServerInfoMgr
from mmm_da.lib.formula import hoursdiff
from mmm_da.lib.account.control import AccountMgr
from mmm_da.lib.account.model import SEALED


class ApplyHelpWaitMgr(IManager):
    """
    申请帮助等待
    """
    __metaclass__ = Singleton

    def __init__(self):
        self.__uid_2_wait_dic = {}                # uid <=> wait dic

        self.__ddp = DirtyDictProcess(["apply_wait_uid"])

    def init_sql(self):
        """
        初始化查找sql语句
        :return:
        """
        return "select * from apply_help_wait"

    def init(self, data_ls):
        self.__init__()

        for dic in data_ls:
            self.__add_data_2_mem(dic)

        filter_params = {}
        filter_params.setdefault("apply_aft_accept_hour", ServerInfoMgr().attr_apply_aft_accept_hour)
        filter_params.setdefault("hours_diff_fun", hoursdiff)
        ApplyWaitFilter().init(self.wait_ls,  self.do_not_apply, filter_params)

    def update(self, curtime):
        dirty_dict = self.__ddp.get_db_dirty_dicts()
        DBApplyHelpWaitInst.update_ls(dirty_dict.get("update", []))
        DBApplyHelpWaitInst.insert_ls(dirty_dict.get("insert", []))
        DBApplyHelpWaitInst.delete_ls(dirty_dict.get("delete", []))

    def wait_ls(self):
        """
        获取等待的数据列表
        :return:
        """
        wait_ls = self.__uid_2_wait_dic.values()
        wait_ls = filter(lambda dic: not AccountMgr().get_data_by_id(dic['apply_wait_uid']).is_seal,
                         wait_ls)
        return wait_ls

    def __add_data_2_mem(self, dic):
        self.__uid_2_wait_dic[dic['apply_wait_uid']] = dic

    def __del_data_2_mem(self, dic):
        """
        从mem删除数据
        :param dic:
        :return:
        """
        self.__uid_2_wait_dic.pop(dic['apply_wait_uid'], None)

    def __insert_dic(self, dic):
        """
        插入数据到mem/db
        :param dic: 数据字典
        :return:
        """
        self.__ddp.ist_db_dict(dic['apply_wait_uid'], dic)
        self.__add_data_2_mem(dic)

    def __update_dic(self, apply_wait_uid, dic):
        """
        更新数据到mem/db
        :param apply_wait_uid:  接受帮助等待uid
        :param dic:  更新数据字典
        :return:
        """
        self.__ddp.upd_db_dict(id, dic)

        cur_dic = self.get_data_by_uid(apply_wait_uid)
        if cur_dic:
            cur_dic.update(dic)

    def add_wait(self, apply_wait_uid, apply_wait_time):
        """
        添加等待
        :param apply_wait_uid: 申请帮助等待用户id
        :param apply_wait_time: 申请帮助等待开始时间
        :return:
        """
        data_dic = {'apply_wait_uid': apply_wait_uid,
                    'apply_wait_time': apply_wait_time}
        self.__insert_dic(data_dic)

        logger.info("ApplyHelpWaitMgr add_wait!!, apply_wait_uid:%s, apply_wait_time:%s" % (apply_wait_uid, apply_wait_time))

    def del_wait(self, apply_wait_uid):
        """
        删除等待
        :param apply_wait_uid: 删除等待的用户id
        :return:
        """
        if not self.get_data_by_uid(apply_wait_uid):
            return

        self.__del_data_2_mem(self.get_data_by_uid(apply_wait_uid))
        self.__ddp.del_db_dict(apply_wait_uid, {"apply_wait_uid": apply_wait_uid})

        logger.info("ApplyHelpWaitMgr del_wait!!, apply_wait_uid:%s" % apply_wait_uid)

    def get_data_by_uid(self, uid):
        """
        根据用户id获取信息列表
        :param uid:
        :return:
        """
        return self.__uid_2_wait_dic.get(uid, {})

    def do_not_apply(self, apply_wait_uid):
        """
        在对应时间内没有申请帮助
        :param apply_wait_uid: 等待申请帮助uid
        :return:
        """
        # 封号
        account = AccountMgr().get_data_by_id(apply_wait_uid)
        account.attr_stat = SEALED

        # 删除等待
        self.del_wait(apply_wait_uid)

