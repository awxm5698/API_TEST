#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.path.dirname(os.getcwd()))

import json
import unittest
import random
from test_data import config
from common import elastic_search
from common import common_requests
from common import check_result
from common import json_file
from common import cosmos_db
from common import common_log
from common import common_start



#################################################################
# --------------------------用例参数--------------------------- #
#################################################################

'''
instanttiate Cosmos_DB
:return:
'''
db_url = config.db_url
key = config.key
db_name = config.db_name
cosmosdb = cosmos_db.Cosmos_DB(db_url,key)

#################################################################
# ---------------------------用例脚本-------------------------- #
#################################################################

class test_API_compare_jsonFile(common_start.MyTest):

    def test_check_jsonFile_cosmosdb(self):

        '''
        instanttiate json_file
        :return:
        '''
        json_path = json_file.json_files("../test_data/vehicletype.json")
        json_data = json_path.read_json(json_path)
        year_from_json = json_path.read_all_key(json_data)
        year = json_path.get_random_key(json_data)
        print(year_from_json)
        year_from_json.sort()
        make_dict = json_data.get(year_from_json[0])
        make_from_json = json_path.read_all_key(make_dict)
        make = json_path.get_random_key(make_dict)
        print(make_from_json)
        model_dict = make_dict.get(make_from_json[0])
        model_from_json = json_path.read_all_key(model_dict)
        model = json_path.get_random_key(model_dict)
        print(model_from_json)
        tireSize_list = model_dict.get(model_from_json[0])
        tireSize_from_json = random.sample(tireSize_list,1)

        table1_name = 'vehicleYear'
        table2_name = 'vehicleBase'
        year_sql = 'SELECT v.modelYear FROM vehicleYear v'
        make_sql = 'SELECT distinct vb.makeName FROM vehicleBase vb'
        model_sql = 'SELECT distinct vb.modelName FROM vehicleBase vb'
        trim_sql = 'SELECT distinct vb.submodelName FROM vehicleBase vb'
        year_make_sql = 'SELECT distinct vb.makeName FROM vehicleBase vb where vb.modelYear='+year+''
        make_model_sql = 'SELECT distinct vb.modelName FROM vehicleBase vb where vb.makeName='+make+''
        tireSize_sql = ''
        year_from_cosmosdb = cosmosdb.get_field_list(db_name, table1_name, year_sql, "modelYear")
        print(year_from_cosmosdb)








#################################################################
# ---------------------------执行用例-------------------------- #
#################################################################
if __name__ == "__main__":
    unittest.main()


