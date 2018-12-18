#!/usr/bin/env python2
# -*- coding:utf-8 -*-
from pydocumentdb import document_client

class Cosmos_DB:
    def __init__(self,url,key):
        self.url = url
        self.key = key

    def get_select_results(self, db_name, table_name,_sql):
        client = document_client.DocumentClient(self.url, {'masterKey': self.key})

        db_query = "select * from r where r.id = '{0}'".format(db_name)
        db = list(client.QueryDatabases(db_query))[0]
        db_link = db['_self']

        coll_query = "select * from r where r.id = '{0}'".format(table_name)
        coll = list(client.QueryCollections(db_link, coll_query))[0]
        coll_link = coll['_self']

        option = {'enableCrossPartitionQuery': True, 'maxItemCount': 2}
        query = {'query': _sql}
        docs = client.QueryDocuments(coll_link, query, options=option)

        return list(docs)

if __name__ == "__main__":
    url = '****'
    key = '*****'
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
