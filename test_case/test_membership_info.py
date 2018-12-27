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
from common import cosmos_db



#################################################################
# --------------------------用例参数--------------------------- #
#################################################################


api_url = config.api_url
req = common_requests.CommonRequests(api_url)

get_data = set_post_data.SetData()
check_res = check_result.CheckAssertResult()

db_url = config.db_url
key = config.key
db_name = config.db_name
cos = cosmos_db.CosmosDB(db_url,key)

db = cos.connect_db(db_name)
_info = common_log.CommonLog()





#################################################################
# ---------------------------用例脚本-------------------------- #
#################################################################


class TestMembershipInfo(common_start.MyTest):

    def test_api_and_cosmosdb_membershipinfo_results(self):
        _info.log("test file name:" + os.path.basename(__file__))
        _info.log(self.__class__.__name__+"."+sys._getframe().f_code.co_name)
        path = config.path['get_membership_info']
        membership_id = config.membership_id
        response = req.get(path, membership_id,write_log=True)
        check_res.check_str(response.json().get('code'),100000)
        check_res.check_str(response.json().get('message'),'success')

        """接口获取会员的基本信息
        """
        data = response.json()['data']
        api_membershipInfo = {}
        api_membershipInfo['membershipId'] = data['membershipId']
        api_membershipInfo['firstName'] = data['firstName']
        api_membershipInfo['lastName'] = data['lastName']
        api_membershipInfo['startDate'] = data['startDate']
        api_membershipInfo['type'] = data['type']

        """随机获取会员名下一辆车的信息和vehicleId
        """
        vehicles = data['vehicles']
        random_vehicle = random.sample(vehicles,1)[0]
        api_vehicleId = random_vehicle['vehicleId']
        api_random_vehicle = {}
        api_random_vehicle['licenseId'] = random_vehicle['licenseId']
        api_random_vehicle['modelYear'] = random_vehicle['modelYear']
        api_random_vehicle['makeName'] = random_vehicle['makeName']
        api_random_vehicle['modelName'] = random_vehicle['modelName']
        api_random_vehicle['submodelName'] = random_vehicle['submodelName']
        api_random_vehicle['color'] = random_vehicle['color']
        api_random_vehicle['licenseStateCode'] = random_vehicle['licenseStateCode']
        api_random_vehicle['tire'] = random_vehicle['tire']

        """从cosmosDB查询会员基本信息
        """
        table_name = 'membershipInfo'
        table = cos.connect_table(db,table_name)
        membershipInfo_sql = 'SELECT m.lastName,m.firstName,m.membershipId,m.type,m.startDate FROM membershipInfo m ' \
                             'where m.membershipId = "' + config.membership_id +'"'
        membershipInfo_docs = cos.get_select_results(table,membershipInfo_sql)
        check_res.check_dict(api_membershipInfo,membershipInfo_docs[0])

        """通过接口获取的随机的vehicleId，到cosmosdb查询该车辆信息
        """
        vehicles_sql= 'SELECT m.vehicles FROM membershipInfo m where m.membershipId = "' + config.membership_id +'"'
        vehicles_docs = cos.get_select_results(table,vehicles_sql)
        vehicles = vehicles_docs[0]['vehicles']
        for vehicle in vehicles:
            if vehicle['vehicleId'] == api_vehicleId:
                print(vehicle)
                cs_vehicles = {}
                cs_vehicles['licenseId'] = vehicle['licenseId']
                cs_vehicles['modelYear'] = vehicle['modelYear']
                cs_vehicles['makeName'] = vehicle['makeName']
                cs_vehicles['modelName'] = vehicle['modelName']
                cs_vehicles['submodelName'] = vehicle['submodelName']
                cs_vehicles['color'] = vehicle['color']
                cs_vehicles['licenseStateCode'] = vehicle['licenseStateCode']
                cs_vehicles['tire'] = vehicle['tire']
        check_res.check_dict(api_random_vehicle,cs_vehicles)


#################################################################
# ---------------------------执行用例-------------------------- #
#################################################################


if __name__ == "__main__":
    unittest.main()
