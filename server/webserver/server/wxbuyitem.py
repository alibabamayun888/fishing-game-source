#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

wxBuyItem = {}

#金币
wxBuyItem[100] = {'money':0.01, 'itemId':10010001, 'itemNum':'1'}     #1分钱，测试用
wxBuyItem[101] = {'money':12,   'itemId':10010001, 'itemNum':'60000'}
wxBuyItem[102] = {'money':30,   'itemId':10010001, 'itemNum':'150000'}
wxBuyItem[103] = {'money':98,   'itemId':10010001, 'itemNum':'490000'}
wxBuyItem[104] = {'money':198,  'itemId':10010001, 'itemNum':'990000'}
wxBuyItem[105] = {'money':328,  'itemId':10010001, 'itemNum':'1640000'}
wxBuyItem[106] = {'money':648,  'itemId':10010001, 'itemNum':'3240000'}

#砖石
wxBuyItem[200] = {'money':0.01, 'itemId':10010002, 'itemNum':'1'}     #1分钱，测试用
wxBuyItem[201] = {'money':12,   'itemId':10010002, 'itemNum':'60000'}
wxBuyItem[202] = {'money':30,   'itemId':10010002, 'itemNum':'150000'}
wxBuyItem[203] = {'money':98,   'itemId':10010002, 'itemNum':'490000'}
wxBuyItem[204] = {'money':198,  'itemId':10010002, 'itemNum':'990000'}
wxBuyItem[205] = {'money':328,  'itemId':10010002, 'itemNum':'1640000'}
wxBuyItem[206] = {'money':648,  'itemId':10010002, 'itemNum':'3240000'}