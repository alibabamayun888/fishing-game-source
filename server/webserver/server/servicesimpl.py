#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import sys
import traceback
from datetime import datetime
from datetime import timedelta
import time
import const
import errorcode
import json
import logging
import conf.webserver as djangoconf
import commonutils
from server import models
log = logging.getLogger("wxdjango")

#27001 查询公众号绑定信息
def service_27001(params, jsonData):
    code = params['code']
    uid = int(commonutils.getObjFieldVlaue(params, 'uid', 0))
    page = int(commonutils.getObjFieldVlaue(params, 'pageIndex', 1))
    pageSize = int(commonutils.getObjFieldVlaue(params, 'pageSize', 10))
    startDate = commonutils.getObjFieldVlaue(params, 'startDate')
    endDate = commonutils.getObjFieldVlaue(params, 'endDate')
    phone = str(commonutils.getObjFieldVlaue(params, 'phone'))
    msg = 'servicesimpl::service_27001 uid:{}, page:{}, pageSize:{},phone:{},startDate:{},endDate:{}'.format(uid, page, pageSize, phone, startDate, endDate)
    log.info(msg)

    if(page <= 0):
      page = 1
    if(pageSize > 50):
      pageSize = 50
    
    startPos = (page-1)*pageSize
    endPos = startPos + pageSize
    totalItems = 0
    listData = []

    status = const.WX_PUBLIC_STATUS_BIND
    if uid > 0: #根据UID查询
      totalItems = models.TableWxPublicBinding.objects.all().filter(status=status, uid=uid).count()
      listData = models.TableWxPublicBinding.objects.filter(status=status, uid=uid)[startPos:endPos]

    elif len(phone) > 10: #根据手机号查询
      totalItems = models.TableWxPublicBinding.objects.all().filter(status=status, phone=phone).count()
      listData = models.TableWxPublicBinding.objects.filter(status=status, phone=phone)[startPos:endPos]

    elif len(startDate) >= 10 and len(endDate) >= 10: # 根据时间段查询 
      #startDate="2019-01-16" 
      #endDate="2019-01-17"
      startDate = datetime.strptime(startDate, "%Y-%m-%d") 
      endDate = datetime.strptime(endDate, "%Y-%m-%d") 
      dtStartStr = startDate.strftime('%Y-%m-%d %H:%M:%S')
      dtEndStr   = endDate.strftime('%Y-%m-%d %H:%M:%S')
      msg = 'servicesimpl::service_27001 uid:{}, dtStartStr:{}, dtEndStr:{}'.format(uid, dtStartStr, dtEndStr)
      log.info(msg)
      totalItems = models.TableWxPublicBinding.objects.all().filter(status=status, bind_time__range=[dtStartStr, dtEndStr]).count()
      listData = models.TableWxPublicBinding.objects.filter(status=status, bind_time__range=[dtStartStr, dtEndStr])[startPos:endPos]
    else:
      totalItems = models.TableWxPublicBinding.objects.all().filter(status=status).count()
      listData = models.TableWxPublicBinding.objects.all().filter(status=status)[startPos:endPos]

    jsonData['resultData'] = []
    for data in listData:
      item = {}
      item['uid'] = data.uid
      item['name'] = data.name
      item['openId'] = data.openid
      item['phone'] = data.phone
      item['bindTime'] = data.bind_time.strftime('%Y-%m-%d %H:%M:%S')
      item['unBindTime'] = data.un_bind_time.strftime('%Y-%m-%d %H:%M:%S') 
      item['status'] = data.status
      if data.status != const.WX_PUBLIC_STATUS_UNBIND:
        item['unBindTime'] = None
      jsonData['resultData'].append(item)

    totalPages = totalItems / pageSize
    if totalItems % pageSize != 0:
      totalPages = totalPages + 1

    jsonData['totalItems'] = totalItems
    jsonData['totalPages'] = totalPages

#27002 解除公众号绑定
def service_27002(params, jsonData):
    uid = int(commonutils.getObjFieldVlaue(params, 'uid', 0))
    openid = str(commonutils.getObjFieldVlaue(params, 'openId'))
    optUser = commonutils.getObjFieldVlaue(params, 'optUser')

    errcode = commonutils.wxPublicNoBinding(uid, openid, const.WXPUBLICBINDACTYPE_SYS_UNBIND, optUser)
    msg = 'servicesimpl::service_27002 uid:{},openid:{},errcode:{},optUser:{}'.format(uid, openid, errcode, optUser)
    log.info(msg)

    if errcode != errorcode.EC_SUCC:
      jsonData['result'] = 0  #接口状态，1：成功 0：失败
      jsonData['msg'] = commonutils.getErrorCodeMsg(errcode)




