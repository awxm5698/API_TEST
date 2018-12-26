#!/usr/bin/env python
# -*- coding:utf-8 -*-
# os.path.split(os.path.realpath(__file__))[0]  # 打印当前文件的绝对路径,./a/a.py调用./b/b.py,打印./b
# os.path.split(os.path.abspath(sys.argv[0]))[0] # 打印执行文件的绝对路径，./a/a.py调用./b/b.py,打印./a
import sys,os
import requests
sys.path.append(os.path.dirname(os.getcwd()))
from requests import exceptions
from common.common_log import Common_Log

class Common_Requests:
	def __init__(self, _url, _port=None):

		if _port == None:
			self.url = _url
		else:
			self.url = _url + ":" + _port
		self._info = Common_Log()

	def get(self, _path='/', _from_data=None):
		try:
			item = "from_data=" + str(_from_data)
			self._info.log(item)
			headers = {'Connection': 'close'}
			# requests.packages.urllib3.disable_warnings()
			_response = requests.get(self.url + _path, params=_from_data, headers=headers, verify=False)
			try:
				self._info.log("get_url="+_response.url)
				self._info.log("response_code= " + str(_response.status_code))
				# self._info.log("response=" + str(_response.json()))
			except:
				self._info.log("response is not json or has a unknown error")
			_response.close()
			return _response  # 获取服务器返回的页面信息
		except exceptions.HTTPError as e:
			_response.close()
			self._info.e_log(e)
			return 'Error: ', e

	def post(self, _path='/', _from_data=None):
		try:
			item = "from_data=" + str(_from_data)
			self._info.log(item)
			headers = {'Content-Type': 'application/json;charset=utf-8'}
			_response = requests.post(self.url + _path, json=_from_data, headers=headers, verify=False)
			try:
				self._info.log("post_url="+_response.url)
				self._info.log("response_code= " + str(_response.status_code))
				# self._info.log("response=" + str(_response.json()))
			except:
				self._info.log("response is not json or has a unknown error")
			_response.close()
			return _response
		except exceptions.HTTPError as e:
			_response.close()
			self._info.e_log(e)
			return 'Error: ', e


if __name__ == "__main__":
	url = "http://www.baidu.com"  # type: str
	t = Common_Requests(url)
	t.post()
	l = Common_Log()
	l.log("admin")

	sys.exit()
