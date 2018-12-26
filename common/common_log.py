#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from test_data import config

class Common_Log:
    def __init__(self):
        self.path = os.path.join(os.path.dirname(os.getcwd()), "test_report")
        self.make_dir(self.path)
        self.log_file = os.path.join(self.path, time.strftime("%Y-%m-%d") + "_log.log")
        self.e_log_file = os.path.join(self.path, time.strftime("%Y-%m-%d") + "_e_log.log")
        self.result_file = os.path.join(self.path, "run_result.txt")

    def make_dir(self, path):
        is_exists = os.path.exists(path)
        if not is_exists:
            os.makedirs(path)

    def log(self, temp=None):
        if config.common_config.get("write_log"):
            log_time = time.strftime("%Y-%m-%d %H:%M:%S")
            # 创建日志文件，每天一个文件，追加写入
            f = open(self.log_file, 'a')
            if temp is not None:
                f.write(str(log_time) + "  " + str(temp) + "\n")
            else:
                f.write("\n")
            f.close()


    def e_log(self, temp=None):
        if config.common_config.get("write_log"):
            log_time = time.strftime("%Y-%m-%d %H:%M:%S")
            # 创建异常日志文件，每天一个文件，追加写入
            f = open(self.e_log_file, 'a')
            if temp is not None:
                f.write(str(log_time) + "  " + str(temp) + "\n")
            else:
                f.write("\n")
            f.close()


# 执行报错，输出错误日志及报错行号公共用例
    def run_error(self, test_case_name,test_case_line):
        item = "Error, test case '" + test_case_name + "' line '" \
               + str(test_case_line) + "' running fail, please try again!"
        print(item)
        self.log(item)

    def set_result_true(self):
        f = open(self.result_file, 'w')
        f.write("True")
        f.close()

    def set_result_false(self):
        f = open(self.result_file, 'w')
        f.write(str("False"))
        f.close()

    def get_result(self):
        f = open(self.result_file, 'r')
        result = f.readlines()
        f.close()
        return result

if __name__ == "__main__":
    t = Common_Log()
    print(t.path)
    print(t.log_file)
    print(t.e_log_file)
    print(t.result_file)
    print(os.path.dirname(os.getcwd()))


