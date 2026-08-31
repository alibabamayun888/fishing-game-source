# encoding: utf-8
import os
import sys

# 默认thrift
DEFAULT_THRIFT_IP = '{{ thrift_ip }}' 
DEFAULT_THRIFT_PORT= {{ thrift_port }}

# mysql
MYSQL_HOST      = '{{ db_host }}'
MYSQL_PORT      = {{ db_port }}
MYSQL_DBNAME    = '{{ webdb_name }}'
MYSQL_USER      = '{{ webdb_user }}'
MYSQL_PASS      = '{{ webdb_password }}'

#默认日志目录
DEFAULT_LOG_DIR = '{{ log_dir }}'
if not os.path.exists(DEFAULT_LOG_DIR):
    DEFAULT_LOG_DIR = './logs/'
if not DEFAULT_LOG_DIR.endswith('/'):
  DEFAULT_LOG_DIR += '/' #确保带后缀 /

#微信公众号支付订单状态
WXPUBLIC_ORDER_STATUS_NO_PROCESS  = 0       #未处理
WXPUBLIC_ORDER_STATUS_HAD_PROCESS = 1       #已处理

#微信公众号支付sdk信息
WXPUBLIC_SDK_APPID  = '{{ wx_public_sdk_appid }}'
WXPUBLIC_SDK_APPKEY = '{{ wx_public_sdk_appkey }}'
WXPUBLIC_SDK_SOURCE = '{{ wx_public_sdk_source }}'

#微信公众号绑定上限
WXPUBLIC_BINDING_LIMIT = {{ wx_public_binding_limit }}

#微信公众号每日兑换红包数量限制
WXPUBLIC_EXCHANGE_DAY_LIMIT = {{ wx_public_exchange_day_limit }}

#是否开启django调试模式: True or False
DJANGO_DEBUG = {{ django_debug }}

#服务器端口
SERVER_PORT = {{ port }}

#服务器地址
SERVER_ADDR = '{{ addr }}'

#SDK下红包订单服务器地址
SDK_REDPACK_SERVER_ORDER_ADDR = '{{ sdk_redpack_host }}/order/redpack/create'

#游戏AppId,由红包SDk分配
SDK_REDPACK_SERVER_APPID = '{{ sdk_redpack_appid }}'

#红包SDk下订单签名KEY
SDK_REDPACK_SERVER_ORDER_KEY = '{{ sdk_redpack_key }}'





