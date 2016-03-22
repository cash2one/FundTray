#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-12-15

@author: Jay
"""
from utils.data.cache.dirty import DirtyFlagProcess
from utils.comm_func import sub_dict
import time
from setting import *

class Account(object):
    def __init__(self, db_update_fun=None, **kwargs):
        """
        id, passwd,
        id_card, email, phone,
        leader_id,
        bank, bank_address, bank_account, bank_name,
        wechat, alipay
        :param db_update_fun:
        :param kwargs:
        :return:
        """
        self.__dict__ = kwargs

        self.dfp = DirtyFlagProcess(self)
        self.db_update_fun = db_update_fun

    def update(self, curtime):
        dirty_db_dict = self.dfp.get_db_dirty_attr()
        if dirty_db_dict and self.db_update_fun:
            dirty_db_dict['id'] = self.id
            self.db_update_fun([dirty_db_dict])

    def __str__(self):
        return str(self.get_info_dic())

    def __eq__(self, other):
        return self.id == other.id

    def __get_key(self, key):
        return self.__dict__[key] if key in self.__dict__ else getattr(self, "attr_%s" % key, "")

    def get_info_dic(self):
        """
        获取所有信息
        :return:
        """
        return dict([(key, self.__get_key(key)) for key in KEY_SET])

    def view_info_dic(self):
        """
        允许别人来查看的信息
        :return:
        """
        return dict([(key, self.__get_key(key)) for key in KEY_SET - PRIVATE_KEY_SET])

    def update_data(self, data_dic):
        """
        数据更新
        :param data_dic: 需要更新的数据
        :return:
        """
        for k, v in data_dic.items():
            self.__dict__[k] = v
        self.dfp.add_db_flag_ls(data_dic.keys())

    # leader_id
    @property
    def attr_leader_id(self):
        return self.leader_id

    # passwd
    @property
    def attr_passwd(self):
        return self.passwd

    @attr_passwd.setter
    def attr_passwd(self, new_passwd):
        if self.passwd == new_passwd or not new_passwd:
            return

        self.passwd = new_passwd
        self.dfp.add_db_flag("passwd")

    # active_coin
    @property
    def attr_active_coin(self):
        return self.active_coin

    @attr_active_coin.setter
    def attr_active_coin(self, new_coin):
        new_coin = int(new_coin)
        if new_coin < 0:
            new_coin = 0

        if new_coin == self.active_coin:
            return

        self.active_coin = new_coin
        self.dfp.add_db_flag("active_coin")

    # stat
    @property
    def attr_stat(self):
        return self.stat

    @attr_stat.setter
    def attr_stat(self, new_stat):
        if self.stat == new_stat:
            return

        self.stat = new_stat
        self.dfp.add_db_flag("stat")
        self.attr_active_time = time.time()

    # login_time
    @property
    def attr_login_time(self):
        return self.login_time

    @attr_login_time.setter
    def attr_login_time(self, new_login_time):
        if self.login_time == new_login_time:
            return

        self.login_time = new_login_time
        self.dfp.add_db_flag("login_time")

    # active_time
    @property
    def attr_active_time(self):
        return self.active_time

    @attr_active_time.setter
    def attr_active_time(self, new_active_time):
        if self.active_time == new_active_time:
            return

        self.active_time = new_active_time
        self.dfp.add_db_flag("active_time")

    # level
    @property
    def attr_level(self):
        finished_orders = self.attr_finished_accept + self.attr_finished_apply

        cur_lvel_idx = 0
        for i, lvl_req in enumerate(LEV_REQ):
            if finished_orders > lvl_req:
                cur_lvel_idx = i
            else:
                break

        return LEVEL[cur_lvel_idx]

    # team count
    @property
    def attr_team_count(self):
        from mmm_da.lib.team import TeamMgr
        return TeamMgr().team_count(self.id)

    # mafuluo
    @property
    def attr_mafuluo(self):
        return self.mafuluo

    @attr_mafuluo.setter
    def attr_mafuluo(self, new_mafuluo):
        if self.mafuluo == new_mafuluo:
            return

        if new_mafuluo < 0:
            new_mafuluo = 0

        self.mafuluo = new_mafuluo
        self.dfp.add_db_flag("mafuluo")

    #finished_apply
    @property
    def attr_finished_apply(self):
        return self.finished_apply

    @attr_finished_apply.setter
    def attr_finished_apply(self, new_finished_apply):
        if self.finished_apply == new_finished_apply:
            return

        self.finished_apply = new_finished_apply
        self.dfp.add_db_flag("finished_apply")

    #finished_accept
    @property
    def attr_finished_accept(self):
        return self.finished_accept

    @attr_finished_accept.setter
    def attr_finished_accept(self, new_finished_accept):
        if self.finished_accept == new_finished_accept:
            return

        self.finished_accept = new_finished_accept
        self.dfp.add_db_flag("finished_accept")

    #match_coin
    @property
    def attr_match_coin(self):
        return self.match_coin

    @attr_match_coin.setter
    def attr_match_coin(self, new_match_coin):
        if self.match_coin == new_match_coin:
            return

        self.match_coin = new_match_coin
        self.dfp.add_db_flag("match_coin")

    #max_apply_money
    @property
    def attr_max_apply_money(self):
        return self.max_apply_money

    @attr_max_apply_money.setter
    def attr_max_apply_money(self, new_max_apply_money):
        if self.max_apply_money == new_max_apply_money:
            return

        self.max_apply_money = new_max_apply_money
        self.dfp.add_db_flag("max_apply_money")

    @property
    def is_seal(self):
        """
        是否封号
        :return:
        """
        return self.attr_stat == SEALED

    @property
    def is_active(self):
        """
        是否激活
        :return:
        """
        return self.attr_stat == ACTIVED