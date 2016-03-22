#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2016-1-8

@author: Jay
"""
import time
from utils.interfaces.common import IManager
from utils.meta.singleton import Singleton
from utils.data.cache.dirty import DirtyDictProcess
from mmm_da.db import DBBonusLogInst
from setting import *
from utils import logger
from mmm_da.lib.server_info import ServerInfoMgr
from mmm_da.lib.formula import calc_pi, calc_match_coin

# 1代10%, 2代3%, 3代2%, 4代1%，5代%0.5， 6代到无限代0.25%
BONUS_RATE_LV = [10, 3, 2, 1, 0.5]
MIN_BONUS_RATE = 0.25

BONUS_PAGE_COUNT = 30

class BonusMgr(IManager):
    """
    奖金管理器
    """
    __metaclass__ = Singleton

    def __init__(self):
        pass

    def on_extract_pi(self, apply_sorder):
        """
        计算本息: 计息间隔:申请帮助开始时间到申请帮助匹配时间
        :param apply_sorder: 申请帮助子订单id
        :return:
        """
        from mmm_da.lib.help_pay.control import ApplyHelpPayMgr
        from mmm_da.lib.help.control import ApplyHelpMgr

        assert ApplyHelpPayMgr().is_confirmed(apply_sorder)
        apply_help_pay_dic = ApplyHelpPayMgr().get_data_by_sorder(apply_sorder)
        apply_help_dic = ApplyHelpMgr().get_data_by_order(apply_help_pay_dic['apply_order'])

        # apply_req_time 就是申请帮助请求时间
        # apply_stime 就是申请帮助请求匹配时间，也即申请帮助开始时间
        pi = calc_pi(apply_help_pay_dic['apply_pmoney'],
                     apply_help_pay_dic['apply_interest'],
                     apply_help_dic['apply_stime'],
                     apply_help_pay_dic['apply_mtime'])
        assert pi
        logger.info("BonusMgr::on_extract_pi apply_money:%s apply_interest:%s days_diff:%s pi:%s" %
                    (apply_help_pay_dic['apply_pmoney'],
                     apply_help_pay_dic['apply_interest'],
                     apply_help_dic['apply_stime'] - apply_help_pay_dic['apply_mtime'],
                     pi))
        return pi

    def on_apply_pay(self, apply_sorder):
        """
        支付奖励处理:奖励利息
        :param apply_sorder: 申请帮助子订单id
        :return:
        """
        from mmm_da.lib.server_info import ServerInfoMgr, daysdiff
        from mmm_da.lib.help_pay.control import ApplyHelpPayMgr
        from mmm_da.lib.help.control import ApplyHelpMgr
        apply_help_pay_dic = ApplyHelpPayMgr().get_data_by_sorder(apply_sorder)
        apply_help_dic = ApplyHelpMgr().get_data_by_order(apply_help_pay_dic['apply_order'])

        days2pay = daysdiff(time.time(), apply_help_dic['apply_stime'])
        for reward_hour, reward_int in ServerInfoMgr().attr_pay_reward_dic.items():
            reward_hour = float(reward_hour)
            if days2pay <= reward_hour:
                upd_dic = {"apply_sorder":apply_sorder,
                           "apply_interest": apply_help_pay_dic['apply_interest'] + reward_int}
                ApplyHelpPayMgr().update_dic(apply_sorder, upd_dic)

                logger.warn("BonusMgr::on_apply_pay reward!!!, reward_hour:%s, reward_int:%s "
                            % (reward_hour, reward_int))
                break

    def on_confirm_pay(self, apply_sorder):
        """
        确认支付奖励处理
        :param apply_sorder: 申请帮助子订单id
        :return:
        """
        from mmm_da.lib.server_info import ServerInfoMgr, daysdiff
        from mmm_da.lib.help_pay.control import ApplyHelpPayMgr
        from mmm_da.lib.help.control import ApplyHelpMgr
        apply_help_pay_dic = ApplyHelpPayMgr().get_data_by_sorder(apply_sorder)
        apply_help_dic = ApplyHelpMgr().get_data_by_order(apply_help_pay_dic['apply_order'])

        days2confirm = daysdiff(time.time(), apply_help_dic['apply_stime'])
        for reward_hour, reward_int in ServerInfoMgr().attr_cfmd_reward_dic.items():
            reward_hour = float(reward_hour)
            if days2confirm <= reward_hour:
                upd_dic = {"apply_sorder": apply_sorder,
                           "apply_interest": apply_help_pay_dic['apply_interest'] + reward_int}
                ApplyHelpPayMgr().update_dic(apply_sorder, upd_dic)
                logger.warn("BonusMgr::on_confirm_pay reward!!!, reward_hour:%s,reward_int:%s "
                            % (reward_hour, reward_int))
                break

    def on_apply_finish(self, apply_uid, apply_money):
        """
        申请帮助支付完成奖金奖励
        :param apply_uid:   申请帮助uid
        :param apply_money: 申请帮助金额
        :return:
        """
        from mmm_da.lib.account.control import AccountMgr
        # 获取领导id列表
        leader_id_ls = []
        chd_account = AccountMgr().get_data_by_id(apply_uid)
        led_account = AccountMgr().get_data_by_id(chd_account.attr_leader_id)
        while led_account:
            leader_id_ls.append(led_account.id)
            led_account = AccountMgr().get_data_by_id(led_account.attr_leader_id)
            if not led_account:
                break

        # 奖励额度获取
        bonus_rate_ls = [BONUS_RATE_LV[i] if i < len(BONUS_RATE_LV) else MIN_BONUS_RATE
                         for i in xrange(len(leader_id_ls))]

        # 奖励
        bonus_dic = dict(zip(leader_id_ls, bonus_rate_ls))

        for uid, bonus_rate in bonus_dic.items():
            account = AccountMgr().get_data_by_id(uid)
            bonus_money = apply_money * bonus_rate / 100
            account.attr_mafuluo += bonus_money

            # 增加奖金日志
            BonusLogMgr().add_bonus_log(uid,
                                        apply_uid,
                                        bonus_money,
                                        LAYER_APPLY_PAID_REWARD)

        logger.info("BonusMgr::on_apply_finish reward!!! apply_uid={auid}, apply_money={amoney}, bonus_dic={bdic}"
                    .format(auid=apply_uid, amoney=apply_money, bdic=bonus_dic))

    def on_apply_cancel(self, apply_uid, apply_money):
        """
        申请帮助取消支付奖金惩罚
        :param apply_uid:   申请帮助uid
        :param apply_money: 申请帮助金额
        :return:
        """
        from mmm_da.lib.server_info import ServerInfoMgr
        from mmm_da.lib.account.control import AccountMgr
        apply_account = AccountMgr().get_data_by_id(apply_uid)
        leader_account = AccountMgr().get_data_by_id(apply_account.attr_leader_id)
        assert leader_account

        punish_money = -apply_money * ServerInfoMgr().attr_apply_unpaid_punish / 100
        leader_account.attr_mafuluo += punish_money

        # 增加奖金日志
        BonusLogMgr().add_bonus_log(apply_account.attr_leader_id,
                                    apply_uid,
                                    punish_money,
                                    LAYER_APPLY_UNPAID_PUNISH)

        logger.info("BonusMgr::on_apply_cancel punish!!! leader_id={luid}, apply_uid={auid}, punish_money={pmoney}"
                    .format(luid=apply_account.attr_leader_id, auid=apply_uid, pmoney=punish_money))

    def match_coin_back(self, apply_sorder):
        """
        排单币返还
        :param apply_sorder: 申请帮助子订单id
        :return: 应该返还的配单币
        """
        from mmm_da.lib.help_pay.control import ApplyHelpPayMgr
        apply_help_pay_dic = ApplyHelpPayMgr().get_data_by_sorder(apply_sorder)

        assert ApplyHelpPayMgr().is_confirmed(apply_sorder)
        assert apply_help_pay_dic
        return calc_match_coin(apply_help_pay_dic['apply_pmoney'])


class BonusLogMgr(IManager):
    """
    奖金日志管理器
    """
    __metaclass__ = Singleton

    def __init__(self):
        self.__ddp = DirtyDictProcess()

    def update(self, curtime):
        dirty_dict = self.__ddp.get_db_dirty_dicts()
        DBBonusLogInst.insert_ls(dirty_dict.get("insert", []))

    def add_bonus_log(self, afctd_uid, afct_uid, afct_bonus, afct_type):
        """
        添加奖励日志,直接插入数据库
        :param afctd_uid: 被奖励的uid
        :param afct_uid:  奖励者
        :param afct_bonus: 奖金
        :param afct_type:  奖励类型
        :return:
        """
        bonus_log_dic = {"afctd_uid": afctd_uid,
                         "afct_uid": afct_uid,
                         "afct_bonus": afct_bonus,
                         "afct_type": afct_type,
                         "afct_time": time.time()}
        self.__ddp.ist_db_dict(ServerInfoMgr().make_unique_id(), bonus_log_dic)

    def get_bonus_logs(self, afctd_uid, page_idx=1):
        """
        获取奖金记录,使用limit从数据库直接获取
        :param afctd_uid: 被奖励的uid
        :param page_idx: 页数，默认1
        :return:
        """
        stime = time.time()
        bonus_log_sql = "SELECT afct_uid,afct_bonus,afct_time,afct_type FROM %s WHERE afctd_uid=%s ORDER BY id DESC limit %s,%s"\
                    %(DBBonusLogInst.table_name,
                      afctd_uid,
                      BONUS_PAGE_COUNT * (page_idx -1),
                      BONUS_PAGE_COUNT)

        bonus_logs = list(DBBonusLogInst.query(bonus_log_sql))

        # 降序排列
        bonus_logs.sort(key=lambda dic:dic["afct_time"], reverse=True)

        etime = time.time()
        logger.info("BonusLogMgr:get_bonus_logs, afctd_uid:%s page_idx:%s use_time:%s  bonus_log_sql:%s"
                    % (afctd_uid,
                       page_idx,
                       etime - stime,
                       bonus_log_sql))
        return bonus_logs

