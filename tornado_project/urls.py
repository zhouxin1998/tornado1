# coding=utf-8
from handlers import Passpoer,VerificationCode,profile
from handlers.BaseHandler import StaticFileHandler as StaticFileHandler

import os
cu_path = os.path.dirname(__file__)
urls = [
    # (r'/', Passpoer.IndexHandler),/api/phonecode
    (r'/api/piccode', VerificationCode.ImageCodeHandler),#验证码
    (r'/api/phonecode', VerificationCode.PhonecodeHandler),#短信验证
    (r'/api/register', Passpoer.RegisterHandler),#注册
    (r'/api/login', Passpoer.LoginHandler),#登录
    (r'/api/logout', Passpoer.LogoutHandler),#退出
    (r'/api/check_login', Passpoer.CheckLoginHandler),   #判断用户是否登录
    (r'/api/profile', profile.ProfileHandler),   #个人信息
    (r'/api/profile/avatar', profile.AvatarHandler),#上传头像
    (r'/api/profile/name', profile.UnameHandler),#修改用户名
    (r'/api/profile/auth', profile.AuthHandler),  # 修改用户名


    (r'/(.*)',StaticFileHandler,dict(path=os.path.join(cu_path,"html"),default_filename='index.html'))


]
