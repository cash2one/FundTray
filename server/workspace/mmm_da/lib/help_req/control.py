#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-12-21

@author: Jay
"""
import time
from utils.interfaces.common import IManager
from utils.meta.singleton import Singleton
from utils.data.cache.dirty import DirtyDictProcess
from mmm_da.lib.filter.control import AcceptReqFilter, ApplyReqFilter
from mmm_da.db import DBApplyHelpReqInst, DBAcceptHelpReqInst
from mmm_da.lib.help.control import AcceptHelpMgr, ApplyHelpMgr
from mmm_da.lib.server_info import ServerInfoMgr
from mmm_da.lib.server_info import daysdiff
from setting import *
from utils import logger, error_code
from mmm_da.lib.formula import calc_match_coin
from mmm_da.lib.account.control import AccountMgr

class AcceptHelpReqMgr(IManager):
    """
    接受帮助
    """
    __metaclass__ = Singleton

    def __init__(self):
        self.__id_2_dic = {}            # id <=> dic
        self.__uid_2_dic = {}           # uid <=> dic
        self.__ddp = DirtyDictProcess(["id"])

    def init_sql(self):
        # 完成的订单不加载
        return "SELECT * FROM accept_help_req WHERE accept_req_stat!=%s" % ACPRS_FINISH

    def init(self, data_ls):
        self.__init__()
        for dic in data_ls:
            self.__add_data_2_mem(dic)

        filter_params = {}
        filter_params.setdefault("accept_match_min_days", ServerInfoMgr().attr_accept_match_min_days)
        filter_params.setdefault("days_diff_fun", daysdiff)
        AcceptReqFilter().init(self.req_ls, self.do_match, filter_params)

    def update(self, curtime):
        dirty_dict = self.__ddp.get_db_dirty_dicts()
        DBAcceptHelpReqInst.update_ls(dirty_dict.get("update", []))
        DBAcceptHelpReqInst.insert_ls(dirty_dict.get("insert", []))
        DBAcceptHelpReqInst.delete_ls(dirty_dict.get("delete", []))

    def req_ls(self):
        """
        获取请求的数据列表
        :return:
        """
        wait_ls = self.__id_2_dic.values()
        wait_ls = filter(lambda dic: not AccountMgr().get_data_by_id(dic['accept_req_uid']).is_seal,
                         wait_ls)
        return wait_ls

    def __add_data_2_mem(self, dic):
        self.__id_2_dic[dic['id']] = dic
        self.__uid_2_dic.setdefault(str(dic['accept_req_uid']), {})[dic['id']] = dic

    def __del_data_2_mem(self, dic):
        """
        从mem删除数据
        :param dic:
        :return:
        """
        self.__id_2_dic.pop(dic['id'])
        self.__uid_2_dic.get(str(dic['accept_req_uid']), {}).pop(dic['id'])

    def __insert_dic(self, dic):
        """
        插入数据到mem/db
        :param dic: 数据字典
        :return:
        """
        self.__ddp.ist_db_dict(dic['id'], dic)
        self.__add_data_2_mem(dic)

    def __update_dic(self, id, dic):
        """
        更新数据到mem/db
        :param id:  接受帮助请求id
        :param dic:  更新数据字典
        :return:
        """
        self.__ddp.upd_db_dict(dic['id'], dic)

        cur_dic = self.get_data_by_id(id)
        if cur_dic:
            cur_dic.update(dic)

    def get_data_by_id(self, id):
        return self.__id_2_dic.get(id)

    def get_datas_by_uid(self, uid):
        return self.__uid_2_dic.get(str(uid), {}).values()

    def get_unfinish(self, uid):
        """
        获取uid对应的未完成的接受帮助请求匹配信息
        :param uid: uid
        :return: {}
        """
        unfinish_ls = [accept_help_req
                       for accept_help_req in self.get_datas_by_uid(uid)
                       if accept_help_req['accept_req_stat'] not in [ACPRS_FINISH]]

        assert len(unfinish_ls) <= 1
        return unfinish_ls[0] if len(unfinish_ls) ==1 else None

    def add_req(self, accept_req_uid, accept_req_money):
        """
        添加接受帮助请求
        :param accept_req_uid: 接受帮助请求用户id
        :param accept_req_money: 接受帮助请求金额
        :return:
        """
        data_dic = {'id': ServerInfoMgr().make_unique_id(),
                    'accept_req_uid': str(accept_req_uid),
                    'accept_req_time': time.time(),
                    'accept_req_money': accept_req_money,
                    'accept_req_stat': ACPRS_REQUEST}
        self.__insert_dic(data_dic)

        # 增加接受帮助总次数
        ServerInfoMgr().attr_total_accept_cnt += 1

    def del_req(self, req_id):
        """
        删除请求队列
        :param req_id:
        :return:
        """
        self.__del_data_2_mem(self.get_data_by_id(req_id))
        self.__ddp.del_db_dict(req_id, {"id": req_id})

        # 减少接受帮助总次数
        ServerInfoMgr().attr_total_accept_cnt -= 1

    def do_match(self, id):
        """
        进入匹配队列
        :param id: 进入匹配的id
        :return:
        """
        accept_dic = self.get_data_by_id(id)

        # upd data
        upd_dic = {"id": id,
                   "accept_req_stat": ACPRS_FINISH}
        self.__update_dic(id, upd_dic)

        # 接受帮助请求完成的时候可以删除内存
        self.__del_data_2_mem(accept_dic)

        # 减少接受帮助总次数
        ServerInfoMgr().attr_total_accept_cnt -= 1

        # 加入接受帮助管理器
        AcceptHelpMgr().add_accept_help(accept_dic['id'], accept_dic['accept_req_uid'], accept_dic['accept_req_money'])


class ApplyHelpReqMgr(IManager):
    """
    申请帮助
    """
    __metaclass__ = Singleton

    def __init__(self):
        self.__id_2_dic = {}                    # id <=> dic
        self.__uid_2_dic = {}                   # uid <=> dic

        self.__ddp = DirtyDictProcess(["id"])

    def init_sql(self):
        # 完成的订单不加载
        return " SELECT * FROM apply_help_req WHERE apply_req_stat !=%s" % APYRS_FINISH

    def init(self, data_ls):
        self.__init__()

        for dic in data_ls:
            self.__add_data_2_mem(dic)

        filter_params = {}
        filter_params.setdefault("apply_match_min_days", ServerInfoMgr().attr_apply_match_min_days)
        filter_params.setdefault("days_diff_fun", daysdiff)
        ApplyReqFilter().init(self.req_ls,  self.do_match, filter_params)

    def update(self, curtime):
        dirty_dict = self.__ddp.get_db_dirty_dicts()
        DBApplyHelpReqInst.update_ls(dirty_dict.get("update", []))
        DBApplyHelpReqInst.insert_ls(dirty_dict.get("insert", []))
        DBApplyHelpReqInst.delete_ls(dirty_dict.get("delete", []))

    def req_ls(self):
        """
        获取请求的数据列表
        :return:
        """
        wait_ls = self.__id_2_dic.values()
        wait_ls = filter(lambda dic: not AccountMgr().get_data_by_id(dic['apply_req_uid']).is_seal,
                         wait_ls)
        return wait_ls

    def __add_data_2_mem(self, dic):
        self.__id_2_dic[dic['id']] = dic
        self.__uid_2_dic.setdefault(dic['apply_req_uid'], {})[dic['id']] = dic

    def __del_data_2_mem(self, dic):
        """
        从mem删除数据
        :param dic:
        :return:
        """
        self.__id_2_dic.pop(dic['id'], None)
        self.__uid_2_dic.get(dic['apply_req_uid'], {}).pop(dic['id'], None)

    def __insert_dic(self, dic):
        """
        插入数据到mem/db
        :param dic: 数据字典
        :return:
        """
        self.__ddp.ist_db_dict(dic['id'], dic)
        self.__add_data_2_mem(dic)

    def __update_dic(self, id, dic):
        """
        更新数据到mem/db
        :param id:  接受帮助请求id
        :param dic:  更新数据字典
        :return:
        """
        self.__ddp.upd_db_dict(id, dic)

        cur_dic = self.get_data_by_id(id)
        if cur_dic:
            cur_dic.update(dic)

    def add_req(self, apply_req_uid, apply_req_money):
        """
        添加申请帮助请求
        :param apply_req_uid: 申请帮助请求用户id
        :param apply_req_money: 申请帮助请求金额
        :return:
        """
        data_dic = {'id': ServerInfoMgr().make_unique_id(),
                    'apply_req_uid': apply_req_uid,
                    'apply_req_time': time.time(),
                    'apply_req_money': apply_req_money,
                    'apply_req_stat': APYRS_REQUEST}
        self.__insert_dic(data_dic)

        # 总申请帮助次数增加
        ServerInfoMgr().attr_total_apply_cnt += 1

    def del_req(self, req_id):
        """
        删除请求队列
        :param req_id:
        :return:
        """
        self.__del_data_2_mem(self.get_data_by_id(req_id))
        self.__ddp.del_db_dict(req_id, {"id": req_id})

        # 请求队列个数减少
        ServerInfoMgr().attr_total_apply_cnt -= 1

    def get_data_by_id(self, id):
        """
        根据id获取信息
        :param id:
        :return:
        """
        return self.__id_2_dic.get(id)

    def get_datas_by_uid(self, uid):
        """
        根据用户id获取信息列表
        :param uid:
        :return:
        """
        return self.__uid_2_dic.get(uid, {}).values()

    def get_unfinish(self, uid):
        """
        获取uid对应的未完成的申请帮助请求匹配信息
        :param uid: uid
        :return: {}
        """
        unfinish_ls = [apply_help_req
                       for apply_help_req in self.get_datas_by_uid(uid)
                       if apply_help_req['apply_req_stat'] not in [APYRS_FINISH]]

        assert len(unfinish_ls) <= 1
        return unfinish_ls[0] if len(unfinish_ls) ==1 else None

    def get_unfinishs(self):
        """
        获取所有未完成的申请帮助请求信息
        :return:
        """
        return self.__id_2_dic.values()

    def do_req(self, account, apply_money):
        """
        请求处理
        :param account:
        :param apply_money:
        :return: error_code
        """
        apply_money = int(apply_money)
        if apply_money < MIN_APPLY_HELP_MONEY or apply_money > MAX_APPLY_HELP_MONEY:
            logger.info("apply_help ERROR_LOGIC, not valid apply_money:%s must > %s and < %s" %
                        (apply_money, MIN_APPLY_HELP_MONEY, MAX_APPLY_HELP_MONEY))
            return error_code.ERROR_LOGIC

        # 投资必须为1000的整数倍
        if apply_money % 1000 != 0:
            logger.info("apply_help ERROR_LOGIC, not times of 1000:%s" % apply_money)
            return error_code.ERROR_LOGIC

        # 还在请求处理，
        if ApplyHelpReqMgr().get_unfinish(account.id):
            logger.info("apply_help ERROR_LOGIC, has ApplyHelpReqMgr!!!, id:%s" % account.id)
            return error_code.ERROR_LOGIC

        # 还在匹配处理
        if ApplyHelpMgr().get_datas_by_uid(account.id):
            logger.info("apply_help ERROR_LOGIC, has ApplyHelpMgr!!!, id:%s" % account.id)
            return error_code.ERROR_LOGIC

        # 投资额必须大于等于之前累计投资额
        if apply_money < account.attr_max_apply_money:
            logger.info("apply_help ERROR_LOGIC, apply_money:%s must big than max_apply_money:%s!!!, id:%s"
                        % (apply_money, account.attr_max_apply_money, account.id))
            return error_code.ERROR_MAX_APPLY_HELP_LESS

        # 排单币不够
        must_match_coin = calc_match_coin(apply_money)
        if account.attr_match_coin <= must_match_coin:
            logger.info("apply_help ERROR_LOGIC, not enouth match coin!!!, id:%s, match_coin:%s, must_match_coin:%s, apply_money:%s"
                        % (account.id, account.attr_match_coin, must_match_coin, apply_money))
            return error_code.EEROR_MATCH_COIN_LACK

        # 添加申请帮助请求
        self.add_req(account.id, apply_money)

        # 设置最大投资额
        account.attr_max_apply_money = apply_money

        # 扣除排单币
        account.attr_match_coin -= must_match_coin

        # 判断是否有等待申请帮助，如果有则删除对应等待
        from mmm_da.lib.help_wait.control import ApplyHelpWaitMgr
        ApplyHelpWaitMgr().del_wait(account.id)

        return error_code.ERROR_SUCCESS

    def do_match(self, id):
        """
        进入匹配队列处理
        :param id: id
        :return:
        """
        # upd data
        upd_dic = {'id': id, 'apply_req_stat': APYRS_FINISH}

        self.__update_dic(id, upd_dic)

        # 请求队列个数减少
        ServerInfoMgr().attr_total_apply_cnt -= 1

        # 加入申请帮助管理器,进入匹配队列
        apply_req_dic = self.get_data_by_id(id)
        ApplyHelpMgr().add_apply_help(apply_req_dic['id'],
                                      apply_req_dic['apply_req_uid'],
                                      apply_req_dic['apply_req_money'],
                                      apply_req_dic['apply_req_time'])

        # 从匹配队列删除
        self.__del_data_2_mem(self.get_data_by_id(id))