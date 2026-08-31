# encoding: utf-8

import os

basedir = os.path.abspath(os.path.dirname(__file__))
logdir = os.path.join(basedir, 'reportlog')

import logging
# 忽略登录验证码
VC_IGNORE = True
# 游戏服不需要支持小游戏排行榜，设置为 False
LB_ENABLE = True

class Config():
    """
    配置表
    """

    # DEBUG = True

    # MySQL
    DIALECT = 'mysql'
    DRIVER = 'mysqldb'
    USERNAME = {{ sdb_user }}
    PASSWORD = {{ sdb_password }}
    HOST = {{ sdb_host }}
    PORT = {{ db_port }}
    DATABASE = {{ sdb_name }}

    # SQLAlchemy
    # export DATABASE_URL=mysql+mysqldb://root:xmen2018@127.0.0.1:3306/fish1
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              '{}+{}://{}:{}@{}:{}/{}'.format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = False

    # WTF
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = 'xmenfish'
    SECRET_KEY = 'xmenfish'

    #thrift
    THRIFT_DEFAULT_PLATFORM_IP = {{ thrift_ip }}
    THRIFT_DEFAULT_PLATFORM_PORT = {{ thrift_port }}

    #后台端口
    RUN_PORT = {{ port }}
    
    #日志配置
    LOG_LEVEL = logging.DEBUG #debug info error
    LOG_DIR = '{{ log_dir }}/' #文件夹全路径，后面要有/
    LOG_FILE = '{{ log_file }}' #日志文件名
