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
#sys.path.append("../../../")
#sys.path.append("../../")
#from webserver import webserver
#import webserver
#from main import WebServer

from PlatformService import *
import PlatformService
#import ttypes
from ttypes import *
import wxbuyitem
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
# from thrift.protocol import *
from thrift.protocol import TBinaryProtocol
import json
import logging
logger = logging.getLogger("django")
#logger.info("some info")
import commonutils
import conf.webserver as djangoconf
defaultPlatformIp = djangoconf.DEFAULT_THRIFT_IP #default platform的thrift接口
defaultPlatformPort = djangoconf.DEFAULT_THRIFT_PORT
from datetime import datetime

# 默认主页
@csrf_exempt
def defaultIndex(request):
    response = HttpResponse("ok")
    return response


# 404
@csrf_exempt
def page404(request, **kwargs):
    dtNow = datetime.now()
    strTime = dtNow.strftime('%Y-%m-%d %H:%M:%S')
    tip = 'hi boy 404 curtime:{}'.format(strTime)
    response = HttpResponse(tip)
    return response    

# 500
@csrf_exempt
def page500(request, **kwargs):
    dtNow = datetime.now()
    strTime = dtNow.strftime('%Y-%m-%d %H:%M:%S')
    tip = 'hi boy 500 curtime:{}'.format(strTime)
    response = HttpResponse(tip)
    return response  

# SDK兑换结果
@csrf_exempt
def exchangeItem(request):
  try:
    if request.method == 'GET':
      logger.info("exchangeItem callback:...GET... path=%s",sys.path[0])
      response = HttpResponse("not ok")
      return response
    elif request.method == 'POST':
      for k, v in request.POST.items():
        logger.info("exchangeItem:%s:%s", k, v)
      jsonDict = {}
#      jsonDict["orderType"] = request.POST.get("orderType", "")
#      jsonDict["gameSn"] = request.POST.get("gameSn", "")
#      jsonDict["orderSn"] = request.POST.get("orderSn", "")
#      jsonDict["sdkUid"] = request.POST.get("sdkUid", "")
#      jsonDict["roleId"] = request.POST.get("roleId", "")
#      jsonDict["goodsValue"] = request.POST.get("goodsValue", "")
#      jsonDict["gameType"] = request.POST.get("gameType", "")
#      jsonDict["extraInfo"] = request.POST.get("extraInfo", "")
#      jsonDict["orderInfo"] = request.POST.get("orderInfo", "")
#      jsonDict["timespan"] = request.POST.get("timespan", "")
      jsonDict["data"] = request.POST.get("data", "")
      jsonDict["sign"] = request.POST.get("sign", "")
      strJson = json.dumps(jsonDict)
      logger.info("exchangeItem:%s", strJson)
      transport = TSocket.TSocket(defaultPlatformIp, defaultPlatformPort)
      transport = TTransport.TFramedTransport(transport)
      protocol = TBinaryProtocol.TBinaryProtocol(transport)
      client = PlatformService.Client(protocol)
      transport.open()
      res = client.exchangeItem(strJson)
      transport.close()

      if res != 0:
        response = HttpResponse("not ok")
        return response

      response = HttpResponse("ok")
      return response
  except:
    traceback.print_exc()
    logger.error("exchangeItem:except", exc_info = True)
    response = HttpResponse("not ok")
    return response


