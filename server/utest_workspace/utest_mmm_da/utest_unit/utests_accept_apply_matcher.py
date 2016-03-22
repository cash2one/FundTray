#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-12-23

@author: Jay
"""
#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-12-22

@author: Jay
"""

from lib.common import *
from mmm_da.lib.match import AcceptApplyMatcher
import time
from utils.comm_func import make_unique_id


sacp_match_dic = {} # {"accept_order": 1, "accept_stime": time.time(), "accept_lmoney": 100000}
acp_match_dic = {}  # acp_match_dic.setdefault(acp_uid1, {"accept_order": 1, "accept_stime": time.time(), "accept_lmoney": 10000})
apy_match_dic = {}  # apy_match_dic.setdefault(apy_uid1, {'id':make_unique_id() ,'apply_req_uid': apy_uid1, 'apply_money': 500, 'apply_req_time': time.time()})

is_using_sys_accept = True
def sys_accept_check_fun():
    return is_using_sys_accept
def set_using_sys_accept(whether_use):
    global is_using_sys_accept
    is_using_sys_accept = whether_use


accept_cb_ls = []
def do_accept_cb(accept_order, apply_money):
    # 将帮助信息累计起来
    for accept_cb_info in accept_cb_ls:
        if accept_cb_info['accept_order'] == accept_order:
            accept_cb_info['apply_money'] += apply_money
            return

    accept_cb_ls.append({"accept_order": accept_order, "apply_money": apply_money})

apply_cb_ls = []
def do_apply_cb(accept_order, apply_order, apply_sorder, apply_money):
    apply_cb_ls.append({"accept_order": accept_order,
                        "apply_order": apply_order,
                        "apply_sorder": apply_sorder,
                        "apply_money": apply_money})


def clear_tmp():
    sacp_match_dic.clear()
    acp_match_dic.clear()
    apy_match_dic.clear()

    global accept_cb_ls, apply_cb_ls
    accept_cb_ls= []
    apply_cb_ls = []


def test_match_assert(test_obj, should_acp_infos, should_match, should_finish_ids):
    print "should_match,",should_match
    print "accept_cb_ls,",accept_cb_ls
    print "apply_cb_ls,",apply_cb_ls
    # accept_cb
    for accept_cb in accept_cb_ls:
        test_obj.assertTrue(accept_cb['apply_money'] == should_acp_infos[accept_cb['accept_order']])

    # apply_cb
    for apply_cb in apply_cb_ls:
        print apply_cb
        test_obj.assertTrue(apply_cb['apply_money'] == should_match[apply_cb['apply_order']][apply_cb['accept_order']])


def acp_match_ls():
    ls = [sacp_match_dic] if sys_accept_check_fun() else acp_match_dic.values()
    return ls

def apy_match_ls():
    ls = apy_match_dic.values()
    return ls

aamatch = AcceptApplyMatcher()
aamatch.init(acp_match_ls,  apy_match_ls, do_accept_cb,  do_apply_cb)

