# coding=utf-8
"""
Created on 2015-4-22

@author: Jay
"""
import os

from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader
from tornado import web

from utils.route import Route
from utils.meta.singleton import Singleton
from utils.network.http import HttpRpcServer
from utils.comm_func import import_handlers
from utils import __path__ as utils_paths

CUR_FILE_PATH = os.path.realpath(__file__)
CUR_FILE_DIR_PATH = os.path.dirname(CUR_FILE_PATH)

settings = {"static_path": os.path.join(utils_paths[0], "web", "static"),
            "template_path": [os.path.join(utils_paths[0], "web", "template"),
                              os.path.join(os.path.dirname(CUR_FILE_DIR_PATH), "logic", "web", "template")],
            'cookie_secret': "SZUzonpBQIuXE3yKBtWPre2N5AS7jEQKv0Kioj9iKT0="}

ssl_args = {"certfile": os.path.join(utils_paths[0], "CA", "server.crt"),
            "keyfile": os.path.join(utils_paths[0], "CA", "server.key")}



class WebApp(HttpRpcServer):
    __metaclass__ = Singleton

    def __init__(self, port, is_https):
        # import handlers
        handler_path = os.path.join(os.path.dirname(CUR_FILE_DIR_PATH), "logic", "web", "handler")
        import_path = "logic.web.handler"
        import_handlers(handler_path, import_path)

        # register handlers
        handlers = [web.url(r"/static/(.+)",
                            web.StaticFileHandler,
                            dict(path=settings['static_path']),
                            name='static_path')] + Route.routes()

        jinja_environment = Environment(loader=FileSystemLoader(settings['template_path']),
                                        auto_reload=True,
                                        autoescape=False)

        jinja_environment.filters['lt_gt'] = lambda s: s.replace('<', '&lt;').replace('>', '&gt;')
        jinja_environment.globals['settings'] = settings
        super(WebApp, self).__init__(ssl_args if is_https else {}, port, handlers, jinja_env=jinja_environment, **settings)