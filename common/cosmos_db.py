#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys,os
sys.path.append(os.path.dirname(os.getcwd()))
from pydocumentdb import document_client
from common import common_log
class Cosmos_DB:
    def __init__(self,url,key):
        self.url = url
        self.key = key
        self._info = common_log.Common_Log()

    def get_select_results(self, db_name, table_name,_sql):
        client = document_client.DocumentClient(self.url, {'masterKey': self.key})

        db_query = "select * from r where r.id = '{0}'".format(db_name)
        db = list(client.QueryDatabases(db_query))[0]
        db_link = db['_self']
        self._info.log("Connect DB='"+db_name+"' success!")
        coll_query = "select * from r where r.id = '{0}'".format(table_name)
        coll = list(client.QueryCollections(db_link, coll_query))[0]
        coll_link = coll['_self']
        self._info.log("Connect Table='"+table_name+"' success!")
        option = {'enableCrossPartitionQuery': True, 'maxItemCount': 2}
        query = {'query': _sql}
        docs = client.QueryDocuments(coll_link, query, options=option)
        self._info.log("Execute SQL='"+_sql+"' success!")
        self._info.log("SQL results='"+str(list(docs))+"'")
        return list(docs)

    def get_field_list(self, db_name, table_name,_sql, field):
        docs = self.get_select_results(db_name, table_name,_sql)
        field_list = []
        for doc in list(docs):
            field_list.append(str(doc[field]))
        self._info.log("value "+field+"='"+field_list+"'")
        return field_list


if __name__ == "__main__":
    url = 'https://dev-tirebattery-app.documents.azure.com:443/ '
    key = 'lXy59oFu6uAbraxLgbMIyh8EF242LIqBvEBuuZWD82Su98xulfi82HuSZt74iFTf6zRx9e2AvwEZdzKPhmgq6g=='
    db_name = 'TBC_QA'
    table_name = 'vehicleYear'
    _sql = 'SELECT v.modelYear FROM vehicleYear v'
    c = Cosmos_DB(url,key)
    docs = c.get_select_results(db_name,table_name,_sql)
    print(list(docs))
    arr_year = []
    for doc in list(docs):
        arr_year.append(doc['modelYear'])
    print(arr_year)
