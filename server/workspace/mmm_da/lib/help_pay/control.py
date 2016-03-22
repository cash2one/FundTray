#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2016-2-24

@author: Jay
"""
import time
from utils import logger
from utils.service_control.parser import ArgumentParser
from utils.interfaces.common import IManager
from utils.meta.singleton import Singleton
from utils.data.cache.dirty import DirtyDictProcess
from mmm_da.db import DBApplyHelpPayInst
from mmm_da.lib.server_info import ServerInfoMgr
from mmm_da.lib.bonus import BonusMgr
from mmm_da.lib.nginx import rm_pay_pic
from mmm_da.lib.help_pay.setting import *
from mmm_da.lib.account.control import AccountMgr
from mmm_da.lib.account.model import SEALED
from mmm_da.lib.filter.control import ApplyPayFilter
from mmm_da.lib.server_info import daysdiff


class ApplyHelpPayMgr(IManager):
    """
    申请帮助支付管理器
    """
    __metaclass__ = Singleton

    def __init__(self):
        self.__apply_sorder_2_dic = {}          # apply_sorder <=> dic
        self.__apply_order_2_dic = {}           # apply_order <=> dic
        self.__accept_order_2_dic = {}          # accept_order <=> dic

        self.__ddp = DirtyDictProcess(["apply_sorder"])

    def init_sql(self):
        # 完成/取消/异常的订单不加载
        # 申请帮助同一订单没有全部支付完成的都要加载，部分完成的也要加载
        # 接受帮助同一订单没有全部支付完成的都要加载，部分完成的也要加载
        from mmm_da.lib.help.setting import APYS_FINISH, ACPS_FINISH
        apply_pay_condition = ",".join([str(APYS_PAY_FINISH)])
        return "SELECT * FROM apply_help_pay WHERE apply_pstat NOT IN (%s) "% (apply_pay_condition)

    def init(self, data_ls):
        self.__init__()

        for dic in data_ls:
            self.__add_data_2_mem(dic)

        filter_params = {}
        filter_params.setdefault("apply_pay_max_days", ServerInfoMgr().attr_apply_pay_max_days)
        filter_params.setdefault("days_diff_fun", daysdiff)
        ApplyPayFilter().init(self.apply_wait_ls,  self.do_deny_pay, filter_params)

    def update(self, curtime):
        dirty_dict = self.__ddp.get_db_dirty_dicts()
        DBApplyHelpPayInst.update_ls(dirty_dict.get("update", []))
        DBApplyHelpPayInst.insert_ls(dirty_dict.get("insert", []))

    def apply_wait_ls(self):
        """
        获取等待支付的数据列表
        :return:
        """
        wait_ls = self.__apply_sorder_2_dic.values()
        wait_ls = filter(lambda dic: dic['apply_pstat'] == APYS_PAY_WAIT, wait_ls)
        return wait_ls

    def __add_data_2_mem(self, dic):
        """
        添加数据到mem
        :param dic:
        :return:
        """
        self.__apply_sorder_2_dic[dic['apply_sorder']] = dic
        self.__apply_order_2_dic.setdefault(dic['apply_order'], {})[dic['apply_sorder']] = dic
        self.__accept_order_2_dic.setdefault(dic['accept_order'], {})[dic['apply_sorder']] = dic

    def __del_data_2_mem(self, dic):
        """
        从mem删除数据
        :param dic:
        :return:
        """
        self.__apply_sorder_2_dic.pop(dic['apply_sorder'])
        self.__apply_order_2_dic.get(dic['apply_order'], {}).pop(dic['apply_sorder'])
        self.__accept_order_2_dic.get(dic['accept_order'], {}).pop(dic['apply_sorder'])

    def __insert_dic(self, dic):
        """
        插入数据到mem/db
        :param dic: 数据字典
        :return:
        """
        self.__ddp.ist_db_dict(dic["apply_sorder"], dic)
        self.__add_data_2_mem(dic)

    def update_dic(self, apply_sorder, dic):
        """
        更新数据到mem/db
        :param apply_sorder:  申请帮助子订单id
        :param dic:  更新数据字典
        :return:
        """
        self.__ddp.upd_db_dict(apply_sorder, dic)

        cur_dic = self.get_data_by_sorder(apply_sorder)
        if cur_dic:
            cur_dic.update(dic)

    def get_data_by_sorder(self, apply_sorder):
        """
        获取apply_sorder对应的申请帮助支付信息,
        :param apply_sorder:
        :return: {}
        """
        return self.__apply_sorder_2_dic.get(apply_sorder)

    def get_datas_by_accept_order(self, accept_order):
        """
        根据接受帮助订单id获取所有申请帮助支付信息
        :param accept_order:
        :return: [apply_help_pay_dic,,,,]
        """
        return self.__accept_order_2_dic.get(accept_order, {}).values()

    def get_datas_by_apply_order(self, apply_order):
        """
        根据申请帮助订单id获取所有申请帮助支付信息
        :param apply_order:
        :return: [apply_help_pay_dic,,,,]
        """
        return self.__apply_order_2_dic.get(apply_order, {}).values()

    def is_confirmed(self, apply_sorder):
        """
        判断申请帮助是否确认支付
        :param apply_sorder:
        :return:
        """
        apply_help_pay = self.get_data_by_sorder(apply_sorder)
        assert apply_help_pay, apply_sorder
        return apply_help_pay['apply_pstat'] == APYS_PAY_CFRM

    def is_accept_finished(self, accept_order):
        """
        判断接受帮助订单是否全部完成:
        1.所有支付订单都确认支付就算完成
        :param accept_order: 接受帮助订单
        :return:
        """
        apply_help_pays = self.get_datas_by_accept_order(accept_order)
        for apply_help_pay in apply_help_pays:
            if not self.is_confirmed(apply_help_pay['apply_sorder']):
                return False
        return True

    def is_apply_finished(self, apply_order):
        """
        判断申请帮助订单是否全部完成:
        1.所有支付订单都确认支付就算完成
        :param apply_order: 申请帮助订单
        :return:
        """
        apply_help_pays = self.get_datas_by_apply_order(apply_order)
        for apply_help_pay in apply_help_pays:
            if not self.is_confirmed(apply_help_pay['apply_sorder']):
                return False
        return True

    def do_apply(self, apply_sorder, accept_order, apply_order, apply_pmoney):
        """
        申请帮助处理, 产生一个申请帮助支付的订单
        :param apply_sorder: 申请子订单id
        :param accept_order:接受订单id
        :param apply_order:申请订单id
        :param apply_pmoney: 申请帮助金钱
        :return:
        """
        data_dic = {'apply_sorder': apply_sorder,
                    'accept_order': accept_order,
                    'apply_order': apply_order,
                    'apply_mtime': time.time(),
                    'apply_pmoney': apply_pmoney,
                    'apply_interest': ServerInfoMgr().attr_apply_interest,
                    'apply_pstat': APYS_PAY_WAIT}
        self.__insert_dic(data_dic)

        # 总申请帮助总额增加
        ServerInfoMgr().attr_total_apply_money += apply_pmoney

    def do_pay(self, apply_sorder, pay_piture, pay_msg):
        """
        支付处理
        :param apply_sorder: 申请帮助子订单id
        :param pay_piture: 申请帮助支付截图
        :param pay_msg: 申请帮助支付消息
        :return:
        """
        upd_dic = {'apply_sorder': apply_sorder,
                   'apply_ptime': time.time(),
                   'apply_piture': pay_piture,
                   'apply_message': pay_msg,
                   'apply_pstat': APYS_PAY_SUCCESS}

        self.update_dic(apply_sorder, upd_dic)

        # 支付奖励处理
        BonusMgr().on_apply_pay(apply_sorder)

    def do_confirm(self, apply_sorder):
        """
        确定收款处理, 订单完成
        :param apply_sorder: 申请帮助子订单id
        :return:
        """
        from mmm_da.lib.help.control import ApplyHelpMgr
        upd_dic = {"apply_sorder": apply_sorder,
                   "apply_pstat": APYS_PAY_CFRM}
        self.update_dic(apply_sorder, upd_dic)

        # 确认奖励处理
        BonusMgr().on_confirm_pay(apply_sorder)

        apply_help_pay_dic = self.get_data_by_sorder(apply_sorder)

        # 添加马夫罗到钱包余额
        apply_help_dic = ApplyHelpMgr().get_data_by_order(apply_help_pay_dic['apply_order'])

        assert apply_help_dic
        account = AccountMgr().get_data_by_id(apply_help_dic['apply_uid'])

        account.attr_mafuluo += BonusMgr().on_extract_pi(apply_sorder)

        # 排单币返还成钱包余额
        account.attr_mafuluo += BonusMgr().match_coin_back(apply_sorder)

        # 订单完成
        self.do_finish(apply_sorder)

    def do_deny_pay(self, apply_sorder):
        """
        拒绝支付处理
        :param apply_sorder: 申请帮助子订单id
        :return:
        """
        from mmm_da.lib.help.control import ApplyHelpMgr, AcceptHelpMgr
        apply_help_pay_dic = self.get_data_by_sorder(apply_sorder)
        assert apply_help_pay_dic

        apply_help_dic = ApplyHelpMgr().get_data_by_order(apply_help_pay_dic['apply_order'])

        # 封号
        account = AccountMgr().get_data_by_id(apply_help_dic['apply_uid'])
        account.attr_stat = SEALED

        # 接受帮助/申请帮助恢复
        AcceptHelpMgr().do_recover(apply_help_pay_dic['accept_order'], apply_help_pay_dic['apply_pmoney'])
        ApplyHelpMgr().do_recover(apply_help_pay_dic['apply_order'], apply_help_pay_dic['apply_pmoney'])

        # 未支付奖金处理
        BonusMgr().on_apply_cancel(apply_help_dic['apply_uid'], apply_help_pay_dic['apply_pmoney'])

        upd_dic = {"apply_sorder": apply_sorder,
                   "apply_pstat": APYS_PAY_REFUSE}
        self.update_dic(apply_sorder, upd_dic)

    def do_noreceived(self, apply_sorder):
        """
        申请帮助方已经支付，到时接受帮助方未收到，系统处于订单异常状态，等待客服处理
        :param apply_sorder: 申请帮助子订单id
        :return:
        """
        upd_dic = {"apply_sorder": apply_sorder,
                   "apply_pstat": APYS_PAY_UNUSUAL}
        self.update_dic(apply_sorder, upd_dic)

    def do_finish(self, apply_sorder):
        """
        申请帮助完成
        :param apply_sorder: 申请帮助子订单id
        :return:
        """
        upd_dic = {"apply_sorder": apply_sorder,
                   "apply_pstat": APYS_PAY_FINISH}
        self.update_dic(apply_sorder, upd_dic)

        from mmm_da.lib.help.control import ApplyHelpMgr
        apply_help_pay_dic = self.get_data_by_sorder(apply_sorder)
        apply_help = ApplyHelpMgr().get_data_by_order(apply_help_pay_dic['apply_order'])

        # 删除支付截图
        if apply_help_pay_dic['apply_piture']:
            file_name = apply_help_pay_dic['apply_piture'].split("/")[-1]
            pic_store_path = "%s/%s" % (ArgumentParser().args.pic_store_path, file_name)

            logger.info("ApplyHelpMgr::do_finish del pic_store_path:%s " % pic_store_path)
            rm_pay_pic(pic_store_path)

        # 订单完成奖励
        BonusMgr().on_apply_finish(apply_help['apply_uid'], apply_help_pay_dic['apply_pmoney'])

        # 内存删除完成订单
        self.__del_data_2_mem(apply_help_pay_dic)
