#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-12-19

@author: Jay
"""
import time
import ujson
from utils.interfaces.common import IManager
from utils.meta.singleton import Singleton
from utils.comm_func import sub_dict
from utils.data.cache.dirty import DirtyDictProcess
from utils.service_control.parser import ArgumentParser
from utils import logger
from mmm_da.lib.formula import daysdiff



KEY_SET = set(["start_time", "apply_match_min_days", "apply_match_max_days",
               "apply_pay_max_days", "accept_match_min_days",
               "apply_interest", "pay_reward_dic", "cfmd_reward_dic",
               "min_account_id", "notice",
               "active_coin_loss", "match_coin_loss", "apply_paid_reward", "apply_unpaid_punish",
               "system_balance", "total_apply_money", "total_accept_money",
               "min_unique_id",
               "total_apply_cnt","total_accept_cnt","total_apply_factor","total_accept_factor",
               "apply_aft_accept_hour"])

CAN_UPDAET_KEY_SET = set(["apply_match_min_days", "apply_match_max_days",
                          "apply_pay_max_days", "accept_match_min_days",
                          "apply_interest", "pay_reward_dic", "cfmd_reward_dic","notice",
                          "active_coin_loss", "match_coin_loss", "apply_paid_reward", "apply_unpaid_punish",
                          "system_balance",
                          "total_apply_cnt","total_accept_cnt","total_apply_factor","total_accept_factor",
                          "apply_aft_accept_hour"])

JSON_KEY_SET = set(["pay_reward_dic", "cfmd_reward_dic"])

PRIVATE_KEY = "start_time"

class ServerInfoMgr(IManager):
    __metaclass__ = Singleton

    def init(self, data_ls):
        assert data_ls
        self.__dict__ = data_ls[0]
        self.ddp = DirtyDictProcess([])

        self.pay_reward_dic = ujson.loads(self.pay_reward_dic)
        self.cfmd_reward_dic = ujson.loads(self.cfmd_reward_dic)
        logger.warn("ServerInfoMgr::init __dict__:%s" % sub_dict(self.__dict__, KEY_SET))

    def update(self, curtime):
        dirty_dic = self.ddp.get_db_dirty_dicts()
        dirty_upd_ls = dirty_dic.get("update", [])
        if dirty_upd_ls:
            # 增加主键key
            map(lambda dic: dic.update({PRIVATE_KEY: self.attr_start_time}), dirty_upd_ls)
            from mmm_da.db import DBServerInfoInst
            DBServerInfoInst.update_ls(dirty_upd_ls)

    def past_days_2_now(self):
        """
        判断系统启动距离当前的天数
        :return:
        """
        return daysdiff(time.time(), self.attr_start_time)

    def get_info_dic(self):
        """
        获取所有信息
        :return:
        """
        return sub_dict(self.__dict__, KEY_SET)

    @property
    def attr_start_time(self):
        return self.start_time

    @property
    def attr_apply_match_min_days(self):
        """
        申请帮助至少匹配时间(天)
        :return:
        """
        return self.apply_match_min_days

    @property
    def attr_apply_match_max_days(self):
        """
        申请帮助最多匹配时间(天)
        :return:
        """
        return self.apply_match_max_days

    @property
    def attr_apply_pay_max_days(self):
        """
        申请帮助最多支付时间(天)
        :return:
        """
        return self.apply_pay_max_days

    @property
    def attr_accept_match_min_days(self):
        """
        接受帮助至少匹配时间(天)
        :return:
        """
        return self.accept_match_min_days

    @property
    def attr_apply_interest(self):
        """
        申请帮助利息(百分比)
        :return:
        """
        return self.apply_interest

    @property
    def attr_pay_reward_dic(self):
        """
        支付奖励字典 {及时支付时间:奖励利息百分比,,,,}
        :return:
        """
        return self.pay_reward_dic

    @property
    def attr_cfmd_reward_dic(self):
        """
        支付确认奖励字典 {及时支付时间:奖励利息百分比,,,,}
        :return:
        """
        return self.cfmd_reward_dic

    @property
    def attr_day_seconds(self):
        """
        一天的秒数
        :return:
        """
        return ArgumentParser().args.day_seconds if ArgumentParser().args.day_seconds else self.day_seconds

    #min_account_id
    @property
    def attr_min_account_id(self):
        """
        获取最小的account id
        :return:
        """
        return self.min_account_id

    @attr_min_account_id.setter
    def attr_min_account_id(self, new_id):
        assert new_id > self.attr_min_account_id

        self.min_account_id = new_id
        self.ddp.upd_db_dict(self.attr_start_time, {"min_account_id": self.min_account_id})

    #notice
    @property
    def attr_notice(self):
        return self.notice

    @attr_notice.setter
    def attr_notice(self, notice):
        self.notice = notice
        self.ddp.upd_db_dict(self.attr_start_time, {"notice": self.notice})

    #active_coin_loss
    @property
    def attr_active_coin_loss(self):
        return self.active_coin_loss

    #match_coin_loss
    @property
    def attr_match_coin_loss(self):
        return self.match_coin_loss

    #apply_paid_reward
    @property
    def attr_apply_paid_reward(self):
        return self.apply_paid_reward

    #apply_unpaid_punish
    @property
    def attr_apply_unpaid_punish(self):
        return self.apply_unpaid_punish

    #system_balance
    @property
    def attr_system_balance(self):
        return self.system_balance

    #total_apply_money
    @property
    def attr_total_apply_money(self):
        return self.total_apply_money

    @attr_total_apply_money.setter
    def attr_total_apply_money(self, new_total_apply_money):
        if self.total_apply_money == new_total_apply_money:
            return

        self.total_apply_money = new_total_apply_money
        self.ddp.upd_db_dict(self.attr_start_time, {"total_apply_money": self.total_apply_money})

    #total_accept_money
    @property
    def attr_total_accept_money(self):
        return self.total_accept_money

    @attr_total_accept_money.setter
    def attr_total_accept_money(self, new_total_accept_money):
        if self.total_accept_money == new_total_accept_money:
            return

        self.total_accept_money = new_total_accept_money
        self.ddp.upd_db_dict(self.attr_start_time, {"total_accept_money": self.total_accept_money})

    #total_apply_cnt
    @property
    def attr_total_apply_cnt(self):
        # 增加因子
        apply_cnt = self.total_apply_cnt + self.attr_total_apply_factor
        if apply_cnt < 0:
            apply_cnt = 0
        return apply_cnt

    @attr_total_apply_cnt.setter
    def attr_total_apply_cnt(self, new_total_apply_cnt):
        """
        设置总申请帮助次数
        :param new_total_apply_cnt: 申请帮助次数，包括接受帮助因子
        :return:
        """
        # 减少因子
        new_total_apply_cnt -= self.attr_total_apply_factor
        if new_total_apply_cnt < 0:
            new_total_apply_cnt = 0
        if self.total_apply_cnt == new_total_apply_cnt:
            return

        self.total_apply_cnt = new_total_apply_cnt
        self.ddp.upd_db_dict(self.attr_start_time, {"total_apply_cnt": self.total_apply_cnt})

    #total_accept_cnt
    @property
    def attr_total_accept_cnt(self):
        # 增加因子
        accept_cnt = self.total_accept_cnt + self.attr_total_accept_factor
        if accept_cnt < 0:
            accept_cnt = 0
        return accept_cnt

    @attr_total_accept_cnt.setter
    def attr_total_accept_cnt(self, new_total_accept_cnt):
        """
        设置总接受帮助次数
        :param new_total_apply_cnt: 接受帮助次数，包括接受帮助因子
        :return:
        """
        # 减少因子
        new_total_accept_cnt -= self.attr_total_accept_factor
        if new_total_accept_cnt < 0:
            new_total_accept_cnt = 0
        if self.total_accept_cnt == new_total_accept_cnt:
            return

        self.total_accept_cnt = new_total_accept_cnt
        self.ddp.upd_db_dict(self.attr_start_time, {"total_accept_cnt": self.total_accept_cnt})

    #total_apply_factor
    @property
    def attr_total_apply_factor(self):
        return self.total_apply_factor

    @attr_total_apply_factor.setter
    def attr_total_apply_factor(self, new_total_apply_factor):
        if self.total_apply_factor == new_total_apply_factor:
            return

        self.total_apply_factor = new_total_apply_factor
        self.ddp.upd_db_dict(self.attr_start_time, {"total_apply_factor": self.total_apply_factor})

    #total_accept_factor
    @property
    def attr_total_accept_factor(self):
        return self.total_accept_factor

    @attr_total_accept_factor.setter
    def attr_total_accept_factor(self, new_total_accept_factor):
        if self.total_accept_factor == new_total_accept_factor:
            return

        self.total_accept_factor = new_total_accept_factor
        self.ddp.upd_db_dict(self.attr_start_time, {"total_accept_factor": self.total_accept_factor})

    #min_unique_id
    @property
    def attr_min_unique_id(self):
        """
        获取最小的唯一id
        :return:
        """
        return self.min_unique_id

    @attr_min_unique_id.setter
    def attr_min_unique_id(self, new_id):
        assert new_id > self.attr_min_unique_id

        self.min_unique_id = new_id
        self.ddp.upd_db_dict(self.attr_start_time, {"min_unique_id": self.min_unique_id})

    def make_unique_id(self):
        """
        获取唯一id
        :return:
        """
        unique_id = "id%s" % self.attr_min_unique_id
        self.attr_min_unique_id +=1
        return unique_id

    #apply_aft_accept_hour
    @property
    def attr_apply_aft_accept_hour(self):
        return self.apply_aft_accept_hour

    @attr_apply_aft_accept_hour.setter
    def attr_apply_aft_accept_hour(self, new_apply_aft_accept_hour):
        if self.apply_aft_accept_hour == new_apply_aft_accept_hour:
            return

        self.apply_aft_accept_hour = new_apply_aft_accept_hour
        self.ddp.upd_db_dict(self.attr_start_time, {"apply_aft_accept_hour": self.apply_aft_accept_hour})

    def update_value(self, field, value):
        assert field in CAN_UPDAET_KEY_SET

        if field in self.__dict__:
            if field in JSON_KEY_SET:
                try:
                    self.__dict__[field] = ujson.loads(value)
                except:
                    logger.warn("ServerInfoMgr::update_value Failed!!!!  field:%s value:%s" %(field, value))
                    return
            else:
                try:
                    self.__dict__[field] = int(value)
                except:
                    self.__dict__[field] = value
            self.ddp.upd_db_dict(self.attr_start_time, {field: value})


