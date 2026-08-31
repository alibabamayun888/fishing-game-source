#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json

class DataWeChatItmes:
  def __init__(self,id,name,cost_num):
    self.id = id
    self.name = name
    self.cost_num = cost_num
    pass
datawechatitmesdict = {}
datawechatitmesdict[1] = DataWeChatItmes(1,5,500)
datawechatitmesdict[2] = DataWeChatItmes(2,10,1000)
datawechatitmesdict[3] = DataWeChatItmes(3,50,5000)
datawechatitmesdict[4] = DataWeChatItmes(4,100,10000)



def get_item(id):
    return datawechatitmesdict.get(id, None)



def get_all_items():
  return datawechatitmesdict
