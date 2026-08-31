#!/usr/bin/env python
# -*- coding: utf-8 -*-
#视图函数
# Create your views here
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings 
import sys
import traceback
from datetime import datetime
from datetime import timedelta
import time
import PlatformService
import wxbuyitem
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
import json
import commonutils
import logging
log = logging.getLogger("wxdjango")
import wxpay
from models import TableWxPublicPay
from models import TableWxPublicBinding
from models import TableWxPublicExchangeRedPacket
from models import TablePlayerInfo
import conf.webserver as djangoconf
import const
import errorcode
import datawechatitmes

@csrf_exempt
def wxPay(request):
  template = {}
  template['uid'] = ''
  if request.session.has_key('uid'):
     template['uid'] = request.session['uid']

  return render(request , 'wxpay.html', template)

@csrf_exempt
def wxBuyItem(request):
    if request.method == 'GET':
      return HttpResponse("wxBuyItem...")
    try:
      log.info('wxBuyItem...')
      buyInfo = {}
      jsonData = json.loads(request.body)
      uid = int(jsonData['uid'])
      gamePass = jsonData['gamePass']
      request.session['uid'] = uid

      id = int(jsonData['id'])
      buyItem = wxbuyitem.wxBuyItem[id]

      buyInfo['uid'] = uid
      buyInfo['id'] = id
      buyInfo['money'] = buyItem['money']
      buyInfo['itemId'] = buyItem['itemId']
      buyInfo['itemNum'] = buyItem['itemNum']
      buyInfo['time'] = datetime.now().strftime('%Y%m%d %H:%M:%S')

      openid = jsonData['openid']
      if len(openid) < 10 and request.session.has_key('openid'):
        openid = request.session['openid']

      notify_url = request.scheme + '://' + request.get_host() + '/onWxpay/'
      total_fee = int(buyItem['money']*100)  #订单金额，单位分
      # total_fee = 1
      buyInfo['total_fee'] = total_fee

      dtNow = datetime.now()
      trade_no = '' # 商户系统内部订单号，要求32个字符内，只能是数字、大小写字母_-|* 且在同一个商户号下唯一
      trade_no = "{}_{}".format(uid, dtNow.strftime('%Y%m%d%H%M%S%f'))
      buyInfo['trade_no'] = trade_no

      log.info('uid:' + str(uid))
      log.info('id:' + str(id))
      log.info('trade_no:' + trade_no)
      log.info('total_fee:' + str(total_fee))
      log.info('openid:' + str(openid))
      log.info('notify_url:' + notify_url)

      
      wxPayHelper = wxpay.WxPayHelper()
      orderData = wxPayHelper.getUnifiedorderData(openid, notify_url, total_fee, trade_no)
      log.info('orderData:')
      log.info(orderData)

      #向腾讯下订单
      postUrl = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
      postRetData = commonutils.httpsPost(postUrl, orderData)
      log.info('postRetData:')
      log.info(postRetData)

      xmlObj = wxPayHelper.xmlToArray(postRetData)
      jsParam = {}
      jsParam['appId'] = xmlObj['appid']
      jsParam['timeStamp'] = int(time.time())
      jsParam['nonceStr'] = xmlObj['nonce_str']
      jsParam['package'] = 'prepay_id=' + xmlObj['prepay_id']
      jsParam['signType'] = 'MD5'
      jsParam['paySign'] = wxPayHelper.getSign(jsParam)
      jsParam['error'] = 0

      #订单信息入库
      tbWxPublicPay = TableWxPublicPay.objects.create()
      tbWxPublicPay.trade_no = trade_no
      tbWxPublicPay.buy_info = json.dumps(buyInfo)
      tbWxPublicPay.status = djangoconf.WXPUBLIC_ORDER_STATUS_NO_PROCESS
      tbWxPublicPay.save()

      return HttpResponse(json.dumps(jsParam), content_type="application/json")
    except:
      ret = {}
      ret['error'] = 1
      ret['msg'] = traceback.format_exc()
      log.error(ret['msg'])
      return HttpResponse(json.dumps(ret), content_type="application/json")

