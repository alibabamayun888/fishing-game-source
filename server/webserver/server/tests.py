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
import commonutils
log = logging.getLogger("system")
import models


@csrf_exempt
def testUtils(request):
    t = commonutils.getRequestParam(request, 't')
    msg = 'testUtils t:{}'.format(t)
    log.info(msg)

    if t == 'wxbind':
        jsStr = commonutils.wxPublicBinding(9137572, 'openid123', '10086', '123456', '987wxws')
        msg = 'tests::testUtils wxbind jsStr:{}'.format(jsStr)
        log.info(msg)


    dtNow = datetime.now()
    msg = 'ok {}'.format(dtNow.strftime('%Y-%m-%d %H:%M:%S'))
    response = HttpResponse(msg)
    return response
