#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2016-2-20

@author: Jay
"""
from lib.account import *
from utils.interfaces.mmm_da.http_rpc import add_accept_help, auto_match, apply_help, add_apply_help
from lib.help import random_apply_money, paid_confirm
from lib.setting import SYNC_WAIT_TIME

class HelpAcceptFinishHttpRPCTest(unittest.TestCase):

    # 初始化工作
    def setUp(self):
        pass

    # 退出清理工作
    def tearDown(self):
        pass

    @unittest_adaptor()
    def test_http_rpc_accept_finish_apply_normal(self):
        """
        接受帮助以后及时申请帮助没有被封号
         注意：如果要测试以下流程，mmm_da需要开启以下模式--apply_req second_1 --match second_11 --apply_pay second_21 --accept_req second_31 --day_seconds 1 --force_mtype system --enable_active False --enable_seal False  --enable_pay_check False
        :return:
        """
        # 申请帮助方
        apply_id, apply_passwd = new_account()
        apply_token = new_access_token(apply_id, apply_passwd)
        apply_money = 1000
        add_apply_help_result = add_apply_help(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, apply_id, apply_money)
        print "add_apply_help_result,", add_apply_help_result

        # 接受帮助方
        accept_id, accept_passwd = new_account()
        accept_token = new_access_token(accept_id, accept_passwd)
        add_accept_help_result = add_accept_help(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, accept_id, apply_money)
        print "add_accept_help_result,", add_accept_help_result

        # 接受帮助全部匹配完成
        auto_match_result = auto_match(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, apply_id, accept_id, apply_money)
        self.assertTrue(auto_match_result == error_code.ERROR_SUCCESS)
        paid_confirm(self, apply_id, apply_token)

        # 申请帮助方:申请帮助
        apply_money = random_apply_money(accept_id)
        apply_help_result = apply_help(MMMDAHttpRpcClt, accept_id, accept_token, apply_money)
        self.assertTrue(apply_help_result['result'] == error_code.ERROR_SUCCESS)
        print "apply_help_result,",apply_help_result

        time.sleep(SYNC_WAIT_TIME)

        # 可以正常登陆
        login_result = login(MMMDAHttpRpcClt, accept_id, accept_passwd)
        self.assertTrue(login_result['result'] == error_code.ERROR_SUCCESS)

    @unittest_adaptor()
    def test_http_rpc_accept_finish_not_apply_sealed_normal(self):
        """
        接受帮助以后没有申请帮助被封号
         注意：如果要测试以下流程，mmm_da需要开启以下模式--apply_req second_1 --match second_11 --apply_pay second_21 --accept_req second_31 --day_seconds 1 --force_mtype system --enable_active False --enable_seal False  --enable_pay_check False
        :return:
        """
        # 申请帮助方
        apply_id, apply_passwd = new_account()
        apply_token = new_access_token(apply_id, apply_passwd)
        apply_money = 1000
        add_apply_help_result = add_apply_help(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, apply_id, apply_money)
        print "add_apply_help_result,", add_apply_help_result

        # 接受帮助方
        accept_id, accept_passwd = new_account()
        accept_token = new_access_token(accept_id, accept_passwd)
        add_accept_help_result = add_accept_help(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, accept_id, apply_money)
        print "add_accept_help_result,", add_accept_help_result

        # 接受帮助全部匹配完成
        auto_match_result = auto_match(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, apply_id, accept_id, apply_money)
        self.assertTrue(auto_match_result == error_code.ERROR_SUCCESS)
        paid_confirm(self, apply_id, apply_token)

        time.sleep(SYNC_WAIT_TIME)

        # login error on sealed account, 暂时测试是不开启封号的
        self.assertRaises(Exception, login, MMMDAHttpRpcClt, accept_id, accept_passwd)