#微信公众号充值成功回调
#https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_7&index=8
@csrf_exempt
def onWxpay(request):
    try:
      log.info("onWxpay...")
      log.info(request.get_full_path())
      wxPayHelper = wxpay.WxPayHelper()
      if(request.method == 'POST'):
          log.info(request.body)
          xmlObj = wxPayHelper.xmlToArray(request.body)
          out_trade_no = xmlObj['out_trade_no']
          cash_fee = xmlObj['cash_fee']
          total_fee = xmlObj['total_fee']
          transaction_id = xmlObj['transaction_id']
          time_end = xmlObj['time_end']
          log.info('out_trade_no:' + str(out_trade_no)) #商户订单号
          log.info('cash_fee:' + str(cash_fee))
          log.info('total_fee:' + str(total_fee))
          log.info('transaction_id:' + str(transaction_id)) #微信支付订单号
          log.info('time_end:' + str(time_end)) #支付完成时间

          tbWxPublicPay = TableWxPublicPay.objects.get(trade_no=out_trade_no, status=djangoconf.WXPUBLIC_ORDER_STATUS_NO_PROCESS)
          buyInfo = json.loads(tbWxPublicPay.buyInfo)
          jsonData = {}
          uid = int(buyInfo['uid'])
          jsonData['uid'] = buyInfo['uid']
          jsonData['itemId'] = buyInfo['itemId']
          jsonData['itemNum'] = buyInfo['itemNum']
          log.info('uid:' + str(uid)) #支付完成时间

          if commonutils.rechargeCallBack(uid, 1, jsonData):
            tbWxPublicPay.status = djangoconf.WXPUBLIC_ORDER_STATUS_HAD_PROCESS
            tbWxPublicPay.save()
            log.info('onWxpay process order finish...')
          else:
            log.info('onWxpay process order failed...')

      retData = {}
      retData['return_code'] = 'SUCCESS'
      retData['return_msg'] = 'OK'
      retData = wxPayHelper.arrayToXml(retData)
      return HttpResponse(retData)
    except:
      msg = traceback.format_exc()
      log.error(msg)


@csrf_exempt
def getPlayerInfo(request):
  if request.method == 'GET':
      return HttpResponse("getPlayerInfo...")
  try:
    jsonData = json.loads(request.body)
    uid = int(jsonData['gameId'])
    # gamePass = jsonData['gamePass']
    jsonData = {}

    log.info("getPlayerInfo thriftIp:%s, thriftPort = %d " , settings.DEFAULT_THRIFT_IP, settings.DEFAULT_THRIFT_PORT)
    transport = TSocket.TSocket(settings.DEFAULT_THRIFT_IP, settings.DEFAULT_THRIFT_PORT) 
    transport = TTransport.TFramedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)   
    client = PlatformService.Client(protocol)
    transport.open()    
    jsonStr = client.gmGetPlayerInfo(uid) 
    transport.close()
    
    jsonData = json.loads(jsonStr)
    jsonData['error'] = 0
    return HttpResponse(json.dumps(jsonData), content_type="application/json")
  except:
    ret = {}
    ret['error'] = 1
    ret['msg'] = traceback.format_exc()
    log.error(ret['msg'])
    return HttpResponse(json.dumps(ret), content_type="application/json")

@csrf_exempt
def wxcodeback(request):
    log.info("wxcodeback...")
    code = request.GET.get('code')
    if code is None:
       code= 'None'
    log.info("code:" + code)

    wxPayHelper = wxpay.WxPayHelper()
    openUrl = wxPayHelper.getOpenidUrl(code)
    log.info(openUrl)

    body = commonutils.getHttps(openUrl)
    log.info(body)

    openid = 0
    jsonData = json.loads(body)
    if jsonData.has_key('openid'):
      openid = jsonData['openid']

    request.session['openid'] = openid
    redirectUrl = request.scheme + '://' + request.get_host() + '/wxPay/?openid=' + str(openid)
    return HttpResponseRedirect(redirectUrl)
    # return HttpResponse("wxcodeback...openid: " + str(openid) + ' ' + body)

