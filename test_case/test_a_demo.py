#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import unittest
import sys, os,logging
sys.path.append(os.path.dirname(os.getcwd()))
# print(paths[0:paths.rfind("\\")])
from common import common_requests
from common import common_log
from common import common_start
from common import check_result

#################################################################
# --------------------------用例参数--------------------------- #
#################################################################

url = "http://www.baidu.com"
req = common_requests.Common_Requests(url)
_info = common_log.Common_Log()
c = check_result.check_assert_result()

#################################################################
# ---------------------------用例脚本-------------------------- #
#################################################################
class test_API_GET(common_start.MyTest):
    def test_API_GET(self):
        _info.log("test file name:" + os.path.basename(__file__))
        _info.log(self.__class__.__name__+"."+sys._getframe().f_code.co_name)
        print(sys._getframe().f_code)
        print(os.path.basename(__file__))
        self.assertTrue("True","yes")

        # response = req.get()

    def test_API_post(self):
        _info.log("test file name:" + os.path.basename(__file__))
        _info.log(self.__class__.__name__+"."+sys._getframe().f_code.co_name)
        # response = req.post()

    def test_check(self):
        _info.log("test file name:" + os.path.basename(__file__))
        _info.log(self.__class__.__name__+"."+sys._getframe().f_code.co_name)
        self.assertEqual("1000", '1000')

        c.check_str("1000", 1000)

#################################################################
# ---------------------------执行用例-------------------------- #
#################################################################
if __name__ == "__main__":
    unittest.main()
