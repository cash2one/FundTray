#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-5-27

@author: Jay
"""
from utils.route import route
from utils.network.http import HttpRpcHandler
from service_mgr.lib.service_group import ServiceGrpMgr
from service_mgr.db.db_oper import DBServiceGroupInst
from service_mgr.logic.web import require_login
from utils.wapper.web import web_adaptor, ajax_recv_wapper
from utils import logger
import traceback


@route(r'/view_service_group', name='view_service_group')
class ViewServiceGroup(HttpRpcHandler):
    """
    查看服务组
    """
    @require_login
    @web_adaptor(use_http_render=False)
    def get(self, *args, **kwargs):
        render_data = {'service_group_data': ServiceGrpMgr().id_to_dic}
        self.render('common/service_group.html', **render_data)


@route(r'/save_service_group_data', name='save_service_group_data')
class SaveServiceGroupData(HttpRpcHandler):
    """
    保存服务组参数
    """
    @require_login
    @web_adaptor()
    @ajax_recv_wapper()
    def post(self, *args, **kwargs):
        try:
            data_ls = ServiceGrpMgr().web_unpick(kwargs['js_data'])
        except:
            logger.warn("SaveServiceGroupData::post error!!!, js_data:%s traceback:%s" % (kwargs['js_data'], traceback.format_exc()))
            return

        last_data_ls = ServiceGrpMgr().get_init_data_ls()

        try:
            DBServiceGroupInst.update_diff(last_data_ls, data_ls)
            ServiceGrpMgr().init(data_ls)
        except:
            logger.warn("SaveServiceGroupData::post error!!!, data_ls:%s traceback:%s" % (data_ls, traceback.format_exc()))
            ServiceGrpMgr().init(last_data_ls)