@csrf_exempt
def getwxcode(request):
    log.info('getwxcode...')
    #redirectUrl不能包含端口号
    #必须把端口号去掉
    redirectUrl = request.scheme + '://' + request.get_host() + '/wxcodeback'
    # redirectUrl = 'http://test-pay.fish.mb1768.cn:12195/wxcodeback'
    pos = redirectUrl.rfind(':')
    if pos > 0:
        redirectUrl = redirectUrl[0:pos] + '/wxcodeback'

    log.info('redirectUrl=' + redirectUrl)
    wxPayHelper = wxpay.WxPayHelper()
    redirectUrl = wxPayHelper.getCodeUrl(redirectUrl)
    log.info('redirectUrl=' + redirectUrl)
    return HttpResponseRedirect(redirectUrl)
    # return HttpResponse("getwxcode..." + redirectUrl)


@csrf_exempt
def wxpaysuccess(request):
  return render(request , 'wxpaysuccess.html')

#获取公众号游戏绑定信息
@csrf_exempt
def getWxPublicBinding(request):
  jsonData = {}
  jsonData['errcode'] = 0
  try:
    openid = commonutils.getRequestParam(request, 'openid', 0)
    log.info('getWxPublicBinding openid=' + str(openid))

    jsonData['jsonData'] = 0
    jsonData['limit'] = djangoconf.WXPUBLIC_BINDING_LIMIT
    jsonData['data'] = []
    # jsonData['data'].append({'uid':111, 'name':'test', 'bindingDt': '2018-01-01 11:11:11'})

    request.session['openid'] = openid

    #openid是否曾经被绑定过，获得绑定的第一个uid
    firstUid = 0
    firstData = TableWxPublicBinding.objects.filter(openid=openid).order_by("id").first()
    if firstData:
        firstUid = firstData.uid
    listData = TableWxPublicBinding.objects.filter(openid=openid,status=const.WX_PUBLIC_STATUS_BIND)
    for data in listData:
      item = {}
      uid = data.uid
      playerInfo = json.loads(commonutils.getPlayerInfo(uid))

      item['uid'] = uid
      item['name'] = data.name
      if playerInfo:
        item['name'] = playerInfo['nick']
      item['bindingDt'] = data.bind_time.strftime("%Y-%m-%d %H:%M:%S")
      item['isNew'] = 0
      if uid == firstUid:
        item['isNew'] = 1
      jsonData['data'].append(item)

  except:
    err = traceback.format_exc()
    log.error(err)
    errcode =  errorcode.EC_UNKOWN_ERR
    jsonData['errcode'] = errcode
    jsonData['msg'] = commonutils.getErrorCodeMsg(errcode)
  return HttpResponse(json.dumps(jsonData), content_type="application/json,charset=utf-8")
  
