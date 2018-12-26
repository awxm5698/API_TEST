#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.dirname(os.getcwd()))

import unittest,random
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
check_res = check_result.check_assert_result()
'''
instanttiate ElasticObj
:return:
'''
es_ip = config.es_ip
index_type = config.index_type
index_name = config.index_name
es = elastic_search.ElasticObj(index_name,index_type,es_ip)
_info = common_log.Common_Log()

#################################################################
# ---------------------------用例脚本-------------------------- #
#################################################################

class test_API_searchByTireSize(common_start.MyTest):

    def test_check_api_and_es_results(self):
        _info.log("test file name:" + os.path.basename(__file__))
        _info.log(self.__class__.__name__+"."+sys._getframe().f_code.co_name)
        data = get_data.get_tires_data()
        form_data = data.get("form_data")
        path = config.path['get_searchByTireSize']
        response = t.post(path, form_data)
        check_res.check_str(response.json().get('code'),100000)
        check_res.check_str(response.json().get('message'),'success')
        # self.assertEqual(response.json().get('code'),100000)
        # self.assertEqual(response.json().get('message'),'success')

        '''get es results'''
        doc = data.get("docs")
        res = es.Get_Data_By_Body(doc)
        check_res.check_str(res.get('timed_out'), False)
        # self.assertEqual(res.get('timed_out'), False)

        '''实例化 check'''
        items = response.json().get('data').get('items')
        hits = res.get("hits").get("hits")
        check = check_result.check_results(items,hits)
        aggs = response.json().get('data').get('aggs')
        # print(aggs)

        '''将api与es的结果对比'''
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
        # check tireSpeedRating
        check.check_result("tireSpeedRating")
        # check tireLoadIndex
        check.check_result("tireLoadIndex")
        # check season
        check.check_result("season")
        # check brand
        check.check_result("brand")
        # check warrantyInfo
        check.check_result("warrantyInfo")

    def test_check_search_tilter(self):
        _info.log("test file name:" + os.path.basename(__file__))
        _info.log(self.__class__.__name__+"."+sys._getframe().f_code.co_name)
        data = get_data.get_tires_data()
        form_data = data.get("form_data")
        path = config.path['get_searchByTireSize']
        response = t.post(path, form_data)
        check_res.check_str(response.json().get('code'),100000)
        check_res.check_str(response.json().get('message'),'success')
        # self.assertEqual(response.json().get('code'),100000)
        # self.assertEqual(response.json().get('message'),'success')
        items = response.json().get('data').get('items')

        '''get brand from api result'''
        brands = []
        for item in items:
            if item not in brands:   # 去除重复brand
                brands.append(item.get('brand'))
        brand = random.sample(brands, 1)  #从结果随机取一个brand

        '''增加过滤条件brand通过api去查询'''
        form_data["brand"] = brand
        brand_response = t.post(path, form_data)
        check_res.check_str(response.json().get('code'),100000)
        check_res.check_str(response.json().get('message'),'success')
        # self.assertEqual(brand_response.json().get('code'), 100000)
        # self.assertEqual(brand_response.json().get('message'), 'success')
        brand_items = brand_response.json().get('data').get('items')

        '''再从过滤结果里面取brand'''
        for item in brand_items:
            check_res.check_str(item.get('brand'),brand[0])
            # self.assertEqual(item.get('brand'),brand[0])

        '''增加过滤条件brand通过es去查询'''
        brand = get_data.tire_data("brand", brand[0])
        doc = data.get("docs")
        doc["query"]["bool"]["must"].append(brand)

        es_response = es.Get_Data_By_Body(doc)
        check_res.check_str(es_response.get('timed_out'), False)
        # self.assertEqual(es_response.get('timed_out'), False)

        '''实例化 check'''
        items = brand_response.json().get('data').get('items')
        hits = es_response.get("hits").get("hits")
        check = check_result.check_results(items,hits)

        '''将api与es的结果对比'''
        # check productId
        check.check_result('productId')
        # check upc
        check.check_result("upc")
        # check tireSideWall
        check.check_result("tireSideWall")
        # check productName
        check.check_result("productName")
        # check brand
        check.check_result("brand")
        # check tireLoadIndex
        check.check_result("tireLoadIndex")
        # check season
        check.check_result("season")






#################################################################
# ---------------------------执行用例-------------------------- #
#################################################################
if __name__ == "__main__":
    unittest.main()


