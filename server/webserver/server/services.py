#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
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
import servicesimpl
log = logging.getLogger("wxdjango")


#数据中心GM接口
@csrf_exempt
def gmserivices(request):
  jsonData = {}
  try:
    uid = 0
    code = 0
    params = {}
    time = 0

    if request.method == 'POST':
      postBody = request.body
      msg = 'services::gmserivices postBody:{}'.format(postBody)
      log.info(msg)
      postBodyObj = json.loads(postBody.decode())
      uid = commonutils.getObjFieldVlaue(postBodyObj, 'uid', 0)
      code = commonutils.getObjFieldVlaue(postBodyObj, 'code', 0)
      params = commonutils.getObjFieldVlaue(postBodyObj, 'params', '{}')
      params = json.loads(params)
    else:
      uid = int(commonutils.getRequestParam(request, 'uid', 0))
      code = commonutils.getRequestParam(request, 'code')
      time = commonutils.getRequestParam(request, 'time')

    msg = 'services::gmserivices code:{},time:{},params:{}'.format(code, time, params)
    log.info(msg)
    
    jsonData['totalItems'] = 0
    jsonData['totalPages'] = 0
    jsonData['result'] = 1
    jsonData['msg'] = ''

    if params is None:
      params = {}
      msg = 'services::gmserivices params is None'
      log.info(msg)

    if uid > 0:
      params['uid'] = uid

    #调用接口
    params['code'] = code
    function_name = 'service_' + str(code)
    getattr(servicesimpl, function_name)(params, jsonData)

  except:
    msg = traceback.format_exc()
    log.error(msg)
    jsonData['result'] = 0  #接口状态，1：成功 0：失败
    jsonData['msg'] = msg
  return HttpResponse(json.dumps(jsonData), content_type="application/json,charset=utf-8")