#SDK平台传过来的支付回调处理
@csrf_exempt
def paycallback(request):
  if request.method == 'GET':
      logger.info("paycallback:...GET... path=%s",sys.path[0])
      #return render(request , 'paycallback.html')
      return "ok"
  elif request.method == 'POST':
    logger.info("paycallback:...post... ")

    #"extraInfo":"player_id=1129593,server_id=0,rechargeId=101"
    strJson = ""
    accId = "0"
    userId = 0
    strExtraInfo = ""
    if request.POST.has_key("amount"):
      logger.info("has_key amount:%s, is ios" , request.POST["amount"])
      jsonDict = {}
      jsonDict["amount"] = request.POST.get("amount",0.0)
      jsonDict["tradeNo"] = request.POST.get("tradeNo","")
      #jsonDict["userId"] = request.POST.get("userId",0)
      accId = request.POST.get("userId","0")
      if accId == "0":
        accId = request.POST.get("uid","0")
      jsonDict["userId"] = accId
      jsonDict["orderNo"] = request.POST.get("orderNo","0")
      jsonDict["extraInfo"] = request.POST.get("extraInfo","")
      strExtraInfo = request.POST.get("extraInfo","")
      jsonDict["sign"] = request.POST.get("sign","")
      #userId = request.POST.get("userId",0)
      strJson = json.dumps(jsonDict)
      
    else:
      logger.info("not has_key android, json:%s" , request.body)
      strJson = request.body
      rechangeJS = json.loads(strJson)
      #accId = rechangeJS.get("userId")
      strExtraInfo = rechangeJS.get("extraInfo")

    strExtraInfoVec = strExtraInfo.split(',')
    if len(strExtraInfoVec) >= 3:
      playerInfoVec = strExtraInfoVec[0].split('=')
      if len(playerInfoVec) == 2:
          userId = playerInfoVec[1]
          userId = int(userId)

    logger.info("strJson = [%s] POST:%s, request:%s , userId:%d" , strJson,request.POST,request,userId)
    """
    transport = TSocket.TSocket('192.168.60.31',6710)
    #transport = TTransport.TBufferedTransport(transport)
    transport = TTransport.TFramedTransport(transport)
    #protocol = TBinaryProtocol.TBinaryProtocol(transport)
    protocol = TCompactProtocol.TCompactProtocol(transport)
    client = PlatformService.Client(protocol)
    transport.open()
    """
    #先通过默认的platform的接口获得用户id所在的platform的thrift ip和端口，解决多个platform的问题
    # Make socket     
    transport = TSocket.TSocket(defaultPlatformIp, defaultPlatformPort) #default platform的thrift接口
    # Buffering is critical. Raw sockets are very slow    
    transport = TTransport.TFramedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)   
    # Create a client to use the protocol encoder    
    client = PlatformService.Client(protocol)
    # Connect!    
    transport.open()    
    # Call Server services  
    logger.info("getPlatFormThriftByUid before userId = [%d] " , userId)
    retData = client.getPlatFormThriftByUid(userId)
    logger.info("getPlatFormThriftByUid retData = [%s] " , retData)
    transport.close()
    
    #获得uid所在的platform的thrift接口
    thriftIp = defaultPlatformIp
    thriftPort = defaultPlatformPort
    retDataJson = json.loads(retData)
    keyIp = "ip"
    keyPort = "port"
    if (keyIp in retDataJson) :
        thriftIp = retDataJson[keyIp]
    if (keyPort in retDataJson):
        thriftPort = retDataJson[keyPort]
        
    logger.info("payCallBack thriftIp:%s, thriftPort = %d " , thriftIp,thriftPort)
    transport = TSocket.TSocket(thriftIp, thriftPort) 
    transport = TTransport.TFramedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)   
    client = PlatformService.Client(protocol)
    transport.open()    
    res = client.payCallBack(strJson) 
    logger.info("payCallBack res:%d " , res)
    #res = client.upgradeCannonLv(1, "123", 1)
    if res != 0:
        logger.error("paycallback:client.paycallback  error, res:%d",res)
        transport.close()
        response = HttpResponse("not ok")
        return response
    transport.close()
    #return render(request , "paycallback.html" , {'string':404})
    response = HttpResponse("ok")
    return response
  
#后台发送邮件
@csrf_exempt
def sendmail(request):
  if request.method == 'GET':
      logger.info("paycallback:...GET... path=%s",sys.path[0])
      #return render(request , 'paycallback.html')
      return "ok"
  elif request.method == 'POST':
    logger.info("paycallback:...post... ")

    #{"confid": "100009","exceptchannel": "wx|pc","fromid": "0","toid": "123456","title": "补偿","content": "给你补偿，查收附件。","attach": [{"itemid": "10010001","itemnum": "100"}, {"itemid": "10010002","itemnum": "100"}]}
    strJson = ""
    userId = "0"
    if request.POST.has_key("amount"):
      logger.info("has_key amount:%s, is ios" , request.POST["amount"])
      jsonDict = {}
      userId = request.POST.get("toid","0")
      jsonDict["userId"] = userId
      strJson = json.dumps(jsonDict)
      
    else:
      logger.info("not has_key android, json:%s" , request.body)
      strJson = request.body
      rechangeJS = json.loads(strJson)
      #accId = rechangeJS.get("userId")
      #strExtraInfo = rechangeJS.get("extraInfo")
      userId = rechangeJS.get("toid")

    
    logger.info("strJson = [%s] POST:%s" , strJson,request.POST)
          
    logger.info("sendmail thriftIp:%s, thriftPort = %d " , defaultPlatformIp,defaultPlatformPort)
    transport = TSocket.TSocket(defaultPlatformIp, defaultPlatformPort) 
    transport = TTransport.TFramedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)   
    client = PlatformService.Client(protocol)
    transport.open()    
    res = client.sendMail(strJson) 
    logger.info("sendmail res:%d " , res)
    #res = client.upgradeCannonLv(1, "123", 1)
    if res != 0:
        logger.error("sendmail:client.sendmail  error, res:%d",res)
        transport.close()
        response = HttpResponse("not ok")
        return response
    transport.close()
    #return render(request , "paycallback.html" , {'string':404})
    response = HttpResponse("ok")
    return response

