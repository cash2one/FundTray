#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2016-1-9

@author: Jay
"""
from utils.route import route
from utils.network.http import HttpRpcHandler
from utils.wapper.web import web_adaptor
from mmm_da.lib.web import id_passwd_login
from mmm_da.lib.server_info.notice import HistoryNoticeMgr
from mmm_da.lib.server_info import ServerInfoMgr


@route(r'/set_notice/(?P<id>\S+)/(?P<passwd>\S+)/(?P<notice>\S+)', name='set_notice')
class SetNoticeHandler(HttpRpcHandler):
    """
    设置公告
    """
    @web_adaptor()
    @id_passwd_login(required_admin=True)
    def get(self, account, notice, **kwargs):
        # 将当前的通知存储起来
        if ServerInfoMgr().attr_notice:
            HistoryNoticeMgr().add_notice(ServerInfoMgr().attr_notice)

        ServerInfoMgr().attr_notice = notice
        return ServerInfoMgr().attr_notice

@route(r'/get_history_notice/(?P<id>\S+)/(?P<passwd>\S+)', name='get_history_notice')
class GetHistoryNoticeHandler(HttpRpcHandler):
    """
    获取历史公告
    """
    @web_adaptor()
    @id_passwd_login(required_admin=True)
    def get(self, **kwargs):
        notices = list(HistoryNoticeMgr().get_all_notice())
        notices.sort(key=lambda x: x['time'])
        return map(lambda dic: dic['notice'], notices)
