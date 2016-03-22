#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2016-2-26

@author: Jay
"""
from lib.common import *
from utils.interfaces.mmm_da.http_rpc import gm_login, view_account, active_account, seal_account, \
    login,unseal_account, add_active_coin, add_match_coin
from utils import error_code
from lib.account import new_account, MMMDAHttpRpcClt,admin0d_id, admin01_passwd
from mmm_da.lib.account.setting import ACTIVED


class GMAccountHttpRPCTest(unittest.TestCase):

    # 初始化工作
    def setUp(self):
        pass

    # 退出清理工作
    def tearDown(self):
        pass

    @unittest_adaptor()
    def test_http_rpc_gm_login(self):
        # gm 可以登陆
        login_result = gm_login(MMMDAHttpRpcClt, admin0d_id, admin01_passwd)
        print "login_result,", login_result
        self.assertTrue(login_result['result'] == error_code.ERROR_SUCCESS)

        # 其他账号不可以登陆
        new_id, new_passwd = new_account()
        self.assertRaises(Exception, gm_login, MMMDAHttpRpcClt, new_id, new_passwd)

    @unittest_adaptor()
    def test_http_rpc_gm_view_account(self):
        new_id, new_passwd = new_account()
        print "new_id,",new_id

        view_result = view_account(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, new_id)
        print "view_result,",view_result
        self.assertTrue(str(view_result['id']) == str(new_id))
        self.assertTrue(view_result['passwd'] == new_passwd)

    @unittest_adaptor()
    def test_http_rpc_gm_active_account(self):
        new_id, new_passwd = new_account(can_active=False)

        view_result1 = view_account(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, new_id)
        print "view_result1,",view_result1, type(view_result1)
        self.assertTrue(view_result1['stat'] != ACTIVED)

        active_result = active_account(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, new_id)
        print
        self.assertTrue(active_result == error_code.ERROR_SUCCESS)

        view_result2 = view_account(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, new_id)
        self.assertTrue(view_result2['stat'] == ACTIVED)

    @unittest_adaptor()
    def test_http_rpc_seal_account(self):
        new_id, new_passwd = new_account()

        # 登陆成功
        login_result = login(MMMDAHttpRpcClt, new_id, new_passwd)
        print "login_result,", login_result
        self.assertTrue(login_result['result'] == error_code.ERROR_SUCCESS)

        # 封号
        seal_account_result = seal_account(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, new_id)
        print "seal_account_result :%s, new_id:%s," % (seal_account_result, new_id)

        # 登陆失败
        # login error on sealed account, 暂时测试是不开启封号的
        self.assertRaises(Exception, login, MMMDAHttpRpcClt, new_id, new_passwd)

    @unittest_adaptor()
    def test_http_rpc_unseal_account(self):
        new_id, new_passwd = new_account()

        # 登陆成功
        login_result = login(MMMDAHttpRpcClt, new_id, new_passwd)
        print "login_result,", login_result
        self.assertTrue(login_result['result'] == error_code.ERROR_SUCCESS)

        # 封号
        seal_account_result = seal_account(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, new_id)
        print "seal_account_result :%s, new_id:%s," % (seal_account_result, new_id)

        # 登陆失败
        # login error on sealed account, 暂时测试是不开启封号的
        self.assertRaises(Exception, login, MMMDAHttpRpcClt, new_id, new_passwd)

        # 解除封号
        seal_account_result = unseal_account(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, new_id)
        print "seal_account_result :%s, new_id:%s," % (seal_account_result, new_id)

        # 登陆成功
        login_result = login(MMMDAHttpRpcClt, new_id, new_passwd)
        print "login_result,", login_result
        self.assertTrue(login_result['result'] == error_code.ERROR_SUCCESS)

    @unittest_adaptor()
    def test_http_rpc_add_active_coin(self):
        adding_account, new_passwd = new_account()

        add_coin_result = add_active_coin(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, adding_account, 11)

        cur_active_coin = add_coin_result['active_coin']
        adding_active_coin = random.randint(1, 1000)
        add_coin_result = add_active_coin(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, adding_account, adding_active_coin)
        self.assertTrue(add_coin_result['active_coin'] == cur_active_coin + adding_active_coin)

    @unittest_adaptor()
    def test_http_rpc_add_match_coin(self):
        adding_account, new_passwd = new_account()

        add_coin_result = add_match_coin(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, adding_account, 11)
        print "add_coin_result,",add_coin_result

        cur_match_coin = add_coin_result['match_coin']
        print "cur_match_coin,",cur_match_coin
        adding_match_coin = random.randint(1, 1000)
        print "adding_match_coin,",adding_match_coin
        add_coin_result = add_match_coin(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, adding_account, adding_match_coin)
        print "add_coin_result,",add_coin_result
        self.assertTrue(add_coin_result['match_coin'] == cur_match_coin + adding_match_coin)