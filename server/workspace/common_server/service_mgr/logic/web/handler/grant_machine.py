# coding=utf-8
"""
Created on 2015-4-22

@author: Jay
"""
from utils.route import route
from utils.network.http import HttpRpcHandler
from service_mgr.lib.grant_machine import GrantMachineMgr
from service_mgr.db.db_oper import DBGrantMachineInst
from service_mgr.logic.web import require_login
from utils.wapper.web import web_adaptor, ajax_recv_wapper
from utils import logger
import traceback

@route(r'/view_grant_machine', name='view_grant_machine')
class ViewGrantMachine(HttpRpcHandler):
    """
    查看授权主机
    """
    @require_login
    @web_adaptor(use_http_render=False)
    def get(self, *args, **kwargs):
        machine_ls = GrantMachineMgr().machine_dic.values()
        machine_ls.sort(key=lambda x: x['ip'])
        render_data = {'grant_machine_ls': machine_ls}
        self.render('common/grant_machine.html', **render_data)


@route(r'/save_grant_machine_data', name='save_grant_machine_data')
class SaveGrantMachineData(HttpRpcHandler):
    """
    保存授权机器参数
    """
    @require_login
    @web_adaptor()
    @ajax_recv_wapper()
    def post(self, *args, **kwargs):
        try:
            data_ls = GrantMachineMgr().web_unpick(kwargs['js_data'])
        except:
            logger.warn("SaveGrantMachineData::post error!!!, js_data:%s traceback:%s" % (kwargs['js_data'], traceback.format_exc()))
            return

        last_data_ls = GrantMachineMgr().get_init_data_ls()

        try:
            DBGrantMachineInst.update_diff(last_data_ls, data_ls)
            GrantMachineMgr().init(data_ls)
        except:
            logger.warn("SaveGrantMachineData::post error!!!, data_ls:%s traceback:%s" % (data_ls, traceback.format_exc()))
            GrantMachineMgr().init(last_data_ls)