#公众号绑定游戏
@csrf_exempt
def wxPublicBinding(request):
  jsonData = {}
  jsonData['errcode'] = errorcode.EC_SUCC
  try:
    openid = commonutils.getRequestParam(request, 'openid')
    uid    = commonutils.getRequestParam(request, 'uid', 0)
    phone  = commonutils.getRequestParam(request, 'phone')
    vcode  = commonutils.getRequestParam(request, 'vcode')    #短信验证码
    key    = commonutils.getRequestParam(request, 'key')      #绑定口令
    uid    = int(uid)
    msg = 'wxviews::wxPublicBinding openid:{}, uid:{}, phone:{}, vcode:{}, key:{}'.format(openid, uid, phone, vcode, key)
    log.info(msg)

    #是否已经达到绑定上限
    listData = TableWxPublicBinding.objects.filter(openid=openid,status=const.WX_PUBLIC_STATUS_BIND)
    if len(listData) >= djangoconf.WXPUBLIC_BINDING_LIMIT:
      errcode = errorcode.EC_BINDING_NUM_LIMIT
      jsonData['errcode'] = errcode
      jsonData['msg'] = commonutils.getErrorCodeMsg(errcode)
      return HttpResponse(json.dumps(jsonData), content_type="application/json,charset=utf-8")

    #是否已经绑定过了
    # listData = TableWxPublicBinding.objects.filter(openid=openid, uid=uid, status=const.WX_PUBLIC_STATUS_BIND)
    listData = TableWxPublicBinding.objects.filter(uid=uid, status=const.WX_PUBLIC_STATUS_BIND)
    if len(listData) >= 1:
      if listData[0].openid == openid:
        msg = 'wxviews::wxPublicBinding openid:{}, uid:{} had bind...'.format(openid, uid)
        log.error(msg)
        errcode = errorcode.EC_HAD_BINDING
        jsonData['errcode'] = errcode
        jsonData['msg'] = commonutils.getErrorCodeMsg(errcode)
        return HttpResponse(json.dumps(jsonData), content_type="application/json,charset=utf-8")

    #这个openid是否曾被绑定过
    isBind = 0
    openidData = TableWxPublicBinding.objects.filter(openid=openid)
    if len(openidData) > 0:
        isBind = 1

    jsStr = commonutils.wxPublicBinding(uid, openid, phone, vcode, key)
    msg = 'wxviews::wxPublicBinding jsStr:{}'.format(jsStr)
    log.info(msg)

    jsObj = json.loads(jsStr)
    if jsObj['errcode'] == errorcode.EC_SUCC:
      # wxPublicBinding = TableWxPublicBinding.objects.get(openid=openid, uid=uid) # get方法 记录不存在、记录超过一行时，会抛异常
      # wxPublicBinding = TableWxPublicBinding.objects.filter(openid=openid, uid=uid).first()
      wxPublicBinding = TableWxPublicBinding.objects.filter(uid=uid).first()
      if not wxPublicBinding:
        wxPublicBinding = TableWxPublicBinding()
      wxPublicBinding.openid = openid
      wxPublicBinding.phone = phone
      wxPublicBinding.uid = uid
      wxPublicBinding.status = const.WX_PUBLIC_STATUS_BIND
      wxPublicBinding.bind_time = datetime.now()
      wxPublicBinding.un_bind_time = datetime.now() #因为不能为空，所以给个值
      wxPublicBinding.name = jsObj['name']
      wxPublicBinding.save()

      #更新玩家信息
      playerInfo = TablePlayerInfo.objects.filter(uid=uid).first()
      if not playerInfo:
        playerInfo = TablePlayerInfo()
      playerInfo.uid = uid
      playerInfo.openid = openid
      playerInfo.phone = phone
      playerInfo.save()

      log.info('wxviews::wxPublicBinding success uid:' + str(uid))
    else:
      log.info('wxviews::wxPublicBinding failed uid:' + str(uid))

    jsonData['errcode'] = jsObj['errcode']
    jsonData['isBind'] = isBind
  except:
    err = traceback.format_exc()
    log.error(err)
    jsonData['errcode'] = errorcode.EC_UNKOWN_ERR
  jsonData['msg'] = commonutils.getErrorCodeMsg(jsonData['errcode'])
  return HttpResponse(json.dumps(jsonData), content_type="application/json,charset=utf-8")
  

#解除公众号绑定游戏uid
@csrf_exempt
def wxPublicNoBinding(request):
  jsonData = {}
  jsonData['errcode'] = errorcode.EC_SUCC
  try:
    openid = commonutils.getRequestParam(request, 'openid')
    uid    = commonutils.getRequestParam(request, 'uid', 0)
    uid    = int(uid)
    msg = 'wxviews::wxPublicNoBinding openid:{}, uid:{}'.format(openid, uid)
    log.info(msg)

    optUser = ''
    errcode = commonutils.wxPublicNoBinding(uid, openid, const.WXPUBLICBINDACTYPE_UNBIND, optUser)
    jsonData['errcode'] = errcode
    msg = 'wxviews::wxPublicNoBinding uid:{},errcode:{}'.format(uid, errcode)
    log.info(msg)
  except:
    err = traceback.format_exc()
    log.error(err)
    jsonData['errcode'] = errorcode.EC_UNKOWN_ERR
  jsonData['msg'] = commonutils.getErrorCodeMsg(jsonData['errcode'])
  return HttpResponse(json.dumps(jsonData), content_type="application/json,charset=utf-8")
  

