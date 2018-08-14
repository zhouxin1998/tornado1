# coding=utf-8

import os

current_path = os.path.dirname(__file__)
settings = {
    "static_path": os.path.join(current_path, "static"),
    "template_path": os.path.join(current_path, "template"),
    "cookie_secret": "jV8kzwh5Ra23YBhvRtgXKFrJ9NfggkhyihcHtstCAIc=",
    # "xsrf_cookies": True,
    "debug": True,
}

# mysql
mysql_options = dict(
    host = "127.0.0.1",
    database = "ihome",
    user = "root",
    password = "mysql"
)

# redis
redis_options = dict(
    host = "127.0.0.1",
    port = 6379,
)

# 日志配置
# log_path = os.path.join(current_path, "logs/log")
log_path = os.path.join(os.path.dirname(__file__), "logs/log")

log_level = "debug"

passwd_hash_key = "nlgCjaTXQX2jpupQFQLoQo5N4OkEmkeHsHD9+BBx2WQ="