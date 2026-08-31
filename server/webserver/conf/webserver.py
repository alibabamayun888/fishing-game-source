# encoding: utf-8
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 默认thrift
DEFAULT_THRIFT_IP = '127.0.0.1' 
DEFAULT_THRIFT_PORT= 10081 # 20899

# mysql
MYSQL_HOST      = '127.0.0.1'
MYSQL_PORT      = 3306
MYSQL_DBNAME    = 'fish_websvrdb'
MYSQL_USER      = 'root'
MYSQL_PASS      = 'xmen123456'

#默认日志目录
DEFAULT_LOG_DIR = '/data/logs/fish/web_server/'
if not os.path.exists(DEFAULT_LOG_DIR):
    DEFAULT_LOG_DIR = './logs/'
if not DEFAULT_LOG_DIR.endswith('/'):
  DEFAULT_LOG_DIR += '/' #确保带后缀 /

#微信公众号支付订单状态
WXPUBLIC_ORDER_STATUS_NO_PROCESS  = 0       #未处理
WXPUBLIC_ORDER_STATUS_HAD_PROCESS = 1       #已处理

#微信公众号支付sdk信息
WXPUBLIC_SDK_APPID  = '5b7393d30e824261ab0f82e1fb5f853a'
WXPUBLIC_SDK_APPKEY = 'f2330e5f2e9249ee80ca745cfc14dc49'
WXPUBLIC_SDK_SOURCE = 'GZHZF-01_115'

#微信公众号绑定上限
WXPUBLIC_BINDING_LIMIT = 10

#微信公众号每日兑换红包数量限制
WXPUBLIC_EXCHANGE_DAY_LIMIT = 5

#是否开启django调试模式: True or False
DJANGO_DEBUG = True

#服务器端口
SERVER_PORT = 12198

#服务器地址
SERVER_ADDR = '0.0.0.0'

#SDK下红包订单服务器地址
# SDK_REDPACK_SERVER_ORDER_ADDR = 'https://apirp.wcsdk.poker3a.com/order/redpack/create' #正式地址
SDK_REDPACK_SERVER_ORDER_ADDR = 'http://sanbox-apirp.wcsdk.mb1768.cn/order/redpack/create' #沙箱环境

#游戏AppId,由红包SDk分配
SDK_REDPACK_SERVER_APPID = '446bf9871aca4e22b0537017f88841ce'

#红包SDk下订单签名KEY
SDK_REDPACK_SERVER_ORDER_KEY = '247588ba8dbe40baac994645e9f64ba6'

