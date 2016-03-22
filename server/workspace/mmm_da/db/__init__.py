#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-9-30

@author: Jay
"""

from utils.data.db.mysql_manual import SchemaTable
from utils.service_control.cacher import ParamCacher
from utils.meta.instance_pool import InstancePool
from utils.service_control.parser import ArgumentParser


class DBMMMTable(SchemaTable):
    __metaclass__ = InstancePool

    def __init__(self, table_name):
        super(DBMMMTable, self).__init__(ParamCacher().db_instance, ArgumentParser().args.db_name, table_name)

DBAccountInst = DBMMMTable.instance("account")
DBApplyHelpInst = DBMMMTable.instance("apply_help")
DBApplyHelpReqInst = DBMMMTable.instance("apply_help_req")
DBAcceptHelpInst = DBMMMTable.instance("accept_help")
DBAcceptHelpReqInst = DBMMMTable.instance("accept_help_req")
DBServerInfoInst = DBMMMTable.instance("server_info")
DBBonusLogInst = DBMMMTable.instance("bonus_log")
DBHistoryNoticeInst = DBMMMTable.instance("history_noticce")
DBApplyHelpWaitInst = DBMMMTable.instance("apply_help_wait")
DBApplyHelpPayInst = DBMMMTable.instance("apply_help_pay")
