#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2016-1-13

@author: Jay
"""
from lib.account import *
from utils.interfaces.mmm_da.http_rpc import auto_match, add_accept_help, cur_apply_help, add_apply_help,\
    cur_accept_help,apply_help_list, add_accept_help, accept_help_list
from lib.help import random_apply_money


class GMHelpMatchHttpRPCTest(unittest.TestCase):

    # 初始化工作
    def setUp(self):
        pass

    # 退出清理工作
    def tearDown(self):
        pass

    @unittest_adaptor()
    def test_http_rpc_add_accept_help_normal(self):
        """
        添加接受帮助
         注意：如果要测试以下流程，mmm_da需要开启以下模式--apply_req second_1 --match second_11 --apply_pay second_21 --accept_req second_31 --day_seconds 1 --force_mtype system --enable_active False --enable_seal False  --enable_pay_check False
        :return:
        """
        new_id, new_passwd = new_account()
        new_token = new_access_token(new_id, new_passwd)

        apply_money = random_apply_money(new_id)
        add_accept_help_result = add_accept_help(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, new_id, apply_money)
        print "add_accept_help_result,", add_accept_help_result

        cur_accept_help_result = cur_accept_help(MMMDAHttpRpcClt, new_id, new_token)
        print cur_accept_help_result
        self.assertTrue(cur_accept_help_result['accept_help'])

    @unittest_adaptor()
    def test_http_rpc_add_apply_help_normal(self):
        """
        添加申请帮助
         注意：如果要测试以下流程，mmm_da需要开启以下模式--apply_req second_1 --match second_11 --apply_pay second_21 --accept_req second_31 --day_seconds 1 --force_mtype system --enable_active False --enable_seal False  --enable_pay_check False
        :return:
        """
        new_apply_id, new_apply_passwd = new_account()
        new_token = new_access_token(new_apply_id, new_apply_passwd)
        apply_money = random_apply_money(new_apply_id)
        add_apply_help_result = add_apply_help(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, new_apply_id, apply_money)
        print "add_apply_help_result,", add_apply_help_result

        cur_accept_help_result = cur_apply_help(MMMDAHttpRpcClt, new_apply_id, new_token)
        self.assertTrue(cur_accept_help_result['apply_help'])

    @unittest_adaptor()
    def test_http_rpc_auto_match_normal(self):
        """
        自动匹配
         注意：如果要测试以下流程，mmm_da需要开启以下模式--apply_req second_1 --match second_11 --apply_pay second_21 --accept_req second_31 --day_seconds 1 --force_mtype system --enable_active False --enable_seal False  --enable_pay_check False
        :return:
        """
        new_id, new_passwd = new_account()
        apply_money = random_apply_money(new_id)
        add_accept_help_result = add_accept_help(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, new_id, apply_money)
        print "add_accept_help_result,", add_accept_help_result

        # 新申请帮助方:信息
        new_apply_id2, new_apply_passwd2 = new_account()
        new_apply_token2 = new_access_token(new_apply_id2, new_apply_passwd2)
        add_apply_help_result = add_apply_help(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, new_apply_id2, apply_money)
        print "add_apply_help_result,", add_apply_help_result

        # 新申请帮助方:自动匹配
        auto_match_result = auto_match(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, new_apply_id2, new_id, apply_money)
        self.assertTrue(auto_match_result == error_code.ERROR_SUCCESS)

        # 新申请帮助方:当前申请帮助列表
        cur_apply_help_result = cur_apply_help(MMMDAHttpRpcClt, new_apply_id2, new_apply_token2)
        print "cur_apply_help_result,", cur_apply_help_result
        self.assertTrue(cur_apply_help_result['apply_help'])

    @unittest_adaptor()
    def test_http_rpc_apply_help_list_normal(self):
        """
        gm申请帮助列表显示
         注意：如果要测试以下流程，mmm_da需要开启以下模式--apply_req second_1 --match second_11 --apply_pay second_21 --accept_req second_31 --day_seconds 1 --force_mtype system --enable_active False --enable_seal False  --enable_pay_check False
        :return:
        """
        apply_id, apply_passwd = new_account()
        apply_token = new_access_token(apply_id, apply_passwd)
        print "apply_id,",apply_id

        apply_money = random_apply_money(apply_id)
        # 申请帮助方:申请帮助
        add_apply_help_result = add_apply_help(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, apply_id, apply_money)
        print "add_apply_help_result,", add_apply_help_result

        # admin 可以访问
        apply_help_list_result = apply_help_list(MMMDAHttpRpcClt, admin0d_id, admin01_access_token)
        print "apply_help_list_result,",apply_help_list_result
        self.assertTrue(apply_help_list_result['result'] == error_code.ERROR_SUCCESS)
        self.assertTrue(apply_help_list_result['apply_help_list'])
        apply_help_id_ls = map(lambda dic:dic['apply_uid'], apply_help_list_result['apply_help_list'])
        print "apply_help_id_ls,",apply_help_id_ls
        self.assertTrue(str(apply_id) in apply_help_id_ls)

        # 普通用户不可以访问
        self.assertRaises(Exception, apply_help_list, MMMDAHttpRpcClt, apply_id, apply_token)

    @unittest_adaptor()
    def test_http_rpc_accept_help_list_normal(self):
        """
        gm接受帮助列表显示
         注意：如果要测试以下流程，mmm_da需要开启以下模式--apply_req second_1 --match second_11 --apply_pay second_21 --accept_req second_31 --day_seconds 1 --force_mtype system --enable_active False --enable_seal False  --enable_pay_check False
        :return:
        """
        accept_id, accept_passwd = new_account()
        accept_token = new_access_token(accept_id, accept_passwd)

        accept_money = 10000
        add_accept_help_result = add_accept_help(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, accept_id, accept_money)
        print "add_accept_help_result,", add_accept_help_result

        # admin 可以访问
        accept_help_list_result = accept_help_list(MMMDAHttpRpcClt, admin0d_id, admin01_access_token)
        print "accept_help_list_result,",accept_help_list_result
        self.assertTrue(accept_help_list_result['result'] == error_code.ERROR_SUCCESS)
        self.assertTrue(accept_help_list_result['accept_help_list'])
        accept_help_id_ls = map(lambda dic:dic['accept_uid'], accept_help_list_result['accept_help_list'])
        print "accept_help_id_ls,",accept_help_id_ls
        self.assertTrue(str(accept_id) in accept_help_id_ls)

        # 普通用户不可以访问
        self.assertRaises(Exception, apply_help_list, MMMDAHttpRpcClt, accept_id, accept_token)