#发送短信验证码
@csrf_exempt
def wxPublicSendVcode(request):
  jsonData = {}
  jsonData['errcode'] = errorcode.EC_SUCC
  try:
    phone = commonutils.getRequestParam(request, 'phone')
    uid    = int(commonutils.getRequestParam(request, 'uid', 0))
    msg = 'wxviews::wxPublicSendVcode phone:{}, uid:{}'.format(phone, uid)
    log.info(msg)

    if uid <= 0:
      jsonData['errcode'] = errorcode.EC_NO_UID
      jsonData['msg'] = commonutils.getErrorCodeMsg(jsonData['errcode'])
      return HttpResponse(json.dumps(jsonData), content_type="application/json,charset=utf-8")
    
    jsStr = commonutils.sendPhoneVcode(uid, phone)
    msg = 'wxviews::wxPublicSendVcode jsStr:{}'.format(jsStr)
    log.info(msg)

    jsonObj = json.loads(jsStr)
    jsonData['errcode'] = jsonObj['errcode']
  except:
    err = traceback.format_exc()
    log.error(err)
    jsonData['errcode'] = errorcode.EC_UNKOWN_ERR
  jsonData['msg'] = commonutils.getErrorCodeMsg(jsonData['errcode'])
  return HttpResponse(json.dumps(jsonData), content_type="application/json,charset=utf-8")

#获取红包数量
@csrf_exempt
def getRedBagNum(request):
  jsonData = {}
  jsonData['errcode'] = errorcode.EC_SUCC
  try:
    uid = int(commonutils.getRequestParam(request, 'uid', 0))
    openid = commonutils.getRequestParam(request, 'openid')
    msg = 'wxviews::getRedBagNum uid:{},openid:{}'.format(uid, openid)
    log.info(msg)

    #是否已经绑定
    wxPublicBinding = TableWxPublicBinding.objects.filter(uid=uid, openid=openid).first()
    if not wxPublicBinding:
      msg = 'wxviews::getRedBagNum error not bind'
      log.info(msg)
      jsonData['errcode'] = errorcode.EC_OPENID_ERROR
      jsonData['msg'] = '找不到绑定信息'
      return HttpResponse(json.dumps(jsonData), content_type="application/json,charset=utf-8")

    # playerInfo = TablePlayerInfo.objects.get(uid=uid) # get方法 记录不存在、记录超过一行时，会抛异常
    playerInfo = TablePlayerInfo.objects.filter(uid=uid).first()
    if playerInfo:
      openid = playerInfo.openid
      log.info('wxviews::getRedBagNum playerInfo uid:{},openid:{}'.format(uid, openid))

    openid = commonutils.getSessionValue(request, 'openid', openid)
    if len(openid) < 28:
      log.info('wxviews::getRedBagNum len openid < 28 uid:{},openid:{}'.format(uid, openid))
      jsonData['errcode'] = errorcode.EC_OPENID_ERROR
      jsonData['msg'] = commonutils.getErrorCodeMsg(jsonData['errcode'])
      return HttpResponse(json.dumps(jsonData), content_type="application/json,charset=utf-8")

    log.info('wxviews::getRedBagNum uid:{}, real openid:{}'.format(uid, openid))
    dayNum = commonutils.getTodayExchangeRedPacketNum(uid, openid) #今天还可以兑换次数
    num = commonutils.getPlayerItemNum(uid, const.ITEM_RMB_RED_PACKET)
    jsonData['num'] = num
    jsonData['dayNum'] = dayNum

    msg = 'wxviews::getRedBagNum uid:{},num:{},dayNum:{}'.format(uid, num, dayNum)
    log.info(msg)
  except:
    err = traceback.format_exc()
    log.error(err)
    jsonData['errcode'] = errorcode.EC_UNKOWN_ERR
  jsonData['msg'] = commonutils.getErrorCodeMsg(jsonData['errcode'])
  return HttpResponse(json.dumps(jsonData), content_type="application/json,charset=utf-8")

