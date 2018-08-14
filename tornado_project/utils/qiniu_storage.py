# coding=utf-8
# flake8: noqa

from qiniu import Auth, put_data, etag
import qiniu.config

import logging

#需要填写你的 Access Key 和 Secret Key
access_key = '1eWcbce_GdaD79esHWaPs_kDGDTmxRLkGGbgsNy_'
secret_key = 'dSUSNJ6yp10Pz3ym7CZ8iEyCEnyj5DXYd71ktwMg'

def storage(file_data):
    try:
        #构建鉴权对象
        q = Auth(access_key, secret_key)

        #要上传的空间
        bucket_name = 'ihome'

        #上传到七牛后保存的文件名
        # key = 'my-python-logo.png'

        #生成上传 Token，可以指定过期时间等
        token = q.upload_token(bucket_name, None, 3600)

        # #要上传文件的本地路径
        # localfile = './sync/bbb.jpg'

        ret, info = put_data(token, None, file_data)
        # print(info)
    except Exception as e:
        logging.error(e)
        raise e

    if 200 == info.status_code:
        return ret['key']
    else:
        raise Exception("上传失败")
    # assert ret['key'] == key
    # assert ret['hash'] == etag(localfile)

if __name__ == '__main__':
    file_name = raw_input('输入文件：')
    with open(file_name,'rb') as file:
        file_data = file.read()
        ret = storage(file_data)
        print(ret)