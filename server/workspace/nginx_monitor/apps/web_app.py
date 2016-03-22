# coding=utf-8
"""
Created on 2015-4-25

@author: Jay
"""
import os
from utils.route import Route
from utils.meta.singleton import Singleton
from utils.network.http import HttpRpcServer
from utils.comm_func import import_handlers

ssl_args = {"certfile": os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                     "common_server", "utils", "CA", "server.crt"),
            "keyfile": os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                    "common_server", "utils", "CA", "server.key")}


class WebApp(HttpRpcServer):
    """
    Web服务
    """
    __metaclass__ = Singleton

    def __init__(self, port, is_https):
        # import handlers
        handler_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "logic", "web", "handler")
        import_path = "logic.web.handler"
        import_handlers(handler_path, import_path)

        # register handlers
        super(WebApp, self).__init__(ssl_args if is_https else {}, port, Route.routes())
