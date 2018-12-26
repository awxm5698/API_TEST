#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.path.dirname(os.getcwd()))

import unittest
from test_data import config
from test_data import set_post_data
from common import elastic_search
from common import common_requests
from common import check_result
from common import common_log
from common import common_start

#################################################################
# --------------------------用例参数--------------------------- #
#################################################################
'''
instanttiate common_requests
:return:
'''
api_url = config.api_url
t = common_requests.Common_Requests(api_url)
get_data = set_post_data.set_data()
'''
instanttiate ElasticObj
:return:
'''
es_ip = config.es_ip
index_type = config.index_type
index_name = config.index_name
es = elastic_search.ElasticObj(index_name,index_type,es_ip)
_info = common_log.Common_Log()
check_res = check_result.check_assert_result()

#################################################################
# ---------------------------用例脚本-------------------------- #
#################################################################
class test_API_searchByVehicleType(common_start.MyTest):

    def test_check_api_and_es_results(self):
        _info.log("test file name:" + os.path.basename(__file__))
        _info.log(self.__class__.__name__+"."+sys._getframe().f_code.co_name)
        data = get_data.get_vehicletpye_data()
        form_data = data.get("form_data")
        path = config.path['get_searchByVehicleType']
        response = t.post(path, form_data)
        check_res.check_str(response.json().get('code'),100000)
        check_res.check_str(response.json().get('message'),'success')
        # self.assertEqual(response.json().get('code'),100000)
        # self.assertEqual(response.json().get('message'),'success')
        '''
        get es results
        '''
        doc = data.get("docs")
        es_response = es.Get_Data_By_Body(doc)
        check_res.check_str(es_response.get('timed_out'), False)
        # self.assertEqual(es_response.get('timed_out'), False)
        '''
        instanttiate check
        '''
        items = response.json().get('data').get('items')
        hits = es_response.get("hits").get("hits")
        check = check_result.check_results(items,hits)
        # check productId
        check.check_result('productId')
        # check upc
        check.check_result("upc")
        # check tireSideWall
        check.check_result("tireSideWall")
        # check productName
        check.check_result("productName")
        # check tireSizeAttributes
        check.check_result("tireSizeAttributes")
        # check tireSize
        check.check_result("tireSize")


#################################################################
# ---------------------------执行用例-------------------------- #
#################################################################
if __name__ == "__main__":
    unittest.main()