#兑换红包 rmb：人民币，单位分
@csrf_exempt
def exchangeRedBag(request):
  jsonData = {}
  jsonData['errcode'] = errorcode.EC_SUCC
  try:
    uid = int(commonutils.getRequestParam(request, 'uid', 0))
    id = int(commonutils.getRequestParam(request, 'id', 0))
    openid = str(commonutils.getRequestParam(request, 'openid'))

    if not datawechatitmes.datawechatitmesdict.has_key(id):
      msg = 'wxviews::exchangeRedBag error id:{}'.format(id)
      log.info(msg)
      jsonData['errcode'] = errorcode.EC_SYS_ERR
      jsonData['msg'] = '参数错误'
      return HttpResponse(json.dumps(jsonData), content_type="application/json,charset=utf-8")

    rmb = datawechatitmes.datawechatitmesdict[id].cost_num
    msg = 'wxviews::exchangeRedBag uid:{},id:{},rmb:{},openid:{}'.format(uid, id, rmb, openid)
    log.info(msg)
    dtNow = datetime.now()

    #兑换间隔至少2秒钟
    nowDt = int(time.time())
    lastOrderDt = commonutils.getSessionValue(request, 'lastOrderDt', 0)
    if nowDt - lastOrderDt <= 2:
      msg = 'wxviews::exchangeRedBag do order too fast...'
      log.info(msg)
      jsonData['errcode'] = errorcode.EC_OP_TOO_FAST
      jsonData['msg'] = commonutils.getErrorCodeMsg(jsonData['errcode'])
      return HttpResponse(json.dumps(jsonData), content_type="application/json,charset=utf-8")
    request.session['lastOrderDt'] = nowDt

    #是否已经绑定
    wxPublicBinding = TableWxPublicBinding.objects.filter(uid=uid, openid=openid).first()
    if not wxPublicBinding:
      msg = 'wxviews::exchangeRedBag error openid'
      log.info(msg)
      jsonData['errcode'] = errorcode.EC_OPENID_ERROR
      jsonData['msg'] = commonutils.getErrorCodeMsg(jsonData['errcode'])
      return HttpResponse(json.dumps(jsonData), content_type="application/json,charset=utf-8")

    #清理旧的兑换记录
    dtOld = datetime(dtNow.year, dtNow.month, dtNow.day, 0, 0, 0) + timedelta(days=-90)
    msg = 'wxviews::exchangeRedBag dtOld:{}'.format(dtOld.strftime('%Y-%m-%d %H:%M:%S'))
    log.info(msg)
    listData = TableWxPublicExchangeRedPacket.objects.filter(openid=openid, exchange_time__lt=dtOld)
    for row in listData:
      row.delete()

    #今天还可以兑换次数
    dayNum = commonutils.getTodayExchangeRedPacketNum(uid, openid)
    msg = 'wxviews::exchangeRedBag dayNum:{}'.format(dayNum)
    log.info(msg)
    if dayNum <= 0:
      jsonData['errcode'] = errorcode.EC_DAY_EXCHANGE_NUM_LIMIT
      jsonData['msg'] = commonutils.getErrorCodeMsg(jsonData['errcode'])
      return HttpResponse(json.dumps(jsonData), content_type="application/json,charset=utf-8")

    #红包数量是否够用
    redNum = commonutils.getPlayerItemNum(uid, const.ITEM_RMB_RED_PACKET)
    if redNum < rmb:
      log.info('wxviews::exchangeRedBag uid:{},redNum:{} < rmb:{}'.format(uid, redNum, rmb))
      jsonData['errcode'] = errorcode.EC_NO_ENOUGH_RED_PACKET
      jsonData['msg'] = commonutils.getErrorCodeMsg(jsonData['errcode'])
      return HttpResponse(json.dumps(jsonData), content_type="application/json,charset=utf-8")

    # phone = '12345678901'
    phone = commonutils.getPlayerPhone(uid)
    
    orderObj = commonutils.makeSdkRedpackOrder(uid, phone, rmb)
    if not orderObj['ok']:
      jsonData['errcode'] = errorcode.EC_DAY_EXCHANGE_NUM_LIMIT
      jsonData['msg'] = 'SDK下订单失败'
      return HttpResponse(json.dumps(jsonData), content_type="application/json,charset=utf-8")

    jsStr = commonutils.exchangeRedBag(uid, rmb)
    msg = 'wxviews::exchangeRedBag jsStr:{}'.format(jsStr)
    log.info(msg)

    jsObj = json.loads(jsStr)
    if jsObj['errcode'] == errorcode.EC_SUCC:
      order = orderObj['order']
      jsonData['order'] = order
      wxPublicExchangeRedPacket = TableWxPublicExchangeRedPacket()
      wxPublicExchangeRedPacket.openid = openid
      wxPublicExchangeRedPacket.uid = uid
      wxPublicExchangeRedPacket.rmb = rmb
      wxPublicExchangeRedPacket.order = order
      wxPublicExchangeRedPacket.status = const.WX_RED_PACKET_EXCHANGE_STATUS_WAIT
      wxPublicExchangeRedPacket.exchange_time = datetime.now()
      wxPublicExchangeRedPacket.save()
      msg = 'wxviews::exchangeRedBag success uid:{},rmb:{},openid:{}'.format(uid, rmb, openid)
      log.info(msg)

    jsonData['uid'] = uid
    # jsonData['errcode'] = jsObj['errcode']
  except:
    err = traceback.format_exc()
    log.error(err)
    jsonData['errcode'] = errorcode.EC_UNKOWN_ERR
  jsonData['msg'] = commonutils.getErrorCodeMsg(jsonData['errcode'])
  return HttpResponse(json.dumps(jsonData), content_type="application/json,charset=utf-8")

