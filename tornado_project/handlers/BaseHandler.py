# coding=utf-8
import json

from tornado.web import RequestHandler,StaticFileHandler
from utils.session import Session

class BaseHandler(RequestHandler):
    """handler基类"""
    @property
    def db(self):
        """作为RequestHandler对象的db属性"""
        return self.application.db

    @property
    def redis(self):
        """作为RequestHandler对象的redis属性"""
        return self.application.redis

    def prepare(self):
        """预解析json数据"""
        if self.request.headers.get("Content-Type","").startswith("application/json"):
            self.json_args = json.loads(self.request.body)
        else:
            self.json_args = {}

    def write_error(self):
        pass

    def set_default_headers(self):
        """设置默认json格式"""
        self.set_header("Content-Type","application/json; charset=UTF-8")

    def get_current_user(self):
        """判断用户是否登录"""
        self.session = Session(self)
        return self.session.data


    def initialize(self):
        pass

    def on_finish(self):
        pass

# 开启xsrf验证
class StaticFileHandler(StaticFileHandler):
    def __init__(self,*args, **kwargs):
        super(StaticFileHandler, self).__init__(*args, **kwargs)
        self.xsrf_token