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



#是否开启django调试模式: True or False
DJANGO_DEBUG = {{ django_debug }}

#服务器端口
SERVER_PORT = {{ port }}

#服务器地址
SERVER_ADDR = '{{ addr }}'




