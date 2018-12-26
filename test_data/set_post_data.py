#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import sys,os
sys.path.append(os.path.dirname(os.getcwd()))
from common import json_file
from common import common_log

class set_data:

    def __init__(self):
        self._info = common_log.Common_Log()

    def get_file_path(self, file_name):
        # current_path = os.path.split(os.path.realpath(__file__))[0]
        path = os.path.join(os.getcwd(), file_name)
        return path

    def post_tire_size_data(self):
        post_tire_size_pram = {
            "avgRating": [],
            "brand": [],
            "brandOrderBy": "",
            "clubId": [],
            "construction": [],
            "keywords": [""],
            "page": 0,
            "pageSize": 20,
            "priceOrderBy": "asc",
            "recommended": [""],
            "rimDiameter": [],
            "season": [],
            "terrain": [],
            "tireLoadIndex": [],
            "tireRatio": [],
            "tireSideWall": [],
            "tireSizes": [],
            "tireSpeedRating": [],
            "warrantyInfo": [],
            "width": []
        }
        self._info.log(str(post_tire_size_pram))
        return post_tire_size_pram

    def es_tire_size_data(self, item, field=None):
        docs = {"query": {
                    "bool": {
                        "must": item
                        }
                    },
                "sort":{
                    "priceWithoutTax":"asc"
                },
                "size": 20
                }
        if field is not None:
            docs["aggs"] = field
        self._info.log(str(docs))
        return docs

    def es_vehicletpye_data(self, item, field=None):
        docs = {"query": {
                    "bool": {
                        "should": item
                        }
                    },
                "sort":{
                    "priceWithoutTax":"asc"
                },
                "size": 20
                }
        if field is not None:
            docs["aggs"] = field
        self._info.log(str(docs))
        return docs

    def get_field(self, keyword, select_type=None):
        item = keyword+".keyword"
        if select_type is None:
            select_type = "terms"
        field ={
            select_type:{
                "field":item
            }
        }
        self._info.log(str(field))
        return field

    def tire_data(self,keyword, value, select_type=None):
        item = keyword+".keyword"
        if select_type is None:
            select_type = "term"
        term = {
            select_type: {
                item: {
                    "value": value

                }
            }
        }
        self._info.log(str(term))
        return term

    def get_tires_data(self):
        '''实例化 json_file'''
        path = self.get_file_path("tires_all.json")
        json_path = json_file.json_files(path)

        '''从json file里面取值'''
        json_data = json_path.read_json(json_path)
        width = json_path.get_random_key(json_data)
        tireRatio_dict = json_data.get(width[0])
        tireRatio = json_path.get_random_key(tireRatio_dict)
        rimDiameter_dict = tireRatio_dict.get(tireRatio[0])
        rimDiameter = json_path.get_random_key(rimDiameter_dict)
        width = ['225']
        tireRatio = ['50']
        rimDiameter = ['17']
        '''get api results'''
        form_data = self.post_tire_size_data()
        form_data["width"] = width
        form_data["rimDiameter"] = rimDiameter
        form_data["tireRatio"] = tireRatio
        '''get es results'''

        term = []
        widths = self.tire_data("tireSizeAttributes.width", width[0])
        rimDiameter = self.tire_data("tireSizeAttributes.rimDiameter", rimDiameter[0])
        tireRatio = self.tire_data("tireSizeAttributes.tireRatio", tireRatio[0])
        term.append(rimDiameter)
        term.append(widths)
        term.append(tireRatio)
        docs = self.es_tire_size_data(term)
        data = {}
        data["form_data"] = form_data
        data["docs"] = docs
        self._info.log(str(data))
        return data

    def get_vehicletpye_data(self):
        '''实例化 json_file'''
        path = self.get_file_path("vehicle_qa_allyear.json")
        json_path = json_file.json_files(path)
        json_data = json_path.read_json(json_path)
        year = json_path.get_random_key(json_data)
        make_dict = json_data.get(year[0])
        make = json_path.get_random_key(make_dict)
        model_dict = make_dict.get(make[0])
        model = json_path.get_random_key(model_dict)

        # get all tire size
        tireSize_list = model_dict.get(model[0]).get("trim")
        tireSizes = []
        for key in tireSize_list:
            tireSizes.extend(tireSize_list.get(key))
        # remove the repeat tire size
        tireSize = []
        for item in tireSizes:
            if item not in tireSize:
                tireSize.append(item)

        '''get api results'''
        form_data = self.post_tire_size_data()
        form_data["tireSizes"] = tireSize

        '''get es results'''
        term = []
        for tire_size in tireSize:
            tire_size = self.tire_data("tireSize", tire_size, "prefix")
            term.append(tire_size)
        docs = self.es_vehicletpye_data(term)
        data = {}
        data["form_data"] = form_data
        data["docs"] = docs
        self._info.log(str(data))
        return data

if __name__ == '__main__':
    t = set_data()
    print(t.get_file_path(""))