#获取红包兑换记录
@csrf_exempt
def getExchangeRedBagInfo(request):
  jsonData = {}
  jsonData['errcode'] = errorcode.EC_SUCC
  try:
    openid = commonutils.getRequestParam(request, 'openid')
    uid    = int(commonutils.getRequestParam(request, 'uid', 0))
    msg = 'wxviews::getExchangeRedBagInfo openid:{}, uid:{}'.format(openid, uid)
    log.info(msg)
    
    jsonData['data'] = []
    # jsonData['data'].append({'exchangeTime':'9999-11-11 11:11:11', 'rmb':888, 'status': const.WX_RED_PACKET_EXCHANGE_STATUS_WAIT})
    listData = TableWxPublicExchangeRedPacket.objects.filter(openid=openid, uid=uid).order_by('-exchange_time')[0:30]
    for row in listData:
      item = {}
      item['exchangeTime'] = row.exchange_time.strftime('%Y-%m-%d %H:%M:%S')
      item['status'] = row.status
      item['rmb'] = row.rmb
      jsonData['data'].append(item)

    # jsStr = commonutils.getExchangeRedBagInfo(uid, openid)
    # msg = 'wxviews::getExchangeRedBagInfo jsStr:{}'.format(jsStr)
    # log.info(msg)

  except:
    err = traceback.format_exc()
    log.error(err)
    jsonData['errcode'] = errorcode.EC_UNKOWN_ERR
  jsonData['msg'] = commonutils.getErrorCodeMsg(jsonData['errcode'])
  return HttpResponse(json.dumps(jsonData), content_type="application/json,charset=utf-8")

#获取红包兑换配置列表
@csrf_exempt
def getExchangeRedBagConfig(request):
  jsonData = {}
  jsonData['errcode'] = errorcode.EC_SUCC
  try:
    jsonData['limit'] = djangoconf.WXPUBLIC_EXCHANGE_DAY_LIMIT
    jsonData['data'] = []
    for id, obj in datawechatitmes.datawechatitmesdict.items():
      item = {}
      item['id'] = obj.id
      item['name'] = obj.name
      item['cost'] = obj.cost_num
      jsonData['data'].append(item)

  except:
    err = traceback.format_exc()
    log.error(err)
    jsonData['errcode'] = errorcode.EC_UNKOWN_ERR
  jsonData['msg'] = commonutils.getErrorCodeMsg(jsonData['errcode'])
  return HttpResponse(json.dumps(jsonData), content_type="application/json,charset=utf-8")

