#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-12-22

@author: Jay
"""
from utils import logger
from utils.scheduler import Jobs
from utils.service_control.parser import ArgumentParser
from mmm_da.lib.filter.control import AcceptReqFilter, ApplyReqFilter, ApplyWaitFilter, ApplyPayFilter
from mmm_da.lib.match import AcceptApplyMatcher
from mmm_da.lib.server_info import  ServerInfoMgr
from mmm_da.lib.help.control import AcceptHelpMgr, ApplyHelpMgr



def init_cron_job():
    """
    初始化系统cron job
    :return:
    """
    apply_req = ArgumentParser().args.apply_req
    match = ArgumentParser().args.match
    apply_pay = ArgumentParser().args.apply_pay
    accept_req = ArgumentParser().args.accept_req
    apply_wait = ArgumentParser().args.apply_wait

    # init
    AcceptApplyMatcher().init(AcceptHelpMgr().match_ls,
                              ApplyHelpMgr().match_ls,
                              AcceptHelpMgr().do_accept,
                              ApplyHelpMgr().do_apply,
                              ServerInfoMgr().make_unique_id)

    Jobs().add_cron_job(ApplyReqFilter().filter,
                        **{apply_req.split('_')[0]: int(apply_req.split('_')[1])})
    Jobs().add_cron_job(AcceptApplyMatcher().match,
                        **{match.split('_')[0]: int(match.split('_')[1])})

    if ArgumentParser().args.enable_pay_check:
        Jobs().add_cron_job(ApplyPayFilter().filter,
                            **{apply_pay.split('_')[0]: int(apply_pay.split('_')[1])})

    Jobs().add_cron_job(AcceptReqFilter().filter,
                        **{accept_req.split('_')[0]: int(accept_req.split('_')[1])})
    Jobs().add_cron_job(ApplyWaitFilter().filter,
                        **{apply_wait.split('_')[0]: int(apply_wait.split('_')[1])})
    [logger.warn("cron job:%s" % {"cron": cron_job.cron, "func": cron_job.func}) for cron_job in Jobs().cron_job]

