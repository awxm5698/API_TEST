#coding = utf-8

import sys,os
sys.path.append(os.path.dirname(os.getcwd()))
from elasticsearch import Elasticsearch
from common import common_log

class ElasticObj:
    def __init__(self, index_name,index_type,ip='127.0.0.1'):
        self._info = common_log.Common_Log()
        '''
        :param index_name: 索引名称
        :param index_type: 索引类型
        '''
        self.index_name = index_name
        self.index_type = index_type
        # 无用户名密码状态
        self.es = Elasticsearch([ip])
        # 用户名密码状态
        # self.es = Elasticsearch([ip],http_auth=('elastic', 'password'),port=9200)

    def Get_Data_By_Body(self,doc):
        _searched = self.es.search(index=self.index_name, doc_type=self.index_type, body=doc)
        self._info.log("es_doc="+str(doc))
        # self._info.log("es_results="+str(_searched))
        return _searched




if __name__ == "__main__":
    t = ElasticObj("item_tire_detail","_doc",ip ="168.61.148.253")
    doc = {'query': {'match_all': {}}}
    print(t.Get_Data_By_Body(doc))