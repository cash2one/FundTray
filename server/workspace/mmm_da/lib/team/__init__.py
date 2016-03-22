#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-12-16

@author: Jay
"""
from utils.interfaces.common import IManager
from utils.meta.singleton import Singleton
from mmm_da.lib.active import UNACTIVED, ACTIVED

MAX_LAYER_COUNT = 100

class TeamMgr(IManager):
    __metaclass__ = Singleton

    def __init__(self):
        self.team_dic = {}

    def add_leader(self, id, leader_id):
        if int(id) == 0 or int(leader_id) == 0:
            return
        child_ls = self.team_dic.setdefault(str(leader_id), [])
        child_ls.append(str(id))

    def next_layer_child_ls(self, layer_id_ls):
        """
        获取下一层的id列表
        :param layer_id_ls: 当前层的id列表
        :return: []
        """
        cur_layer_child_ls = []
        [cur_layer_child_ls.extend(self.team_dic.get(id, []))
         for id in layer_id_ls]
        return cur_layer_child_ls

    def gen_layer_detail(self, layer_id_ls):
        """
        计算每层的详细激活信息
        :param layer_id_ls: 层id列表
        :return: {}
        """
        from mmm_da.lib.account.control import AccountMgr
        actived = 0
        unactived = 0
        for id in layer_id_ls:
            account = AccountMgr().get_data_by_id(id)
            if account.attr_stat == ACTIVED:
                actived += 1
            else:
                unactived +=1
        return {"sum": len(layer_id_ls), "actived": actived, "unactived": unactived}

    def summary(self, id):
        """
        团队总结
        :param id: 开始的id
        :return:
        """
        id = str(id)
        layers_summery = []
        cur_layer_child_ls = self.team_dic.get(id, [])
        cur_layer_count = 0
        while cur_layer_child_ls:
            layers_summery.append(cur_layer_child_ls)
            cur_layer_child_ls = self.next_layer_child_ls(cur_layer_child_ls)

            # 循环次数上限
            cur_layer_count += 1
            assert cur_layer_count < MAX_LAYER_COUNT

        return [self.gen_layer_detail(layer_summery) for layer_summery in layers_summery]

    def team_count(self, uid):
        """
        获取当前的团队人数
        :param uid: 用户id
        :return:
        """
        return sum([summary_info['sum'] for summary_info in self.summary(uid)])







