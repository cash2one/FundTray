#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-12-19

@author: Jay
"""
import time
from utils import logger
from utils.interfaces.common import IManager
from utils.meta.singleton import Singleton
from utils.data.cache.dirty import DirtyDictProcess
from mmm_da.lib.account.control import SYSTEM_ACCOUNT_ID
from mmm_da.db import DBApplyHelpInst, DBAcceptHelpInst
from mmm_da.lib.server_info import ServerInfoMgr
from mmm_da.lib.account.control import AccountMgr
from mmm_da.lib.help_pay.control import ApplyHelpPayMgr
from utils.service_control.parser import ArgumentParser
from setting import *


def is_using_system_accept():
    """
    判断是否使用系统接受帮助
    :return:
    """
    if ArgumentParser().args.force_mtype == "system":
        logger.warn("is_using_system_accept force use the system match!!!!")
        return True
    elif ArgumentParser().args.force_mtype == "user":
        logger.warn("is_using_system_accept force use the user match!!!!")
        return False
    # 系统默认使用用户匹配方式，系统匹配采用手动匹配方式
    return False


class AcceptHelpMgr(IManager):
    """
    接受帮助
    """
    __metaclass__ = Singleton

    def __init__(self):
        self.__oid_2_all_match_dic = {}         # accept_order <=> match dic
        self.__uid_2_user_match_dic = {}         # uid <=> match dic
        self.__oid_2_user_match_dic = {}         # iod <=> match dic

        self.__system_match_dic = None   # 系统接受帮助匹配
        self.__ddp = DirtyDictProcess(["accept_order"])

    def init_sql(self):
        # 完成的订单不加载
        return "SELECT * FROM accept_help WHERE accept_stat!=%s" % ACPS_FINISH

    def init(self, data_ls):
        self.__init__()

        for dic in data_ls:
            self.__add_data_2_mem(dic)

        assert self.__system_match_dic

    def update(self, curtime):
        dirty_dict = self.__ddp.get_db_dirty_dicts()
        DBAcceptHelpInst.update_ls(dirty_dict.get("update", []))
        DBAcceptHelpInst.insert_ls(dirty_dict.get("insert", []))

    def __add_data_2_mem(self, dic):
        """
        添加数据到mem
        :param dic:
        :return:
        """
        self.__oid_2_all_match_dic[dic['accept_order']] = dic

        if str(dic['accept_uid']) == str(SYSTEM_ACCOUNT_ID):
            self.__system_match_dic = dic
        else:
            self.__uid_2_user_match_dic.setdefault(dic['accept_uid'], {})[dic['accept_order']] = dic
            self.__oid_2_user_match_dic[dic['accept_order']] = dic

    def __del_data_2_mem(self, dic):
        """
        从mem删除数据
        :param dic:
        :return:
        """
        self.__oid_2_all_match_dic.pop(dic['accept_order'])
        self.__uid_2_user_match_dic.get(dic['accept_uid'], {}).pop(dic['accept_order'])
        self.__oid_2_user_match_dic.pop(dic['accept_order'])

    def __insert_dic(self, dic):
        """
        插入数据到mem/db
        :param dic: 数据字典
        :return:
        """
        self.__ddp.ist_db_dict(dic["accept_order"], dic)
        self.__add_data_2_mem(dic)

    def update_dic(self, order, dic):
        """
        更新数据到mem/db
        :param order:  接受帮助订单id
        :param dic:  更新数据字典
        :return:
        """
        self.__ddp.upd_db_dict(order, dic)

        cur_dic = self.get_data_by_order(order)
        if cur_dic:
            cur_dic.update(dic)

    def add_accept_help(self, accept_req_id, accept_uid, accept_money):
        """
        添加接受帮助
        :param accept_req_id: 接收帮助申请id
        :param accept_uid: 接受帮助用户id
        :param accept_money: 接受帮助金额
        :return:
        """
        # 接收帮助的订单id 就是接收帮助的请求id
        new_accept_order = accept_req_id
        data_dic = {'accept_order': new_accept_order,
                    'accept_uid': accept_uid,
                    'accept_stime': time.time(),
                    'accept_money': accept_money,
                    'accept_lmoney': accept_money,
                    'accept_stat': ACPS_MATCHING}
        self.__insert_dic(data_dic)
        return new_accept_order

    def match_ls(self):
        match_ls = [self.__system_match_dic] if is_using_system_accept() else self.__oid_2_user_match_dic.values()
        match_ls = filter(lambda dic: dic['accept_lmoney'] > 0 and not AccountMgr().get_data_by_id(dic['accept_uid']).is_seal,
                          match_ls)
        match_ls.sort(key=lambda x: x['accept_stime'])
        return match_ls

    def all_match_ls(self):
        match_ls = self.__oid_2_user_match_dic.values()
        match_ls.append(self.__system_match_dic)
        match_ls = filter(lambda dic: dic['accept_lmoney'] > 0 and not AccountMgr().get_data_by_id(dic['accept_uid']).is_seal,
                          match_ls)
        match_ls.sort(key=lambda x: x['accept_stime'])
        return match_ls

    def get_data_by_order(self, accept_order):
        """
        根据accept_order获取当前正在匹配的接受帮助信息
        :param accept_order: 接受帮助订单
        :return: [{}]
        """
        return self.__oid_2_all_match_dic[accept_order]

    def get_datas_by_uid(self, uid):
        """
        根据uid获取当前正在匹配的接受帮助信息
        :param uid: 用户id
        :return:
        """
        return [self.__system_match_dic] \
            if str(uid) == str(SYSTEM_ACCOUNT_ID) \
            else self.__uid_2_user_match_dic.get(uid, {}).values()

    def get_unfinish(self, uid):
        """
        获取uid对应的未完成的接受帮助匹配信息
        :param uid: uid
        :return: {}
        """
        # 完成订单不存在内存，所有留下的都是没有完成的订单
        unfinish_ls = [accept_help
                       for accept_help in self.get_datas_by_uid(uid)]

        assert len(unfinish_ls) <= 1
        return unfinish_ls[0] if len(unfinish_ls) ==1 else None

    def is_finished(self, accept_order):
        """
        判断接受帮助是否完成:
        1.剩余可接受金额为0
        2.所有申请帮助订单都确认支付就算完成
        :param accept_order:
        :return:
        """
        accept_help = self.get_data_by_order(accept_order)
        if accept_help['accept_lmoney'] != 0:
            return False

        return ApplyHelpPayMgr().is_accept_finished(accept_order)

    def do_accept(self, accept_order, apply_money):
        """
        接受帮助处理
        :param accept_order:接受帮助订单id
        :param apply_money: 申请帮助金钱
        :return:
        """
        assert apply_money > 0
        accept_help = self.__oid_2_all_match_dic.get(accept_order)
        accept_lmoney = accept_help['accept_lmoney'] - apply_money
        assert accept_lmoney >= 0

        upd_dic = {"accept_order": accept_order,
                   "accept_lmoney": accept_lmoney}

        self.update_dic(accept_order, upd_dic)

        # 总接受帮助总额增加
        ServerInfoMgr().attr_total_accept_money += apply_money

    def do_recover(self, accept_order, apply_money):
        """
        恢复处理
        :param accept_order:接受帮助订单id
        :param apply_money: 申请帮助金钱
        :return:
        """
        assert apply_money > 0
        accept_help = self.get_data_by_order(accept_order)
        accept_lmoney = accept_help['accept_lmoney'] + apply_money
        assert accept_lmoney > 0

        upd_dic = {"accept_order": accept_order,
                   "accept_lmoney": accept_lmoney}

        self.update_dic(accept_order, upd_dic)

    def do_confirm(self, accept_order):
        """
        申请帮助子订单确认收款，接受帮助确定收款处理，检查是否所有的订单都完成
        :param accept_order: 接受帮助子订单
        :return:
        """
        if self.is_finished(accept_order):
            self.do_finish(accept_order)

    def do_finish(self, accept_order):
        """
        接受帮助订单完成处理,完成的时候不能删除订单
        :param accept_order:接受帮助订单id
        :return:
        """
        upd_dic = {"accept_order": accept_order,
                   "accept_stat": ACPS_FINISH}
        self.update_dic(accept_order, upd_dic)

        # 订单完成数+1
        accept_help = self.get_data_by_order(accept_order)
        account = AccountMgr().get_data_by_id(accept_help['accept_uid'])
        account.attr_finished_accept += 1

        # 内存删除完成订单
        self.__del_data_2_mem(accept_help)

        # 添加等待申请帮助
        from mmm_da.lib.help_wait.control import ApplyHelpWaitMgr
        ApplyHelpWaitMgr().add_wait(accept_help['accept_uid'], time.time())


class ApplyHelpMgr(IManager):
    """
    申请帮助
    """
    __metaclass__ = Singleton

    def __init__(self):
        self.__id_2_dic = {}
        self.__uid_2_dic = {}
        self.__ddp = DirtyDictProcess(["apply_order"])

    def init_sql(self):
        # 完成的订单不加载
        return "SELECT * FROM apply_help WHERE apply_stat!=%s" % APYS_FINISH

    def init(self, data_ls):
        self.__init__()
        for dic in data_ls:
            self.__add_data_2_mem(dic)

    def update(self, curtime):
        dirty_dict = self.__ddp.get_db_dirty_dicts()
        DBApplyHelpInst.update_ls(dirty_dict.get("update", []))
        DBApplyHelpInst.insert_ls(dirty_dict.get("insert", []))

    def match_ls(self):
        match_ls = self.__id_2_dic.values()
        match_ls = filter(lambda dic: dic['apply_lmoney'] > 0 and not AccountMgr().get_data_by_id(dic['apply_uid']).is_seal,
                          match_ls)
        match_ls.sort(key=lambda x: x['apply_stime'])
        return match_ls

    def __add_data_2_mem(self, dic):
        self.__id_2_dic[dic['apply_order']] = dic
        self.__uid_2_dic.setdefault(dic['apply_uid'], {})[dic['apply_order']] = dic

    def __del_data_2_mem(self, dic):
        """
        从mem删除数据
        :param dic:
        :return:
        """
        self.__id_2_dic.pop(dic['apply_order'])
        self.__uid_2_dic.get(dic['apply_uid'], {}).pop(dic['apply_order'])

    def __insert_dic(self, dic):
        """
        插入数据到mem/db
        :param dic: 数据字典
        :return:
        """
        self.__ddp.ist_db_dict(dic["apply_order"], dic)
        self.__add_data_2_mem(dic)

    def update_dic(self, order, dic):
        """
        更新数据到mem/db
        :param order:  接受帮助订单id
        :param dic:  更新数据字典
        :return:
        """
        self.__ddp.upd_db_dict(order, dic)

        cur_dic = self.get_data_by_order(order)
        if cur_dic:
            cur_dic.update(dic)

    def get_datas_by_uid(self, uid):
        """
        获取uid对应的申请帮助匹配信息
        :param uid: uid
        :return: [{}]
        """
        return self.__uid_2_dic.get(uid, {}).values()

    def get_unfinish(self, uid):
        """
        获取uid对应的未完成的申请帮助匹配信息
        :param uid: uid
        :return: {}
        """
        # 完成订单不存在内存，所有留下的都是没有完成的订单
        unfinish_ls = [apply_help
                       for apply_help in self.get_datas_by_uid(uid)]

        assert len(unfinish_ls) <= 1
        return unfinish_ls[0] if len(unfinish_ls) ==1 else None

    def get_data_by_order(self, apply_order):
        """
        apply_order,
        :param apply_order:
        :return: {}
        """
        return self.__id_2_dic.get(apply_order)

    def add_apply_help(self, apply_order, apply_req_uid, apply_money, apply_rtime):
        """
        添加申请帮助请求
        :param apply_order:申请订单id
        :param apply_req_uid: 申请帮助用户id
        :param apply_money: 申请帮助金钱
        :param apply_rtime: 申请帮助请求排单时间，利息和请求时间以及开始时间有关
        :return:
        """
        data_dic = {'apply_order': apply_order,
                    'apply_uid': apply_req_uid,
                    'apply_stime': apply_rtime,
                    'apply_money': apply_money,
                    'apply_lmoney': apply_money,
                    'apply_stat': APYS_MATCHING}
        self.__insert_dic(data_dic)

    def do_apply(self, accept_order, apply_order, apply_sorder, apply_money):
        """
        申请帮助处理,同时产生一个申请帮助订单
        :param accept_order: 接受帮助订单id
        :param apply_order:申请帮助订单id
        :param apply_sorder:申请帮助子订单id，支付订单id
        :param apply_money: 申请帮助金钱
        :return:
        """
        assert apply_money > 0
        apply_help = self.get_data_by_order(apply_order)
        apply_lmoney = apply_help['apply_lmoney'] - apply_money
        assert apply_lmoney >= 0

        upd_dic = {"apply_order": apply_order,
                   "apply_lmoney": apply_lmoney}

        self.update_dic(apply_order, upd_dic)

        # 产生申请帮助支付信息
        ApplyHelpPayMgr().do_apply(apply_sorder, accept_order, apply_order, apply_money)

    def do_deny_pay(self, apply_order):
        """
        拒绝支付处理
        :param apply_order: 申请帮助订单id
        :return:
        """
        apply_help = self.get_data_by_order(apply_order)

        upd_dic = {"apply_order": apply_order,
                   "apply_stat": APYS_UNUSUAL}
        self.update_dic(apply_order, upd_dic)

    def do_recover(self, apply_order, apply_money):
        """
        恢复处理
        :param apply_order: 申请帮助订单id
        :param apply_money: 申请帮助金钱
        :return:
        """
        assert apply_money > 0
        apply_help = self.get_data_by_order(apply_order)
        apply_lmoney = apply_help['apply_lmoney'] + apply_money
        assert apply_lmoney >= 0

        upd_dic = {"apply_order": apply_order,
                   "apply_lmoney": apply_lmoney}

        self.update_dic(apply_order, upd_dic)

    def is_finished(self, apply_order):
        """
        判断申请帮助是否完成:
        1.剩余可接受金额为0
        2.所有申请帮助订单都确认支付就算完成
        :param apply_order:
        :return:
        """
        apply_help = self.get_data_by_order(apply_order)
        if apply_help['apply_lmoney'] != 0:
            return False

        return ApplyHelpPayMgr().is_apply_finished(apply_order)

    def do_confirm(self, apply_order):
        """
        申请帮助子订单确认收款，申请帮助确定收款处理，检查是否所有的订单都完成
        :param apply_order: 接受帮助子订单
        :return:
        """
        if self.is_finished(apply_order):
            self.do_finish(apply_order)

    def do_finish(self, apply_order):
        """
        申请帮助完成
        :param apply_order: 申请帮助订单id
        :return:
        """
        upd_dic = {"apply_order": apply_order,
                   "apply_stat": APYS_FINISH}
        self.update_dic(apply_order, upd_dic)

        # 增加完成订单数
        apply_help = self.get_data_by_order(apply_order)
        account = AccountMgr().get_data_by_id(apply_help['apply_uid'])
        account.attr_finished_apply += 1

        # 内存删除完成订单
        self.__del_data_2_mem(apply_help)
