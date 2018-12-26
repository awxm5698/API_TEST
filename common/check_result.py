#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import unittest
import sys, os

sys.path.append(os.path.dirname(os.getcwd()))
from common import common_log


class check_results(unittest.TestCase):

    def __init__(self, items=None, hits=None):
        self.items = items
        self.hits = hits
        self._info = common_log.Common_Log()

    def check_result(self, pram):
        api_value_list = self.get_api_value_list(self.items, pram)
        es_value_list = self.get_es_value_list(self.hits, pram)
        check_assert_result().check_list(api_value_list,es_value_list)
        # try:
        #     self.assertListEqual(api_value_list, es_value_list)
        #     self._info.log("pass :api_" + pram + "=" + "es_" + pram)
        # except:
        #     self._info.set_result_false()
        #     self._info.log("fail :api_" + pram + "!=" + "es_" + pram)

    def get_api_value_list(self, items, pram):
        arr = []
        for item in items:
            if str(item.get(pram)) not in arr:
                arr.append(str(item.get(pram)))
        self._info.log(pram + "=" + str(arr))
        return arr

    def get_es_value_list(self, hits, pram):
        arr = []
        for hit in hits:
            if str(hit.get("_source").get(pram)) not in arr:
                arr.append(str(hit.get("_source").get(pram)))
        self._info.log(pram + "=" + str(arr))
        return arr

    def get_aggs_value_by_name(self, aggs, name):
        for agg in aggs:
            if agg['name'] == name:
                values = agg['value']
        values.sort()
        self._info.log(str(name) + "=" + str(values))
        return values

    def get_es_buckets_value_by_key(self, es_buckets, key):
        es_values = []
        for key in es_buckets:
            es_values.append(key['key'])
        es_values.sort()
        self._info.log(str(key) + "=" + str(es_values))
        return es_values


class check_assert_result(unittest.TestCase):

    def __init__(self):
        self._info = common_log.Common_Log()

    def check_list(self, list1, list2):
        _list1 = []
        _list2 = []
        for _list in list1:
            _list1.append(str(_list))
        for _list in list2:
            _list2.append(str(_list))
        try:
            self.assertListEqual(_list1, _list2)
            self._info.log("pass :" + str(list1)+"="+str(list2))
        except:
            self._info.set_result_false()
            try:
                raise Exception
            except:
                f = sys.exc_info()[2].tb_frame.f_back
            self._info.run_error(f.f_code.co_name, f.f_lineno)
            self._info.log("fail :" + str(list1)+"!="+str(list2))

    def check_str(self, str1, str2):
        str1 = str(str1)
        str2 = str(str2)
        # try:
        if str1 == str2:
            self._info.log("pass :" + str(str1)+"="+str(str2))
        else:
            self._info.set_result_false()
            try:
                raise Exception
            except:
                f = sys.exc_info()[2].tb_frame.f_back
            self._info.run_error(f.f_code.co_name, f.f_lineno)
            self._info.log("fail :" + str(str1)+"!="+str(str2))

if __name__ == "__main__":
    t = check_assert_result()
    l1 = [' Goodyear', 'Bridgestone', 'Goodyear', 'Hankook', 'Kumho', 'Michelin', 'Pirelli']
    l2 = [' Goodyear', 'Bridgestone', 'Goodyear', 'Hankook', 'Kumho', 'Michelin', 'Pirelli']
    t.check_list(l1,l2)
