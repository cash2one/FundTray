#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-12-22

@author: Jay
"""

from lib.common import *
from mmm_da.lib.filter.control import ApplyReqFilter
import time


apply_match_min_days = 2
days_diff_fun = lambda d1, d2: int((d1 - d2) / 1)
id_2_dic = {}

ot_ls = []
def cb_fun(id):
    ot_ls.append(id)


def clear_tmp():
    global ot_ls
    global id_2_dic
    ot_ls= []
    id_2_dic.clear()


def get_apply_req_ls():
    return id_2_dic.values()

apyrq = ApplyReqFilter()
filter_params = {}
filter_params.setdefault("apply_match_min_days", apply_match_min_days)
filter_params.setdefault("days_diff_fun", days_diff_fun)
apyrq.init(get_apply_req_ls, cb_fun, filter_params)

class AcceptReqTest(unittest.TestCase):

    # 初始化工作
    def setUp(self):
        pass

    # 退出清理工作
    def tearDown(self):
        pass

    @unittest_adaptor()
    def test_apply_req_nomal(self):
        clear_tmp()
        apyrq.filter()
        self.assertTrue(not ot_ls)

    @unittest_adaptor()
    def test_apply_req_ot(self):
        clear_tmp()
        id2 = "2"
        id_2_dic[id2] = {'id': id2, 'apply_req_time': (time.time() - apply_match_min_days)}

        apyrq.filter()
        self.assertTrue(ot_ls == [id2])

    @unittest_adaptor()
    def test_apply_req_ot_much(self):
        clear_tmp()
        id1 = "1"
        id_2_dic[id1] = {'id': id1, 'apply_req_time': (time.time() - apply_match_min_days + 1)}

        id2 = "2"
        id_2_dic[id2] = {'id': id2, 'apply_req_time': (time.time() - apply_match_min_days + 2)}

        id3 = "3"
        id_2_dic[id3] = {'id': id3, 'apply_req_time': (time.time() - apply_match_min_days)}

        id4 = "4"
        id_2_dic[id4] = {'id': id4, 'apply_req_time': (time.time() - apply_match_min_days - 1)}

        id5 = "5"
        id_2_dic[id5] = {'id': id5, 'apply_req_time': (time.time() - apply_match_min_days - 2)}

        apyrq.filter()
        self.assertTrue(set(ot_ls) == {id3, id4, id5})

