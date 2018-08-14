# coding=utf-8
import logging

from .BaseHandler import BaseHandler
from utils.commons import required_login
from utils.response_code import RET
from utils.qiniu_storage import storage

from constants import QINIU_URL_PREFIX

class ProfileHandler(BaseHandler):
    """个人信息"""
    @required_login
    def get(self):
        user_id = self.session.data['user_id']
        try:
            # ret = self.db.get("select up_name,up_mobile,up_avatar from ih_user_profile where up_user_id=%s", user_id)
            sql = "select up_name,up_mobile,up_avatar from ih_user_profile where up_user_id=%s"
            ret = self.db.get(sql,user_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, ermsg="get data error"))

        if ret['up_avatar']:
            avatar_url = QINIU_URL_PREFIX+ret['up_avatar']
        else:
            avatar_url = None
        self.write({"errcode":RET.OK,"errmsg":"OK","data":{
                "user_id": user_id,
                "name":ret['up_name'],
                "mobile":ret['up_mobile'],
                "avatar":avatar_url
            }})

class AvatarHandler(BaseHandler):
    """上传头像"""
    @required_login
    def post(self):
        files = self.request.files.get('avatar')
        if not files:
            return self.write(dict(errcode=RET.PARAMERR, errmsg='未传图片'))
        file = files[0]['body']
        try:
            #　调用7牛空间保存图片
            file_name = storage(file)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.THIRDERR, errmsg='上传失败'))
        user_id = self.session.data['user_id']
        # sql = "update ih_user_profile set up_avatar=%(avatar)s where up_user_id=%(user_id)s"
        #　保存到数据库
        sql = "update ih_user_profile set up_avatar=%(avatar)s where up_user_id=%(user_id)s"
        try:
           self.db.execute_rowcount(sql,avatar=file_name, user_id=user_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg='保存错误'))
        avater_url = QINIU_URL_PREFIX + file_name
        self.write(dict(errcode=RET.OK, errmsg="保存成功",data=avater_url))



class UnameHandler(BaseHandler):
    """用户名"""
    @required_login
    def post(self):
        # 从session中获取当前的登录的用户id
        user_id = self.session.data['user_id']
        uname = self.json_args.get('name')#获取要更改的用户名
        # if not uname:
        if uname in (None, ""):
            return self.write(dict(errcode=RET.PARAMERR, errmsg="params error"))
        # 保存用户昵称name，并同时判断name是否重复（利用数据库的唯一索引)

        sql = 'update ih_user_profile set up_name=%s where up_user_id=%s'
        try:
            # self.db.execute_rowcount("update ih_user_profile set up_name=%s where up_user_id=%s", uname, user_id)
            self.db.execute_rowcount(sql,uname,user_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.OK, errmsg="name has exist"))

        # 修改session数据中的name字段，并保存到redis中
        self.session.data['name'] = uname
        try:
            self.session.save()
        except Exception as e:
            logging.error(e)
        self.write(dict(errcode=RET.OK, errmsg="OK"))

class AuthHandler(BaseHandler):
    """实名认证"""
    @required_login
    def get(self):
        user_id = self.session.data['user_id']
        # 查询数据库中是否存在姓名和身份证号码
        sql = 'select up_real_name,up_id_card from ih_user_profile where up_user_id=%s'
        try:
            ret = self.db.get(sql,user_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR,errmsg="数据库查询错误"))
        if not ret:
            self.write(dict(errcode=RET.DBERR,errmsg="数据库查询错误"))
        else:
            self.write({"errcode":RET.OK,"errmsg":"ok","data":{"real_name":ret['up_real_name'],"id_card":ret['up_id_card']}})

    @required_login
    def post(self):
        user_id = self.session.data['user_id']
        real_name = self.json_args.get('real_name', '')
        id_card = self.json_args.get('id_card', '')
        if not all((real_name,id_card)):
            return self.write(dict(errcode=RET.PARAMERR,errmsg="params error"))
        #更新实名认证，判断实名身份证格式
        sql = "update ih_user_profile set up_real_name=%s,up_id_card=%s where up_user_id=%s"
        try:
            # self.db.execute_rowcount("update ih_user_profile set up_real_name=%s,up_id_card=%s where up_user_id=%s", real_name, id_card, user_id)
            self.db.execute_rowcount(sql,real_name,id_card,user_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR,errmsg="update failed"))
        self.write({"errcode":RET.OK,"errmsg":"OK"})




