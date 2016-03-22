#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2016-1-29

@author: Jay
"""
from lib.common import *
from utils.interfaces.mmm_da.http_rpc import active_coin_transfer, match_coin_transfer, account
from utils import error_code
from lib.account import MMMDAHttpRpcClt, admin0d_id, admin01_access_token, new_account, new_access_token


class CoinTransferHttpRPCTest(unittest.TestCase):

    # 初始化工作
    def setUp(self):
        pass

    # 退出清理工作
    def tearDown(self):
        pass

    @unittest_adaptor()
    def test_http_rpc_active_coin_transfer_nomal(self):
        user1, passwd1 = new_account()
        token1 = new_access_token(user1, passwd1)

        # admin before transfer
        view_account_result1 = account(MMMDAHttpRpcClt, admin0d_id, admin01_access_token, admin0d_id)
        self.assertTrue(view_account_result1['result'] == error_code.ERROR_SUCCESS)
        adm_bf_active_coin = view_account_result1['account_info']['active_coin']
        print "adm_bf_active_coin,",adm_bf_active_coin

        # user before transfer
        view_account_result2 = account(MMMDAHttpRpcClt, user1, token1, user1)
        self.assertTrue(view_account_result2['result'] == error_code.ERROR_SUCCESS)
        user1_bf_active_coin = view_account_result2['account_info']['active_coin']
        print "user1_bf_active_coin,",user1_bf_active_coin

        # transfer
        transfer_coin = random.randint(1, adm_bf_active_coin)
        print "transfer_coin,",transfer_coin
        active_coin_transfer(MMMDAHttpRpcClt,admin0d_id, admin01_access_token, user1, transfer_coin)

        # admin after transfer
        view_account_result3 = account(MMMDAHttpRpcClt, admin0d_id, admin01_access_token, admin0d_id)
        self.assertTrue(view_account_result3['result'] == error_code.ERROR_SUCCESS)
        adm_aft_active_coin = view_account_result3['account_info']['active_coin']
        print "adm_aft_active_coin,",adm_aft_active_coin

        # user after transfer
        view_account_result4 = account(MMMDAHttpRpcClt, user1, token1, user1)
        self.assertTrue(view_account_result4['result'] == error_code.ERROR_SUCCESS)
        user1_aft_active_coin = view_account_result4['account_info']['active_coin']
        print "user1_aft_active_coin,",user1_aft_active_coin

        # transfter assert
        self.assertTrue(adm_bf_active_coin == adm_aft_active_coin + transfer_coin)
        self.assertTrue(user1_bf_active_coin + transfer_coin == user1_aft_active_coin)

    @unittest_adaptor()
    def test_http_rpc_match_coin_transfer_nomal(self):
        user1, passwd1 = new_account()
        token1 = new_access_token(user1, passwd1)

        # admin before transfer
        view_account_result1 = account(MMMDAHttpRpcClt, admin0d_id, admin01_access_token, admin0d_id)
        self.assertTrue(view_account_result1['result'] == error_code.ERROR_SUCCESS)
        adm_bf_match_coin = view_account_result1['account_info']['match_coin']
        print "adm_bf_match_coin,",adm_bf_match_coin

        # user before transfer
        view_account_result2 = account(MMMDAHttpRpcClt, user1, token1, user1)
        self.assertTrue(view_account_result2['result'] == error_code.ERROR_SUCCESS)
        user1_bf_match_coin = view_account_result2['account_info']['match_coin']
        print "user1_bf_match_coin,",user1_bf_match_coin

        # transfer
        transfer_coin = random.randint(1, adm_bf_match_coin)
        print "transfer_coin,",transfer_coin
        match_coin_transfer(MMMDAHttpRpcClt, admin0d_id, admin01_access_token, user1, transfer_coin)

        # admin after transfer
        view_account_result3 = account(MMMDAHttpRpcClt, admin0d_id, admin01_access_token, admin0d_id)
        self.assertTrue(view_account_result3['result'] == error_code.ERROR_SUCCESS)
        adm_aft_match_coin = view_account_result3['account_info']['match_coin']
        print "adm_aft_match_coin,",adm_aft_match_coin

        # user after transfer
        view_account_result4 = account(MMMDAHttpRpcClt, user1, token1, user1)
        self.assertTrue(view_account_result4['result'] == error_code.ERROR_SUCCESS)
        user1_aft_match_coin = view_account_result4['account_info']['match_coin']
        print "user1_aft_match_coin,",user1_aft_match_coin

        # transfter assert
        self.assertTrue(adm_bf_match_coin == adm_aft_match_coin + transfer_coin)
        self.assertTrue(user1_bf_match_coin + transfer_coin == user1_aft_match_coin)