#查询公众号绑定信息
@csrf_exempt
def selWxPublicBinding(request):
  jsonData = {}
  jsonData['errcode'] = errorcode.EC_SUCC
  try:
    uid = int(commonutils.getRequestParam(request, 'uid', 0))
    page = int(commonutils.getRequestParam(request, 'page', 1))
    pageSize = int(commonutils.getRequestParam(request, 'pageSize', 10))
    msg = 'wxviews::selWxPublicBinding uid:{}, page:{}, pageSize:{}'.format(uid, page, pageSize)
    log.info(msg)

    if(page <= 0):
      page = 1
    if(pageSize > 100):
      pageSize = 100
    
    startPos = (page-1)*pageSize
    endPos = startPos + pageSize

    totalItems = 0
    listData = []
    if uid > 0:
      totalItems = TableWxPublicBinding.objects.all().filter(uid=uid).count()
      listData = TableWxPublicBinding.objects.filter(uid=uid)
    else:
      totalItems = TableWxPublicBinding.objects.count()
      listData = TableWxPublicBinding.objects.all()[startPos:endPos]
    
    jsonData['data'] = []
    jsonData['totalItems'] = totalItems
    
    for data in listData:
      item = {}
      item['uid'] = data.uid
      item['name'] = data.name
      item['openid'] = data.openid
      item['phone'] = data.phone
      item['bind_time'] = data.bind_time.strftime('%Y-%m-%d %H:%M:%S')
      jsonData['data'].append(item)

  except:
    err = traceback.format_exc()
    log.error(err)
    jsonData['errcode'] = errorcode.EC_UNKOWN_ERR
  jsonData['msg'] = commonutils.getErrorCodeMsg(jsonData['errcode'])
  return HttpResponse(json.dumps(jsonData), content_type="application/json,charset=utf-8")

#微信公众号红包检查接口
@csrf_exempt
def wxPublicRedpackCheckOrder(request):
  try:
    msg = 'wxviews::wxPublicRedpackCheckOrder...method:{}'.format(request.method)
    log.info(msg)
    mobile = commonutils.getRequestParam(request, 'mobile')
    billNo = commonutils.getRequestParam(request, 'billNo')
    money = commonutils.getRequestParam(request, 'money')
    orderDate = commonutils.getRequestParam(request, 'orderDate')
    timespan = int(commonutils.getRequestParam(request, 'timespan', 0))
    extraInfo = commonutils.getRequestParam(request, 'extraInfo')
    sign = commonutils.getRequestParam(request, 'sign')

    #接到请求时的时间点和timespan不能超过5分钟
    nowTimespan = commonutils.getTimeStamp64()
    if nowTimespan - timespan > 5*60*1000:
      msg = '订单超时,已超过5分钟'
      log.info(msg)
      return HttpResponse(msg)
    
    msg = 'wxviews::wxPublicRedpackCheckOrder mobile:{}, billNo:{}, money:{}'.format(mobile, billNo, money)
    log.info(msg)
    listData = TableWxPublicExchangeRedPacket.objects.filter(order=billNo, rmb=money, status=const.WX_RED_PACKET_EXCHANGE_STATUS_WAIT)
    if len(listData) > 0:
      log.info('wxviews::wxPublicRedpackCheckOrder ok...')
      return HttpResponse('ok')
    else:
      return HttpResponse('找不到订单信息：' + str(billNo))
  except:
    err = traceback.format_exc()
    log.error(err)
    return err

#微信公众号红包支付回调接口
@csrf_exempt
def wxPublicRedpackCallback(request):
  try:
    msg = 'wxviews::wxPublicRedpackCallback...method:{}'.format(request.method)
    log.info(msg)
    mobile = commonutils.getRequestParam(request, 'mobile')
    billNo = commonutils.getRequestParam(request, 'billNo')
    money = commonutils.getRequestParam(request, 'money')
    orderDate = commonutils.getRequestParam(request, 'orderDate')
    timespan = int(commonutils.getRequestParam(request, 'timespan', 0))
    extraInfo = commonutils.getRequestParam(request, 'extraInfo')
    sign = commonutils.getRequestParam(request, 'sign')

    rowObj = TableWxPublicExchangeRedPacket.objects.get(order=billNo, rmb=money, status=const.WX_RED_PACKET_EXCHANGE_STATUS_WAIT)
    if not rowObj:
      msg = '找不到订单记录,billNo:{},money:{}'.format(billNo, money)
      log.info(msg)
      return HttpResponse(msg)
    else:
      rowObj.status = const.WX_RED_PACKET_EXCHANGE_STATUS_SUCCESS
      rowObj.save()
      msg = 'wxviews::wxPublicRedpackCallback ok mobile:{}, billNo:{}, money:{}'.format(mobile, billNo, money)
      log.info(msg)
      return HttpResponse('ok')

  except:
    err = traceback.format_exc()
    log.error(err)
    return err