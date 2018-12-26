#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import sys, os
sys.path.append(os.path.dirname(os.getcwd()))

import unittest
from test_data import config
from test_data import set_post_data
from common import elastic_search
from common import common_requests
from common import check_result
from common import json_file
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
req = common_requests.Common_Requests(api_url)
get_data = set_post_data.set_data()
# assert_result = set_post_data.check_assert_result()
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
class test_API_tire_size_filter(common_start.MyTest):

    def test_check_filter_result(self):
        _info.log("test file name:" + os.path.basename(__file__))
        _info.log(self.__class__.__name__+"."+sys._getframe().f_code.co_name)
        data = get_data.get_vehicletpye_data()
        form_data = data.get("form_data")
        path = config.path['get_searchByVehicleType']
        response = req.post(path, form_data)
        check_res.check_str(response.json().get('code'),100000)
        check_res.check_str(response.json().get('message'),'success')

        '''get es results'''
        doc = data.get("docs")
        doc['size'] = 10000

        aggs = {}
        aggs['brand'] = get_data.get_field("brand")
        aggs['tireLoadIndex'] = get_data.get_field("tireLoadIndex")
        aggs['tireSpeedRating'] = get_data.get_field("tireSizeAttributes.tireSpeedRating")
        aggs['tireSideWall'] = get_data.get_field("tireSideWall")
        aggs['warrantyInfo'] = get_data.get_field("warrantyInfo")
        doc['aggs'] = aggs
        es_response = es.Get_Data_By_Body(doc)
        check_res.check_str(es_response.get('timed_out'), False)
        '''
        instanttiate check
        '''
        items = response.json().get('data').get('items')
        hits = es_response.get("hits").get("hits")
        check = check_result.check_results(items, hits)
        aggs = response.json()['data']['aggs']

        '''check filter brand'''
        es_buckets = es_response['aggregations']['brand']['buckets']
        brands = check.get_aggs_value_by_name(aggs,'brand')
        es_brands = check.get_es_buckets_value_by_key(es_buckets,'brand')
        count_brands = check.get_es_value_list(hits,'brand')
        count_brands.sort()
        check_res.check_list(brands, es_brands)
        check_res.check_list(brands, count_brands)


        '''check filter load index'''
        es_buckets = es_response['aggregations']['tireLoadIndex']['buckets']
        tireLoadIndexs = check.get_aggs_value_by_name(aggs, 'tireLoadIndex')
        es_tireLoadIndexs = check.get_es_buckets_value_by_key(es_buckets, 'tireLoadIndex')
        count_tireLoadIndexs = check.get_es_value_list(hits, 'tireLoadIndex')
        count_tireLoadIndexs.sort()
        check_res.check_list(tireLoadIndexs, es_tireLoadIndexs)
        check_res.check_list(tireLoadIndexs, count_tireLoadIndexs)

        '''check filter speed rating'''
        es_buckets = es_response['aggregations']['tireSpeedRating']['buckets']
        tireSpeedRatings = check.get_aggs_value_by_name(aggs, 'tireSpeedRating')
        es_tireSpeedRatings = check.get_es_buckets_value_by_key(es_buckets, 'tireSizeAttributes.tireSpeedRating')
        count_tireSpeedRatings = []
        for hit in hits:
            tireSpeedRating = hit["_source"]["tireSizeAttributes"]["tireSpeedRating"]
            if tireSpeedRating not in count_tireSpeedRatings:
                count_tireSpeedRatings.append(tireSpeedRating)
        # count_tireSpeedRatings = check.get_es_value_list(hits, 'tireSpeedRating')
        count_tireSpeedRatings.sort()
        check_res.check_list(tireSpeedRatings, es_tireSpeedRatings)
        check_res.check_list(tireSpeedRatings, count_tireSpeedRatings)

        '''check filter sidewall'''
        es_buckets = es_response['aggregations']['tireSideWall']['buckets']
        tireSideWalls = check.get_aggs_value_by_name(aggs, 'tireSideWall')
        es_tireSideWalls = check.get_es_buckets_value_by_key(es_buckets, 'tireSideWall')
        count_tireSideWalls = check.get_es_value_list(hits, 'tireSideWall')
        count_tireSideWalls.sort()
        check_res.check_list(tireSideWalls, es_tireSideWalls)
        check_res.check_list(tireSideWalls, count_tireSideWalls)

        '''check filter mileage warranty'''
        es_buckets = es_response['aggregations']['warrantyInfo']['buckets']
        warrantyInfos = check.get_aggs_value_by_name(aggs, 'warrantyInfo')
        es_warrantyInfos = check.get_es_buckets_value_by_key(es_buckets, 'warrantyInfo')
        count_warrantyInfos = check.get_es_value_list(hits, 'warrantyInfo')
        count_warrantyInfos.sort()
        check_res.check_list(warrantyInfos, es_warrantyInfos)
        check_res.check_list(warrantyInfos, count_warrantyInfos)

    def test_add_one_filter_to_request(self):
        _info.log("test file name:" + os.path.basename(__file__))
        _info.log(self.__class__.__name__+"."+sys._getframe().f_code.co_name)
        data = get_data.get_vehicletpye_data()
        form_data = data.get("form_data")
        path = config.path['get_searchByVehicleType']
        response = req.post(path, form_data)
        check_res.check_str(response.json().get('code'), 100000)
        check_res.check_str(response.json().get('message'), 'success')
        aggs = response.json().get('data').get('aggs')

        filter_dict = json_file.filter_dict()
        random_name = filter_dict.get_random_filter_name(aggs)
        random_value = filter_dict.get_random_filter_value(aggs, random_name[0])
        form_data[random_name[0]] = random_value
        filter_response = req.post(path, form_data)
        filter_aggs = filter_response.json().get('data').get('aggs')
        filter_value = filter_dict.get_random_filter_value(filter_aggs, random_name[0])

        check_res.check_list(filter_value, random_value)

        filter_totalHits = filter_response.json().get('data').get('totalHits')

        '''get es results'''
        doc = data.get("docs")
        # doc['size'] = 10000
        aggs = {}
        aggs['brand'] = get_data.get_field("brand")
        aggs['tireLoadIndex'] = get_data.get_field("tireLoadIndex")
        aggs['tireSpeedRating'] = get_data.get_field("tireSizeAttributes.tireSpeedRating")
        aggs['tireSideWall'] = get_data.get_field("tireSideWall")
        aggs['warrantyInfo'] = get_data.get_field("warrantyInfo")
        doc['aggs'] = aggs
        es_response = es.Get_Data_By_Body(doc)
        check_res.check_str(es_response.get('timed_out'), False)
        es_buckets = es_response['aggregations'][random_name[0]]['buckets']
        for item in es_buckets:
            if item['key'] == random_value[0]:
                doc_count = item['doc_count']
        check_res.check_str(filter_totalHits, doc_count)



#################################################################
# ---------------------------执行用例-------------------------- #
#################################################################
if __name__ == "__main__":
    unittest.main()




