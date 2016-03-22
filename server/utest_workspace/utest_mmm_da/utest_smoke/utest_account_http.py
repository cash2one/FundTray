#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-4-30

@author: Jay
"""
from lib.common import *
from utils.interfaces.mmm_da.http_rpc import register, login, account, passwd_change, \
    random_leader_id, check_id, check_phone
from utils import error_code
from lib.account import new_account, new_access_token, MMMDAHttpRpcClt,admin0d_id, admin01_passwd, new_account_id


class AccountHttpRPCTest(unittest.TestCase):

    # 初始化工作
    def setUp(self):
        pass

    # 退出清理工作
    def tearDown(self):
        pass

    @unittest_adaptor()
    def test_http_rpc_register_login_nomal(self):
        new_id = new_account_id()

        register_data = {"id": new_id,
                         "passwd":"123456",
                         "id_card":"test_id_card",
                         "email":"test_email",
                         "phone":"test_phone",
                         "leader_id":"18888",
                         "bank":"test_bank",
                         "bank_address":"test_bank_add",
                         "bank_account":"test_bank_act",
                         "bank_name":"test_bank_name",
                         "wechat":"test_wechat",
                         "alipay":"test_alipay"}

        register_result = register(MMMDAHttpRpcClt, register_data)
        print "register_result,",register_result
        self.assertTrue(register_result['result'] == error_code.ERROR_SUCCESS)

        login_result = login(MMMDAHttpRpcClt, new_id, register_data['passwd'])
        print "login_result,", login_result
        self.assertTrue(login_result['result'] == error_code.ERROR_SUCCESS)

        access_token = login_result['access_token']

        account_result = account(MMMDAHttpRpcClt, new_id, access_token, new_id, {"passwd":"account_change_passwd"})
        print "account_result,", account_result
        self.assertTrue(account_result['result'] == error_code.ERROR_SUCCESS)

    @unittest_adaptor()
    def test_http_rpc_register_login_error(self):
        new_id = new_account_id()

        register_data = {"id": new_id,
                         "passwd":"123456",
                         "id_card":"test_id_card",
                         "email":"test_email",
                         "phone":"test_phone",
                         "leader_id":"18888",
                         "bank":"test_bank",
                         "bank_address":"test_bank_add",
                         "bank_account":"test_bank_act",
                         "bank_name":"test_bank_name",
                         "wechat":"test_wechat",
                         "alipay":"test_alipay"}

        register_result = register(MMMDAHttpRpcClt, register_data)
        print "register_result,",register_result
        self.assertTrue(register_result['result'] == error_code.ERROR_SUCCESS)

        # login error on old passwd
        self.assertRaises(Exception, register, MMMDAHttpRpcClt, register_data)

    @unittest_adaptor()
    def test_http_rpc_change_passwd_nomal(self):
        new_id, new_passwd = new_account()
        new_token = new_access_token(new_id, new_passwd)

        # change passwd
        change_paswd = random_str()
        passwd_change(MMMDAHttpRpcClt, new_id, new_token, new_passwd, change_paswd)

        # login error on old passwd
        self.assertRaises(Exception, login, MMMDAHttpRpcClt, new_id, new_passwd)

        # login success on new passwd
        login_result = login(MMMDAHttpRpcClt, new_id, change_paswd)
        print "login_result,", login_result
        self.assertTrue(login_result['result'] == error_code.ERROR_SUCCESS)

    @unittest_adaptor()
    def test_http_rpc_get_account_infos_nomal(self):
        new_id, new_passwd = new_account()
        new_token = new_access_token(new_id, new_passwd)

        view_id = 18888
        view_account_result = account(MMMDAHttpRpcClt, new_id, new_token, view_id)
        print "view_account_result,", view_account_result
        self.assertTrue(view_account_result['result'] == error_code.ERROR_SUCCESS)
        self.assertTrue("passwd" not in view_account_result['account_info'])

    @unittest_adaptor()
    def test_http_rpc_get_random_leader_id_nomal(self):
        random_leader_id_result = random_leader_id(MMMDAHttpRpcClt)
        print "random_leader_id_result,", random_leader_id_result
        self.assertTrue(random_leader_id_result['result'] == error_code.ERROR_SUCCESS)
        self.assertTrue(random_leader_id_result['leader_id'])

    @unittest_adaptor()
    def test_http_rpc_get_random_team_count_nomal(self):
        login_result = login(MMMDAHttpRpcClt, admin0d_id, admin01_passwd)
        print "login_result,",login_result
        print "team_count,",login_result['account_info']['team_count']
        self.assertTrue(login_result['account_info']['team_count'])

    @unittest_adaptor()
    def test_http_rpc_check_id(self):
        new_id = new_account_id()

        # checkid
        self.assertRaises(Exception, check_id, MMMDAHttpRpcClt, new_id)

        # register
        register_data = {"id": new_id,
                         "passwd":"123456",
                         "id_card":"test_id_card",
                         "email":"test_email",
                         "phone":"test_phone",
                         "leader_id":"18888",
                         "bank":"test_bank",
                         "bank_address":"test_bank_add",
                         "bank_account":"test_bank_act",
                         "bank_name":"test_bank_name",
                         "wechat":"test_wechat",
                         "alipay":"test_alipay"}

        register_result = register(MMMDAHttpRpcClt, register_data)
        print "register_result,",register_result
        self.assertTrue(register_result['result'] == error_code.ERROR_SUCCESS)

        # recheck id
        check_id(MMMDAHttpRpcClt, new_id)

    @unittest_adaptor()
    def test_http_rpc_check_phone(self):
        test_phone = "1" + str(int(time.time()))

        # check phone
        check_phone(MMMDAHttpRpcClt, test_phone)

        # register
        register_data = {"id": new_account_id(),
                         "passwd":"123456",
                         "id_card":"test_id_card",
                         "email":"test_email",
                         "phone":test_phone,
                         "leader_id":"18888",
                         "bank":"test_bank",
                         "bank_address":"test_bank_add",
                         "bank_account":"test_bank_act",
                         "bank_name":"test_bank_name",
                         "wechat":"test_wechat",
                         "alipay":"test_alipay"}

        register_result = register(MMMDAHttpRpcClt, register_data)
        print "register_result,",register_result
        self.assertTrue(register_result['result'] == error_code.ERROR_SUCCESS)

        # recheck phone
        self.assertRaises(Exception, check_phone, MMMDAHttpRpcClt, test_phone)

