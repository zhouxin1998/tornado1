# coding=utf-8
import logging
import re
import hashlib
import config


from .BaseHandler import BaseHandler
from utils.response_code import RET
from utils.session import Session
from utils.commons import required_login

class IndexHandler(BaseHandler):
    def get(self):
        logging.debug("debug msg")
        logging.info("info msg")
        logging.warning("warning msg")
        logging.error("error msg")
        self.write("hello")

class RegisterHandler(BaseHandler):
    """注册"""
    def post(self):
        """获取参数"""
        mobile = self.json_args.get("mobile")
        sms_code = self.json_args.get("phonecode")
        password = self.json_args.get("password")

        #检验参数
        if not all([mobile,sms_code,password]):
            return self.write(dict(errcode=RET.PARAMERR, errmsg="参数不完整"))
        if not re.match(r"^1\d{10}",mobile):
            return self.write(dict(errcode=RET.DATAERR, errmsg="手机号格式错误"))

        # 判断短信验证码是否正确
        if "" != sms_code:
            try:
                real_sms_code = self.redis.get("sms_code_%s"%mobile)
            except Exception as e:
                logging.error(e)
                return self.write(dict(errcode=RET.DBERR, errmsg="查询验证码错误"))
            # 判断短信验证码是否过期
            if not real_sms_code:
                return self.write(dict(errcode=RET.NODATA, errmsg="验证码过期"))
            # 对比用户填写的验证码与真实值
            if real_sms_code != sms_code:
                return self.write(dict(errcode=RET.DATAERR, errmsg="验证码错误"))
            try:
                self.redis.delete("sms_code_%s"%mobile)
            except Exception as e:
                logging.error(e)

        # 保存数据库，同时判断手机号是否存在
        passwd = hashlib.sha256(password+config.passwd_hash_key).hexdigest()
        sql = "insert into ih_user_profile(up_name, up_mobile, up_passwd) values(%(name)s,%(mobile)s,%(passwd)s);"
        try:
            user_id = self.db.execute(sql, name=mobile, mobile=mobile,passwd=passwd)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DATAEXIST, errmsg="手机号已存在"))

        # 用session记录用户的登录状态　注册成功表示已登陆
        session = Session(self)
        session.data['user_id'] = user_id
        session.data['mobile'] = mobile
        session.data['name'] = mobile
        try:
            session.save()
        except Exception as e:
            logging.error(e)

        self.write(dict(errcode=RET.OK, errmsg="注册成功"))

class CheckLoginHandler(BaseHandler):
    """检验是否登录"""
    def get(self):
        if self.get_current_user():
            self.write({"errcode":RET.OK, "errmsg":"true","data":{"name":self.session.data.get("name")}})
        else:
            self.write({"errcode":RET.SESSIONERR, "errmsg":"false"})

class LogoutHandler(BaseHandler):
    """退出登录"""
    @required_login
    def get(self):
        # session = Session(self)
        self.session.clear()
        self.write({"errcode": RET.OK, "errmsg": "成功退出"})

class LoginHandler(BaseHandler):
    """登录"""
    def post(self):
        mobile = self.json_args.get('mobile')
        passwd = self.json_args.get('password')
        # print(mobile)
        #检测参数
        if not all([mobile,passwd]):
            return self.write(dict(errcode=RET.PARAMERR,errmsg="参数错误"))
        if not re.match(r'^1\d{10}$',mobile):
            return self.write(dict(errcode=RET.DATAERR,errmsg="手机号错误"))
        # 查询用户名密码
        sql = "select up_user_id,up_name,up_passwd from ih_user_profile where up_mobile=%(mobile)s"
        results = self.db.get(sql, mobile=mobile)
        # results = self.db.get("select up_user_id,up_name,up_passwd from ih_user_profile where up_mobile=%(mobile)s", mobile=mobile)
        passwd = hashlib.sha256(passwd+config.passwd_hash_key).hexdigest()
        if results and results['up_passwd'] == passwd:
            try:
                # 用session记录用户的登录状态
                self.session = Session(self)
                self.session.data['user_id'] = results['up_user_id']
                self.session.data['name'] = results['up_name']
                self.session.data['mobile'] = mobile
                self.session.save()
                return self.write(dict(errcode=RET.OK, errmsg="OK"))
            except Exception as e:
                logging.error(e)
            return self.write(dict(errcode=RET.OK, errmsg="ok"))
        else:
            return self.write(dict(errcode=RET.DATAERR, errmsg="手机号或者密码错误"))
