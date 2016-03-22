#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-12-16

@author: Jay
"""
from lib.common import *
from utils.interfaces.mmm_da.http_rpc import server_setting, all_server_setting, reset_server_setting, login_info, login
from utils import error_code
from lib.account import MMMDAHttpRpcClt, admin0d_id, admin01_passwd, admin01_access_token, new_account
from mmm_da.lib.server_info import CAN_UPDAET_KEY_SET, JSON_KEY_SET
from utils.comm_func import sub_dict
import copy


class GMServerSettingHttpRPCTest(unittest.TestCase):

    # 初始化工作
    def setUp(self):
        pass

    # 退出清理工作
    def tearDown(self):
        pass

    @unittest_adaptor()
    def test_http_rpc_server_setting_not_json_not_notice_nomal(self):
        apply_match_min_days = 7
        server_setting_result = server_setting(MMMDAHttpRpcClt, admin0d_id, admin01_passwd,
                                               "apply_match_min_days", apply_match_min_days)

        print "server_setting_result,", server_setting_result
        self.assertTrue(server_setting_result['result'] == error_code.ERROR_SUCCESS)

        self.assertTrue(server_setting_result['server_info']['apply_match_min_days'] == apply_match_min_days)

        true_server_setting = server_setting_result['server_info']

        for k in CAN_UPDAET_KEY_SET - JSON_KEY_SET - set("notice"):
            field = k
            value = random.randint(40, 60)
            print "filed,",field
            print "value,",value

            # change
            result = server_setting(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, field, value)
            print "result,",result
            self.assertTrue(result['result'] == error_code.ERROR_SUCCESS)
            self.assertTrue(result['server_info'][field] == value)

            # recove
            result = server_setting(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, field, true_server_setting[field])
            self.assertTrue(result['result'] == error_code.ERROR_SUCCESS)
            self.assertTrue(result['server_info'][field] == true_server_setting[field])

    @unittest_adaptor()
    def test_http_rpc_all_server_setting_nomal(self):
        server_settings = all_server_setting(MMMDAHttpRpcClt, admin0d_id, admin01_access_token)
        self.assertTrue(CAN_UPDAET_KEY_SET == CAN_UPDAET_KEY_SET & set(server_settings.keys()))

    @unittest_adaptor()
    def test_http_rpc_reset_server_setting_not_json_nomal(self):
        update_key_set = CAN_UPDAET_KEY_SET - JSON_KEY_SET
        before_server_settings = all_server_setting(MMMDAHttpRpcClt, admin0d_id, admin01_access_token)
        self.assertTrue(update_key_set == update_key_set & set(before_server_settings.keys()))

        upd_keys = random.sample(list(update_key_set), random.randint(1, len(update_key_set)))
        print "upd_keys,",upd_keys
        upd_settins_dic = dict((upd_key, random.randint(1, 10)) for upd_key in upd_keys)
        print "upd_settins_dic,",upd_settins_dic

        reset_res0 = reset_server_setting(MMMDAHttpRpcClt, admin0d_id, admin01_access_token, upd_settins_dic)
        print "reset_res0,",reset_res0
        self.assertTrue(upd_settins_dic == sub_dict(reset_res0, upd_keys))

        reset_res1 = reset_server_setting(MMMDAHttpRpcClt, admin0d_id, admin01_access_token, before_server_settings)
        print "reset_res1,",reset_res1
        self.assertTrue(reset_res1 == before_server_settings)

    @unittest_adaptor()
    def test_http_rpc_reset_server_setting_json_nomal(self):
        update_key_set = JSON_KEY_SET
        before_server_settings = all_server_setting(MMMDAHttpRpcClt, admin0d_id, admin01_access_token)
        self.assertTrue(update_key_set == update_key_set & set(before_server_settings.keys()))
        print "before_server_settings,",before_server_settings

        upd_keys = random.sample(list(update_key_set), random.randint(1, len(update_key_set)))
        print "upd_keys,",upd_keys

        def random_dic():
            return dict((i, round(random.random(), 2)) for i in random.sample(xrange(1, 100), 2))
        upd_settings_dic = dict((upd_key, random_dic()) for upd_key in upd_keys)
        print "upd_settings_dic,",upd_settings_dic

        upd_settings_json_dic = dict((k, ujson.dumps(v)) for k, v in upd_settings_dic.items())
        reset_res0 = reset_server_setting(MMMDAHttpRpcClt, admin0d_id, admin01_access_token, upd_settings_json_dic)
        print "reset_res0,",reset_res0
        print "sub_dict(reset_res0, upd_keys),",sub_dict(reset_res0, upd_keys)
        self.assertTrue(ujson.loads(ujson.dumps(upd_settings_dic)) == sub_dict(reset_res0, upd_keys))

        before_server_settings_json = copy.deepcopy(before_server_settings)
        [before_server_settings_json.update({jkey:ujson.dumps(before_server_settings_json[jkey])})
         for jkey in JSON_KEY_SET]
        reset_res1 = reset_server_setting(MMMDAHttpRpcClt, admin0d_id, admin01_access_token, before_server_settings_json)
        print "reset_res1,",reset_res1
        self.assertTrue(before_server_settings == reset_res1)

    @unittest_adaptor()
    def test_http_rpc_reset_login_info_nomal(self):
        new_id, new_passwd = new_account()
        login_result = login(MMMDAHttpRpcClt, new_id, new_passwd)
        print "login_result,", login_result
        self.assertTrue(login_result['result'] == error_code.ERROR_SUCCESS)

        last_minutes = random.randint(1, 36000)
        login_count = login_info(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, last_minutes)
        self.assertTrue(login_count > 0)



