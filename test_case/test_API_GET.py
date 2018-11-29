#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import json
import unittest
import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')
sys.dont_write_bytecode = True
path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(path[0:path.rfind("\\")])
# print sys.path
from common import common_requests
#################################################################
# --------------------------用例参数--------------------------- #
#################################################################

url = "http://168.61.148.253"
port = "8080"
t = common_requests.testCommon(url,port)
#################################################################
# ---------------------------启动模块-------------------------- #
#################################################################
class MyTest(unittest.TestCase):
    def setUp(self):
        print "strat test"
        pass
    def tearDown(self):
        print "end test"
        pass
#################################################################
# ---------------------------用例脚本-------------------------- #
#################################################################
class test_API_GET(MyTest):
	
    def test_API_GET(self):
		year = '2017'
		path = '/item/vehicle/makes/'+year
		wordbook = ''
		response = t.get(path,wordbook)
		print response.json()
		
		
#################################################################
# ---------------------------执行用例-------------------------- #
#################################################################
if __name__=="__main__":
    unittest.main()
