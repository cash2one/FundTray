#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2016-2-20

@author: Jay
"""
from lib.common import *
from mmm_da.lib.filter.control import ApplyWaitFilter
import time


apply_aft_accept_hour = 1
hours_diff_fun = lambda d1, d2: int((d1 - d2) / 1)
uid_2_dic = {}

ot_ls = []
def cb_fun(uid):
    ot_ls.append(uid)


def clear_tmp():
    global ot_ls
    global uid_2_dic
    ot_ls= []
    uid_2_dic.clear()


def get_apply_wait_ls():
    return uid_2_dic.values()

ahw = ApplyWaitFilter()
filter_params = {}
filter_params.setdefault("apply_aft_accept_hour", apply_aft_accept_hour)
filter_params.setdefault("hours_diff_fun", hours_diff_fun)
ahw.init(get_apply_wait_ls, cb_fun, filter_params)



class ApplyWaitCheckerTest(unittest.TestCase):
    @unittest_adaptor()
    def test_apply_pay_not_ot(self):
        clear_tmp()
        uid2 = "2"
        uid_2_dic[uid2] = {'apply_wait_time': (time.time()),
                           'apply_wait_uid': uid2}

        ahw.filter()
        self.assertTrue(not ot_ls)

    @unittest_adaptor()
    def test_apply_pay_ot1(self):
        clear_tmp()
        uid2 = "2"
        uid_2_dic[uid2] = {'apply_wait_time': (time.time() - apply_aft_accept_hour),
                           'apply_wait_uid': uid2}

        ahw.filter()
        self.assertTrue(ot_ls == [uid2])

    @unittest_adaptor()
    def test_apply_pay_ot_much(self):
        clear_tmp()
        uid2 = "2"
        uid_2_dic[uid2] = {'apply_wait_time': (time.time() - apply_aft_accept_hour - 1),
                           'apply_wait_uid': uid2}

        uid3 = "3"
        uid_2_dic[uid3] = {'apply_wait_time': (time.time() - apply_aft_accept_hour - 2),
                           'apply_wait_uid': uid3}

        uid4 = "4"
        uid_2_dic[uid4] = {'apply_wait_time': (time.time() - apply_aft_accept_hour),
                           'apply_wait_uid': uid4}

        uid5 = "5"
        uid_2_dic[uid5] = {'apply_wait_time': (time.time()),
                           'apply_wait_uid': uid5}

        ahw.filter()
        print "ot_ls,",ot_ls
        self.assertTrue(set(ot_ls) == {uid2, uid3, uid4})
