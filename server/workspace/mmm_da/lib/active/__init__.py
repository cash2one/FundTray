#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-12-16

@author: Jay
"""

from utils.interfaces.common import IManager
from utils.meta.singleton import Singleton
from utils import logger
from mmm_da.lib.account.model import ACTIVED, UNACTIVED


class ActiveMgr(IManager):
    __metaclass__ = Singleton

    def active_account(self, oper_account, active_id):
        """
        账号激活
        :param oper_account: 操作账号
        :param active_id: 激活id
        :return:
        """
        from mmm_da.lib.account.control import AccountMgr
        activing_account = AccountMgr().get_data_by_id(active_id)
        if not oper_account or not activing_account:
            logger.info("ActiveMgr::active_account Error, not account!!!, oper_id:%s, active_id:%s" % (oper_account.id, active_id))
            return False

        # 如果目标账户已经激活，不再激活
        if activing_account.attr_stat == ACTIVED:
            logger.info("ActiveMgr::active_account Error, has actived active_id:%s" % active_id)
            return False

        from mmm_da.lib.server_info import ServerInfoMgr
        if oper_account.attr_active_coin < ServerInfoMgr().attr_active_coin_loss:
            logger.info("ActiveMgr::active_account Error, oper account not enough active_coin!!!, oper_id:%s" % oper_account.id)
            return False

        # 扣除激活消耗
        oper_account.attr_active_coin -= ServerInfoMgr().attr_active_coin_loss

        # 激活
        activing_account.attr_stat = ACTIVED
        logger.info("ActiveMgr::active_account Success!!!, oper_id:%s, active_id:%s" % (oper_account.id, active_id))
        return True