class AcceptApplyMatchTest(unittest.TestCase):

    # 初始化工作
    def setUp(self):
        pass

    # 退出清理工作
    def tearDown(self):
        pass

    @unittest_adaptor()
    def test_accept_apply_match_system_accept_11_enough(self):
        clear_tmp()
        set_using_sys_accept(True)

        acp_uid1 = "acpuid1"
        acp_order = make_unique_id()
        acp_money = 100000
        sacp_match_dic.update({"accept_uid":acp_uid1, "accept_order": acp_order, "accept_stime": time.time(), "accept_lmoney": acp_money})

        apy_uid1 = "apyuid1"
        id1 = make_unique_id()
        apy_money = 500
        apy_match_dic.setdefault(apy_uid1, {'apply_order': id1, 'apply_uid': apy_uid1, 'apply_money': apy_money, 'apply_lmoney': apy_money, 'apply_stime': time.time()})

        aamatch.match()

        should_acp_infos = {acp_order: apy_money}
        should_match = {id1: {acp_order: apy_money}}
        should_finish_ids = [id1]

        test_match_assert(self, should_acp_infos, should_match, should_finish_ids)

    @unittest_adaptor()
    def test_accept_apply_match_system_accept_11_lack(self):
        clear_tmp()
        set_using_sys_accept(True)

        acp_uid1 = "acpuid1"
        acp_order = 1
        acp_money = 500
        sacp_match_dic.update({"accept_uid":acp_uid1, "accept_order": acp_order, "accept_stime": time.time(), "accept_lmoney": acp_money})

        apy_uid1 = "apyuid1"
        apy_money = 2000
        apy_match_dic.setdefault(apy_uid1, {'apply_order':make_unique_id(), 'apply_uid': apy_uid1, 'apply_money': apy_money, 'apply_lmoney': apy_money,'apply_stime': time.time()})

        aamatch.match()

        # 申请帮助不足，不予匹配
        # accept_cb
        self.assertTrue(not accept_cb_ls)

        # apply_cb
        self.assertTrue(not apply_cb_ls)

    @unittest_adaptor()
    def test_accept_apply_match_system_accept_1n_enough(self):
        clear_tmp()
        set_using_sys_accept(True)

        acp_uid1 = "acpuid1"
        acp_order = 1
        acp_money = 100000
        sacp_match_dic.update({"accept_uid":acp_uid1, "accept_order": acp_order, "accept_stime": time.time(), "accept_lmoney": acp_money})

        apy_uid1 = "apyuid1"
        apy_money1 = 500
        id1 = make_unique_id()
        apy_match_dic.setdefault(apy_uid1, {'apply_order': id1, 'apply_uid': apy_uid1, 'apply_money': apy_money1, 'apply_lmoney': apy_money1, 'apply_stime': time.time() - 2})

        apy_uid2 = "apyuid2"
        apy_money2 = 10000
        id2 = make_unique_id()
        apy_match_dic.setdefault(apy_uid2, {'apply_order': id2, 'apply_uid': apy_uid2, 'apply_money': apy_money2, 'apply_lmoney': apy_money2, 'apply_stime': time.time() - 1})

        apy_uid3 = "apyuid3"
        apy_money3 = 2500
        id3 = make_unique_id()
        apy_match_dic.setdefault(apy_uid3, {'apply_order': id3, 'apply_uid': apy_uid3, 'apply_money': apy_money3, 'apply_lmoney': apy_money3, 'apply_stime': time.time()})

        aamatch.match()

        should_acp_infos = {acp_order: apy_money1 + apy_money2 + apy_money3}
        should_match = {id1: {acp_order: apy_money1},
                        id2: {acp_order: apy_money2},
                        id3: {acp_order: apy_money3},
                        }

        should_finish_ids = [id1, id2, id3]
        test_match_assert(self, should_acp_infos, should_match, should_finish_ids)

    @unittest_adaptor()
    def test_accept_apply_match_system_accept_1n_lack(self):
        clear_tmp()
        set_using_sys_accept(True)

        acp_uid1 = "acpuid1"
        acp_order = 1
        acp_money = 2000
        sacp_match_dic.update({"accept_uid":acp_uid1, "accept_order": acp_order, "accept_stime": time.time(), "accept_lmoney": acp_money})

        apy_uid1 = "apyuid1"
        apy_money1 = 500
        id1 = "apply_order1"
        apy_match_dic.setdefault(apy_uid1, {'apply_order': id1, 'apply_uid': apy_uid1, 'apply_money': apy_money1, 'apply_lmoney': apy_money1, 'apply_stime': time.time() - 2})

        apy_uid2 = "apyuid2"
        apy_money2 = 1000
        id2 = "apply_order2"
        apy_match_dic.setdefault(apy_uid2, {'apply_order': id2,'apply_uid': apy_uid2, 'apply_money': apy_money2, 'apply_lmoney': apy_money2, 'apply_stime': time.time() - 1})

        apy_uid3 = "apyuid3"
        apy_money3 = 1000
        id3 = "apply_order3"
        apy_match_dic.setdefault(apy_uid3, {'apply_order': id3, 'apply_uid': apy_uid3, 'apply_money': apy_money3, 'apply_lmoney': apy_money3, 'apply_stime': time.time()})

        aamatch.match()

        # apy_uid3申请帮助的金额超出接受帮助金额，不予匹配
        should_acp_infos = {acp_order: apy_money1 + apy_money2}
        should_match = {id1: {acp_order: apy_money1},
                        id2: {acp_order: apy_money2}}

        should_finish_ids = [id1, id2]
        test_match_assert(self, should_acp_infos, should_match, should_finish_ids)

    @unittest_adaptor()
    def test_accept_apply_match_accept_11_enough(self):
        clear_tmp()
        set_using_sys_accept(False)

        acp_uid1 = "acpuid1"
        acp_money1 = 100000
        acp_order1 = 1

        acp_match_dic.setdefault(acp_uid1, {"accept_uid":acp_uid1, "accept_order": acp_order1, "accept_stime": time.time(), "accept_lmoney": acp_money1})

        apy_uid1 = "apyuid1"
        apy_money = 500
        id1 = make_unique_id()
        apy_match_dic.setdefault(apy_uid1, {'apply_order': id1, 'apply_uid': apy_uid1, 'apply_money': apy_money, 'apply_lmoney': apy_money, 'apply_stime': time.time()})

        aamatch.match()

        should_acp_infos = {acp_order1: apy_money}
        should_match = {id1: {acp_order1: apy_money}}
        should_finish_ids = [id1]

        test_match_assert(self, should_acp_infos, should_match, should_finish_ids)

    @unittest_adaptor()
    def test_accept_apply_match_accept_11_lack(self):
        clear_tmp()
        set_using_sys_accept(False)

        acp_uid1 = "acpuid1"
        acp_money1 = 1000
        acp_order1 = 1

        acp_match_dic.setdefault(acp_uid1, {"accept_uid":acp_uid1, "accept_order": acp_order1, "accept_stime": time.time(), "accept_lmoney": acp_money1})

        apy_uid1 = "apyuid1"
        apy_money = 5000
        id1 = make_unique_id()
        apy_match_dic.setdefault(apy_uid1, {'apply_order': id1, 'apply_uid': apy_uid1, 'apply_money': apy_money, 'apply_lmoney': apy_money, 'apply_stime': time.time()})

        aamatch.match()

        # 申请帮助不足，不予匹配
        # accept_cb
        self.assertTrue(not accept_cb_ls)

        # apply_cb
        self.assertTrue(not apply_cb_ls)

    @unittest_adaptor()
    def test_accept_apply_match_accept_mn_enough(self):
        clear_tmp()
        set_using_sys_accept(False)

        acp_uid1 = "acpuid1"
        acp_money1 = 500
        acp_order1 = 1
        acp_match_dic.setdefault(acp_uid1, {"accept_uid":acp_uid1, "accept_order": acp_order1, "accept_stime": time.time() -2, "accept_lmoney": acp_money1})

        acp_uid2 = "acpuid2"
        acp_money2 = 2000
        acp_order2 = 2
        acp_match_dic.setdefault(acp_uid2, {"accept_uid":acp_uid2, "accept_order": acp_order2, "accept_stime": time.time() -1, "accept_lmoney": acp_money2})

        acp_uid3 = "acpuid3"
        acp_money3 = 3000
        acp_order3 = 3
        acp_match_dic.setdefault(acp_uid3, {"accept_uid":acp_uid3, "accept_order": acp_order3, "accept_stime": time.time(), "accept_lmoney": acp_money3})

        apy_uid1 = "apyuid1"
        apy_money1 = 1000
        id1 = make_unique_id()
        apy_match_dic.setdefault(apy_uid1, {'apply_order': id1, 'apply_uid': apy_uid1, 'apply_money': apy_money1, 'apply_lmoney': apy_money1, 'apply_stime': time.time() -2})

        apy_uid2 = "apyuid2"
        apy_money2 = 1000
        id2 = make_unique_id()
        apy_match_dic.setdefault(apy_uid2, {'apply_order': id2, 'apply_uid': apy_uid2, 'apply_money': apy_money2, 'apply_lmoney': apy_money2, 'apply_stime': time.time() -1})

        apy_uid3 = "apyuid3"
        apy_money3 = 2000
        id3 = make_unique_id()
        apy_match_dic.setdefault(apy_uid3, {'apply_order': id3, 'apply_uid': apy_uid3, 'apply_money': apy_money3, 'apply_lmoney': apy_money3, 'apply_stime': time.time()})

        aamatch.match()

        should_acp_infos = {acp_order1: acp_money1, acp_order2: acp_money2, acp_order3: (apy_money1 + apy_money2 + apy_money3 - acp_money1 - acp_money2)}
        should_match = {id1: {acp_order1: acp_money1, acp_order2: apy_money1-acp_money1},
                        id2: {acp_order2: apy_money2},
                        id3: {acp_order2: acp_money1+acp_money2-apy_money1-apy_money2, acp_order3: apy_money3-(acp_money1+acp_money2-apy_money1-apy_money2)}}
        should_finish_ids = [id1, id2, id3]

        test_match_assert(self, should_acp_infos, should_match, should_finish_ids)

    @unittest_adaptor()
    def test_accept_apply_match_accept_mn_lack(self):
        clear_tmp()
        set_using_sys_accept(False)

        acp_uid1 = "acpuid1"
        acp_money1 = 500
        acp_order1 = 1
        acp_match_dic.setdefault(acp_uid1, {"accept_uid":acp_uid1, "accept_order": acp_order1, "accept_stime": time.time() -2, "accept_lmoney": acp_money1})

        acp_uid2 = "acpuid2"
        acp_money2 = 2000
        acp_order2 = 2
        acp_match_dic.setdefault(acp_uid2, {"accept_uid":acp_uid2, "accept_order": acp_order2, "accept_stime": time.time() -1, "accept_lmoney": acp_money2})

        acp_uid3 = "acpuid3"
        acp_money3 = 3000
        acp_order3 = 3
        acp_match_dic.setdefault(acp_uid3, {"accept_uid":acp_uid3, "accept_order": acp_order3, "accept_stime": time.time(), "accept_lmoney": acp_money3})

        apy_uid1 = "apyuid1"
        apy_money1 = 1000
        id1 = make_unique_id()
        apy_match_dic.setdefault(apy_uid1, {'apply_order': id1, 'apply_uid': apy_uid1, 'apply_money': apy_money1, 'apply_lmoney': apy_money1, 'apply_stime': time.time() -3})

        apy_uid2 = "apyuid2"
        apy_money2 = 1000
        id2 = make_unique_id()
        apy_match_dic.setdefault(apy_uid2, {'apply_order': id2, 'apply_uid': apy_uid2, 'apply_money': apy_money2, 'apply_lmoney': apy_money2, 'apply_stime': time.time() -2})

        apy_uid3 = "apyuid3"
        apy_money3 = 2000
        id3 = make_unique_id()
        apy_match_dic.setdefault(apy_uid3, {'apply_order': id3, 'apply_uid': apy_uid3, 'apply_money': apy_money3, 'apply_lmoney': apy_money3, 'apply_stime': time.time() -1})

        apy_uid4 = "apyuid4"
        apy_money4 = 20000
        id4 = make_unique_id()
        apy_match_dic.setdefault(apy_uid4, {'apply_order': id4, 'apply_uid': apy_uid4, 'apply_money': apy_money4, 'apply_lmoney': apy_money4, 'apply_stime': time.time()})

        aamatch.match()

        # apy_uid4 超出接受帮助范围，无法投资
        should_acp_infos = {acp_order1: acp_money1, acp_order2: acp_money2, acp_order3: (apy_money1 + apy_money2 + apy_money3 - acp_money1 - acp_money2)}
        should_match = {id1: {acp_order1: acp_money1, acp_order2: apy_money1-acp_money1},
                        id2: {acp_order2: apy_money2},
                        id3: {acp_order2: acp_money1+acp_money2-apy_money1-apy_money2, acp_order3: apy_money3-(acp_money1+acp_money2-apy_money1-apy_money2)}}
        should_finish_ids = [id1, id2, id3]

        test_match_assert(self, should_acp_infos, should_match, should_finish_ids)

