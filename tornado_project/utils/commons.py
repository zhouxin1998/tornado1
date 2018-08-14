# coding=utf-8
import functools

from utils.response_code import RET

def required_login(func):
    '''理解装饰器执行过程
    @required_login
    def get(self):
    １．装饰器本身是一个函数，required_login函数装饰get函数，
    ２．required_login函数接收get函数作为参数，内部定义了wrapper函数并且返回
    ４.inner_new_fn = required_login(get)
    5.inner_new_fn(self)
    6．inner_new_fn(self)调用了wraooer函数，self作为参数传给wraooer，
    7.判断是否登录，执行func(),　　func就是get()
    '''
    @functools.wraps(func)#保证被装饰的函数对象的__name__不变
    def wrapper(request_handler_obj, *args, **kwargs):
        #判断是否登录
        if request_handler_obj.get_current_user():
            func(request_handler_obj, *args, **kwargs)
        else:
            request_handler_obj.write(dict(errcode=RET.SESSIONERR, errmsg="用户未登录"))
    return wrapper