#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-12-16

@author: Jay
"""
from lib.common import *
from utils.interfaces.mmm_da.http_rpc import system_info, set_notice, add_accept_help, cur_accept_help
from lib.account import MMMDAHttpRpcClt, admin0d_id, admin01_access_token, admin01_passwd, new_account, new_access_token
import urllib2


class SystemHttpRPCTest(unittest.TestCase):

    # 初始化工作
    def setUp(self):
        pass

    # 退出清理工作
    def tearDown(self):
        pass

    @unittest_adaptor()
    def test_http_rpc_system_info_nomal(self):
        system_info_result = system_info(MMMDAHttpRpcClt, admin0d_id, admin01_access_token)
        print "system_info_result,", system_info_result
        self.assertTrue(system_info_result)

        notice = "固定收益都是30%利息！  当有人需要资金帮助时，你就可以把你的资金打给对方！ 当你需要资金帮助时，你就可以在平台内提出申请，等待别人帮助。就这样，不断的提供帮助和接受帮助，每个月30%的收益你就可以赚到。资金不经过互助系统平台，而是会员之间相互转账，没有任何风险。"
        notice = urllib2.quote(notice)

        set_notice_result = set_notice(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, notice)
        print "set_notice_result,", set_notice_result
        self.assertTrue(system_info_result)

        system_info_result2 = system_info(MMMDAHttpRpcClt, admin0d_id, admin01_access_token)
        print "system_info_result2,", system_info_result2
        self.assertTrue(system_info_result2)
        print system_info_result2['notice']

    @unittest_adaptor()
    def test_http_rpc_system_add_apply_help_normal(self):
        """
        测试添加流程
         :return:
        """
        new_id, new_passwd = new_account()
        print "new_id,",new_id
        print "new_passwd,",new_passwd
        new_token = new_access_token(new_id, new_passwd)
        add_accept_help_result = add_accept_help(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, new_id, 10000)
        print "add_accept_help_result,", add_accept_help_result

        # 申请帮助方:当前接受帮助
        cur_accept_help_result = cur_accept_help(MMMDAHttpRpcClt, new_id, new_token)
        print "cur_accept_help_result,", cur_accept_help_result
        self.assertTrue(cur_accept_help_result['accept_help'])
