#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-12-22

@author: Jay
"""

from lib.common import *
from mmm_da.lib.filter.control import ApplyPayFilter
import time
from mmm_da.lib.help_pay.setting import APYS_PAY_WAIT


apply_pay_max_days = 1
days_diff_fun = lambda d1, d2: int((d1 - d2) / 1)
id_2_dic = {}

ot_ls = []
def cb_fun(uid):
    ot_ls.append(uid)


def clear_tmp():
    global ot_ls
    global id_2_dic
    ot_ls= []
    id_2_dic.clear()

def get_apply_pay_ls():
    return id_2_dic.values()

apc = ApplyPayFilter()
filter_params = {}
filter_params.setdefault("apply_pay_max_days", apply_pay_max_days)
filter_params.setdefault("days_diff_fun", days_diff_fun)
apc.init(get_apply_pay_ls, cb_fun, filter_params)

class ApplyPayCheckerTest(unittest.TestCase):

    # 初始化工作
    def setUp(self):
        pass

    # 退出清理工作
    def tearDown(self):
        pass

    @unittest_adaptor()
    def test_apply_pay_nomal(self):
        clear_tmp()
        apc.filter()
        self.assertTrue(not ot_ls)

    @unittest_adaptor()
    def test_apply_pay_ot(self):
        clear_tmp()
        uid2 = "2"
        id_2_dic[uid2] = {'apply_sorder':uid2,
                          'apply_mtime': (time.time() - apply_pay_max_days - 1),
                          'apply_pstat': APYS_PAY_WAIT}

        apc.filter()
        self.assertTrue(ot_ls == [uid2])

    @unittest_adaptor()
    def test_apply_pay_ot_much(self):
        clear_tmp()
        uid2 = "2"
        id_2_dic[uid2] = {'apply_sorder':uid2,
                          'apply_mtime': (time.time() - apply_pay_max_days - 1),
                          'apply_pstat': APYS_PAY_WAIT}

        uid3 = "3"
        id_2_dic[uid3] = {'apply_sorder':uid3,
                          'apply_mtime': (time.time() - apply_pay_max_days - 2),
                          'apply_pstat': APYS_PAY_WAIT}

        uid4 = "4"
        id_2_dic[uid4] = {'apply_sorder':uid4,
                          'apply_mtime': (time.time() - apply_pay_max_days),
                          'apply_pstat': APYS_PAY_WAIT}

        uid5 = "5"
        id_2_dic[uid5] = {'apply_sorder':uid5,
                          'apply_mtime': (time.time()),
                          'apply_pstat': APYS_PAY_WAIT}

        apc.filter()
        #self.assertTrue(set(ot_ls) == set([uid2, uid3]))
        self.assertTrue(set(ot_ls) == {uid2, uid3, uid4})

