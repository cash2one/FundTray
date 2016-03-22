#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-12-21

@author: Jay
"""
from utils.interfaces.common import IManager
from utils.meta.singleton import Singleton
from utils.comm_func import make_unique_id
from utils import logger
import copy


class AcceptApplyMatcher(IManager):
    """
    接受帮助匹配申请帮助
    """
    __metaclass__ = Singleton

    def __init__(self):
        self.__acp_match_ls_fun = None
        self.__apy_match_ls_fun = None
        self.do_accept_cb_fun = None
        self.do_apply_cb_fun = None
        self.make_unique_id_func = None

    def init(self,
             acp_match_ls_fun,
             apy_match_ls_fun,
             do_accept_cb_fun=lambda accept_order, apply_money: "",
             do_apply_cb_fun=lambda accept_order, apply_order, apply_sorder, apply_uid, apply_money: "",
             make_unique_id_func=make_unique_id):
        """
        接受帮助匹配申请帮助初始化
        :param acp_match_ls_fun:  用户接受匹配信息列表获取函数
        :param apy_match_ls_fun:  用户申请匹配信息列表获取函数
        :param do_accept_cb_fun:  接受匹配处理回调
        :param do_apply_cb_fun:   申请匹配处理回调
        :return:
        """
        self.__acp_match_ls_fun = acp_match_ls_fun
        self.__apy_match_ls_fun = apy_match_ls_fun
        self.do_accept_cb_fun = do_accept_cb_fun
        self.do_apply_cb_fun = do_apply_cb_fun
        self.make_unique_id_func = make_unique_id_func

    def match(self):
        """
        匹配接受帮助和申请帮助
        :return:
        """
        accept_match_ls, apply_match_ls = self.prepare()
        logger.warn("AcceptApplyMatcher::match start!!! accept_match_ls:%s, apply_match_ls:%s"
                    % (accept_match_ls, apply_match_ls))

        # 匹配接受帮助和申请帮助
        for apply_help_dic in apply_match_ls:
            if apply_help_dic['apply_lmoney'] == 0:
                continue

            # 匹配结果
            matched_ls = self._match_mapper(apply_help_dic, accept_match_ls)
            if not matched_ls:
                logger.warn("AcceptApplyMatcher::match not matched_ls, apply_help_dic:%s accept_match_ls:%s"
                            % (apply_help_dic, accept_match_ls))
                continue

            self.matched_proc(apply_help_dic, matched_ls)
            logger.warn("AcceptApplyMatcher::match success!!!, apply_help_dic:%s matched_ls:%s" % (apply_help_dic, matched_ls))

    def prepare(self):
        """
        数据准备
        :return:
        """
        accept_match_ls = copy.deepcopy(self.__acp_match_ls_fun())
        accept_match_ls.sort(key=lambda x: x['accept_stime'])

        apply_match_ls = copy.deepcopy(self.__apy_match_ls_fun())
        apply_match_ls.sort(key=lambda x: x['apply_stime'])
        return accept_match_ls, apply_match_ls

    @staticmethod
    def _match_mapper(apply_help_dic, accept_matching_ls):
        """
        数据组合处理
        :param apply_help_dic: 请求申请帮助信息
        :param accept_matching_ls: 接受帮助的匹配列表, {"accept_order":接受帮助订单, "accept_money":接受帮助金钱,,,,}
        :return: [{"accept_order":接受帮助订单, "apply_money":接受帮助金钱}]
        """
        apply_money = apply_help_dic['apply_lmoney']

        # 尝试匹配
        accept_try_match_ls = []

        for i, accept_help in enumerate(accept_matching_ls):
            # 如果是自己不能匹配
            if apply_help_dic['apply_uid'] == accept_help['accept_uid']:
                continue

            if apply_money == 0:
                break

            # 如果剩余接受帮助金额为0, 不接受匹配
            if accept_help['accept_lmoney'] == 0:
                continue

            # 匹配金额
            match_money = apply_money \
                if apply_money <= accept_help['accept_lmoney'] \
                else accept_help['accept_lmoney']

            accept_try_match_ls.append({"accept_help": accept_help, "match_money": match_money})
            apply_money -= match_money
            assert apply_money >= 0

        # 没有匹配完成/只有部分匹配 不正式匹配
        if apply_money > 0:
            return []

        # 正式匹配
        accept_matched_ls = []
        for accept_info in accept_try_match_ls:
            accept_help = accept_info['accept_help']
            match_money = accept_info['match_money']

            accept_matched_ls.append({"accept_order": accept_help['accept_order'], "apply_money": match_money})
            accept_help['accept_lmoney'] = accept_help['accept_lmoney'] - match_money
            assert accept_help['accept_lmoney'] >= 0

        return accept_matched_ls

    @staticmethod
    def matched_proc(apply_help_dic, accept_matched_ls):
        """
        匹配到的请求帮助处理
        :param apply_help_dic: 申请帮助信息字典
        :param accept_matched_ls: [{"accept_order": 接受帮助订单id, "apply_money": 提供帮助金额})]
        :return:
        """
        # 申请帮助处理
        [AcceptApplyMatcher().do_apply_cb_fun(accept_info['accept_order'],
                                              apply_help_dic['apply_order'],
                                              AcceptApplyMatcher().make_unique_id_func(),
                                              accept_info['apply_money'])
         for accept_info in accept_matched_ls]

        #  接受帮助处理
        cache_dic = {}
        [cache_dic.update({acped['accept_order']:cache_dic.get(acped['accept_order'], 0) + acped['apply_money']})
         for acped in accept_matched_ls]

        [AcceptApplyMatcher().do_accept_cb_fun(accept_order, apply_money)
         for accept_order, apply_money in cache_dic.items()]

