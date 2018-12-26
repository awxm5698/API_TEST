#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import json
import random
import sys,os
sys.path.append(os.path.dirname(os.getcwd()))
from common import common_log

class json_files:

    def __init__(self, file_path):
        self._info = common_log.Common_Log()
        self.file_path = file_path

    def read_json(self):
        with open(self.file_path, 'r') as load_f:
            load_dict = json.load(load_f)
            return load_dict

    def read_all_key(self, load_dict):
        pram = []
        for item in load_dict:
            pram.append(item)
        self._info.log(pram)
        return pram

    def get_random_key(self,load_dict):
        pram = []
        for item in load_dict:
            pram.append(item)
        random_pram = random.sample(pram,1)
        self._info.log("random_pram:" + str(random_pram))
        return random_pram

class filter_dict:

    def __init__(self):
        self._info = common_log.Common_Log()

    def get_random_filter_name(self,load_dict):
        pram = []
        for item in load_dict:
            pram.append(item['name'])

        random_pram = random.sample(pram,1)
        self._info.log("random_pram:" + str(random_pram))
        return random_pram

    def get_random_filter_value(self,load_dict, name):

        for item in load_dict:
            if item['name'] == name:
                values = item['value']
        if len(values) > 0:
            random_value = random.sample(values, 1)
        self._info.log("random_pram:" + str(random_value))
        return random_value



if __name__ == '__main__':
    # json_path = json_files("../test_data/tiresobj1.json")
    # json_data = json_path.read_json(json_path)
    # print(json_data)
    # # width_list = json_path.read_data(json_data)
    # # print(width_list)
    # width = json_path.get_random_key(json_data)
    # print(width)
    # print(json_data.get(width[0]))
    # # width1 = json_path.get_random_key(json_data.get(width[0]))
    # # print(width1)
    # tireRatio_dict = json_data.get(width[0])
    # tireRatio = json_path.get_random_key(tireRatio_dict)
    # print(tireRatio)
    # rimSize_list = tireRatio_dict.get(tireRatio[0])
    # rimSize = json_path.get_random_key(rimSize_list)
    # print(rimSize)

    json_path = json_files("../test_data/vehicletype.json")
    json_data = json_path.read_json()
    year = json_path.read_all_key(json_data)
    print(year)
    # make_dict = json_data.get(year[0])
    # make = json_path.get_random_key(make_dict)
    # print(make)
    # model_list = make_dict.get(make[0])
    # print("aaaa---",model_list)
    # model = json_path.get_random_key(model_list)
    # print(model)
    # tireSize = model_list[model[0]]
    # for i in tireSize:
    #     print(i)

