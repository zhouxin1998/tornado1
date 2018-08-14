# coding=utf-8
import logging
import re
import random

from .BaseHandler import BaseHandler
from utils.captcha.captcha import captcha
from utils.response_code import RET
from constants import IMAGE_CODE_EXPIRES_SECONDS,SMS_CODE_EXPIES_SECONDS

from libs.yuntongxun.SendTemplateSMS import ccp

class ImageCodeHandler(BaseHandler):
    """图片验证码"""
    def get(self):
        """获取图片验证码"""
        cur_code_id = self.get_argument('cur',"")
        pre_code_id = self.get_argument("pre","")

        """生成图片验证码"""
        name, text, pic = captcha.generate_captcha()
        try:
            if pre_code_id:
                self.redis.delete("pic_code_%s" % pre_code_id)
            self.redis.setex("pic_code_%s" % cur_code_id, IMAGE_CODE_EXPIRES_SECONDS,text)
        except Exception as e:
            logging.error(e)
            self.write("")

        self.set_header("Content-Type", "image/jpg")
        self.write(pic)

class PhonecodeHandler(BaseHandler):
    """短信验证"""
    def post(self):
        """获取参数"""
        mobile = self.json_args.get("mobile")
        piccode = self.json_args.get("piccode")
        piccode_id = self.json_args.get("piccode_id")
        # 参数校验
        if not all((mobile,piccode,piccode_id)):
            return self.write(dict(errcode=RET.PARAMERR, errmsg="参数缺失"))
        if not re.match(r"^1\d{10}$", mobile):
            return self.write(dict(errcode=RET.PARAMERR, errmsg="手机号格式错误"))
        # 获取图片验证码真实值
        try:
            real_piccode = self.redis.get("pic_code_%s" % piccode_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg="查询验证码有误"))
        if not real_piccode:
            return self.write(dict(errcode=RET.NODATA, errmsg="验证码过期"))
        # 删除图片验证码
        try:
            self.redis.delete('pic_code_%s' % piccode_id)
        except Exception as e:
            logging.error(e)
        if real_piccode.lower() != piccode.lower():
            return self.write(dict(errcode=RET.DATAERR, errmsg="验证码错误"))
#       手机号是否存在
        sql = "select count(*) counts from ih_user_profile where up_mobile=%s"
        try:
            ret = self.db.get(sql, mobile)
            print(ret)
        except Exception as e:
            logging.error(e)
        else:
            if 0 != ret["counts"]:
                return self.write(dict(errcode=RET.DATAEXIST, errmsg="手机号已注册"))

        # 产生随机短信验证码
        sms_code = "%06d" % random.randint(1,1000000)
        try:
            self.redis.setex("sms_code_%s" % mobile,SMS_CODE_EXPIES_SECONDS, sms_code)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg="数据库出错"))

        # 发送短信验证码
        try:
            result = ccp.sendTemplateSMS(mobile, [sms_code,SMS_CODE_EXPIES_SECONDS/60],1)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.THIRDERR, errmsg="发送短信失败"))
        if result:
            self.write(dict(errcode=RET.OK, errmsg="发送成功"))
        else:
            self.write(dict(errcode=RET.UNKOWNERR, errmsg="发送失败"))





