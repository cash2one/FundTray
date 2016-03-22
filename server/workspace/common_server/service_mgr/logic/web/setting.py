# coding=utf-8
"""
Created on 2015-4-23

@author: Jay
"""
from utils.service_control.setting import ST_SERVICE_MGR, TP_SERVICE_TYPE
from service_mgr.lib.service_group import ServiceGrpMgr

# [关闭, 正在开启, 已经开启, 关闭中]
[CLOSED, OPENING, OPEN, CLOSING] = xrange(4)

menu = [{"name": '通用', 'url': '/common'},
        {'name': '服务管理', 'url': '/service_manager'},
        {'name': '用户管理', 'url': '/user'}]

service_manager = [{'name': '所有逻辑服务', 'url': '/view_all_service'},
                   {'name': '第三方服务', 'url': '/view_tp_service'}]
service_manager.extend([{'name': service, 'url': '/view_logic_service?service=%s' % service}
                        for service in ServiceGrpMgr().get_service_grps()
                        if service != ST_SERVICE_MGR and service not in TP_SERVICE_TYPE])


common_manager = [{'name': '授权主机', 'url': '/view_grant_machine'},
                  {'name': '服务器组', 'url': '/view_service_group'}
                  ]