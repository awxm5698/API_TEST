#!/usr/bin/env python2
# -*- coding:utf-8 -*-
# os.path.split(os.path.realpath(__file__))[0]  # 打印当前文件的绝对路径,./a/a.py调用./b/b.py,打印./b
# os.path.split(os.path.abspath(sys.argv[0]))[0] # 打印执行文件的绝对路径，./a/a.py调用./b/b.py,打印./a
			
import requests,sys
from requests import exceptions
from requests_toolbelt import SSLAdapter
import sys,os,re
#path = os.path.split(os.path.abspath(sys.argv[0]))[0]

sys.dont_write_bytecode = True


class testCommon():
	def __init__(self,url,port=None):
		if port == "" or port == None:
			self.url = url
		else:
			self.url = url + ":"+port
		
	def get(self,path,wordbook):
		try:
			headers={'Connection':'close'}
			requests.packages.urllib3.disable_warnings()
			response = requests.get(self.url + path, params = wordbook,headers = headers, verify=False)
			#response.encoding = 'utf-8'
			#print response.url
			#print response.cookies
			#print response.json()
			return response #获取服务器返回的页面信息
		except exceptions.HTTPError as e:
			return 'Error: ',e
			
	def post(self,path,wordbook):
		try:
			headers = {'Content-Type':'application/json;charset=utf-8'}
			response = requests.post(self.url + path, data = wordbook,verify=False)
			#print response.status_code
			#print response.headers
			#print response.cookies
			return response
		except exceptions.HTTPError as e:
			return 'Error: ',e
if __name__ == "__main__":
	url = "http://168.61.148.253"
	port = "8080"
	year = '2017'
	path = '/item/vehicle/makes/'+year
	wordbook = ''
	t = testCommon(url,port)
	response = t.get(path,wordbook)
	print response.json()
	

	
	
