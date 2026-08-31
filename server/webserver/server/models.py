#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

#微信公众号支付订单表
class TableWxPublicPay(models.Model):
    # id = models.IntegerField()                #int  An id field is added automatically
    class Meta:
        db_table="tbl_wx_public_pay"
    trade_no = models.CharField(max_length=128) #varchar
    buy_info = models.CharField(max_length=4096) #varchar
    status  = models.IntegerField(default=0)    #int

#微信公众号绑定uid信息表
class TableWxPublicBinding(models.Model):
    class Meta:
        db_table="tbl_wx_public_binding"
    openid = models.CharField(max_length=64, default='')
    phone = models.CharField(max_length=32, default='')
    js_str = models.CharField(max_length=4096, default='')
    name = models.CharField(max_length=64)
    uid = models.IntegerField()
    status = models.IntegerField()
    bind_time = models.DateTimeField()
    un_bind_time = models.DateTimeField()

#微信公众号红包兑换信息表
class TableWxPublicExchangeRedPacket(models.Model):
    class Meta:
        db_table="tbl_wx_exchange_red_packet"
    openid = models.CharField(max_length=64, default='')
    phone = models.CharField(max_length=32, default='')
    order = models.CharField(max_length=128, default='')
    js_str = models.CharField(max_length=4096, default='')
    uid = models.IntegerField()
    rmb = models.IntegerField()
    status = models.IntegerField()
    exchange_time = models.DateTimeField()

#玩家信息表
class TablePlayerInfo(models.Model):
    class Meta:
        db_table="tbl_player_info"
    uid = models.IntegerField()
    openid = models.CharField(max_length=64, default='')
    phone = models.CharField(max_length=32, default='')
    js_str = models.CharField(max_length=4096, default='')