#商城下订单
@csrf_exempt
def newShopOrder(request):
    try:
      uid = 0
      shopId = 0
      rmbFen = 0
      if request.method == 'GET':
        uid = request.GET.get("uid")
        shopId = request.GET.get("shopId")
        rmbFen = request.GET.get("rmbFen")
      else:
        uid = request.POST.get("uid")
        shopId = request.POST.get("shopId")
        rmbFen = request.POST.get("rmbFen")

      jsonStr = commonutils.newShopOrder(uid, shopId, rmbFen)
      # return HttpResponse(json.dumps(jsonData, ensure_ascii=False), content_type="application/json,charset=utf-8")
      return HttpResponse(jsonStr, content_type="application/json,charset=utf-8")
    except:
      msg = traceback.format_exc()
      logger.error("newShopOrder except:%s", msg)

#获取商城配置
@csrf_exempt
def getShopConfig(request):
    try:
      serverType = 0
      if request.method == 'GET':
        serverType = request.GET.get("serverType")
      else:
        serverType = request.POST.get("serverType")

      retData = commonutils.getShopConfig(serverType)
      return HttpResponse(retData, content_type="application/json,charset=utf-8")
    except:
      msg = traceback.format_exc()
      logger.error("getShopConfig except:%s", msg)

#获取玩家信息
@csrf_exempt
def getPlayerInfo(request):
    try:
      uid = 0
      if request.method == 'GET':
        uid = request.GET.get("uid")
      else:
        uid = request.POST.get("uid")

      retData = commonutils.getPlayerInfo(uid)
      jsonData = json.loads(retData)
      jsonData['sdkAppid'] = djangoconf.WXPUBLIC_SDK_APPID
      jsonData['sdkSource'] = djangoconf.WXPUBLIC_SDK_SOURCE

      return HttpResponse(json.dumps(jsonData), content_type="application/json,charset=utf-8")
    except:
      msg = traceback.format_exc()
      logger.error("getPlayerInfo except:%s", msg)  

#获取微信公众号充值物品列表
@csrf_exempt
def getWxPulicItems(request):
  try:
      retData = commonutils.getShopConfig(2)
      # logger.info("getWxPulicItems retData:%s", retData)
      retJson = json.loads(retData)
      data = retJson['data']

      jsonData = []
      for item in retJson['data']:
          data = {}

          cost_type = int(item['cost_type'])
          if cost_type != 3: #消耗类型，3是人民币
                continue

          gainRes = commonutils.getItemFromStr(item['gain_res'])
          normalGive = commonutils.getItemFromStr(item['normal_give'])            #基础赠送
          firstGainRes = commonutils.getItemFromStr(item['first_gain_res'])       #首冲额外获得
          otherGainRes = commonutils.getItemFromStr(item['other_gain_res'])       #非首冲额外赠送
          firstDiamondRes = commonutils.getItemFromStr(item['first_diamond_res']) #首冲额外获得钻石

          ntype = int(item['type'])
          itemId = 0
          itemNum = 0
          if ntype == 1: # 金币
              itemId = normalGive['itemId']
              itemNum = normalGive['itemNum']
          elif ntype == 3: #钻石
              itemId = gainRes['itemId']
              itemNum = gainRes['itemNum']
          elif ntype == 4: #月卡
              itemId = gainRes['itemId']
              itemNum = gainRes['itemNum']
          else:
              continue

          data['costNum'] = item['cost_num']
          # data['name'] = item['name']
          data['shopId'] = item['shop_id']
          data['itemType'] = ntype
          data['itemId'] =  itemId
          data['itemNum'] = itemNum

          '''
          data['normalGiveItemId'] =  normalGive['itemId']
          data['normalGiveItemNum'] = normalGive['itemNum']
          data['firstGainItemId'] =  firstGainRes['itemId']
          data['firstGainItemNum'] = firstGainRes['itemNum']
          data['otherGainResItemId'] =  otherGainRes['itemId']
          data['otherGainResItemNum'] = otherGainRes['itemNum']
          data['firstDiamondResItemId'] =  firstDiamondRes['itemId']
          data['firstDiamondResItemNum'] = firstDiamondRes['itemNum']
          '''

          jsonData.append(data)

      return HttpResponse(json.dumps(jsonData), content_type="application/json,charset=utf-8")
  except:
      msg = traceback.format_exc()
      logger.error("getWxPulicItems except:%s", msg)  