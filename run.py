#coding=utf-8

import unittest
from mylib import HTMLTestRunner3
import time
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header

#################################################################
# ---------------------------执行参数-------------------------- #
#################################################################
emailSmtp = 'smtp.163.com' # 发件邮箱为163邮箱
emailFrom = 'testWolian@163.com'
emailFromPassWord = '*****'
emailTo = ['*****@qq.com']
timestr = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))
#################################################################
# ---------------------------邮件部分-------------------------- #
#################################################################
def send_mail(file_new):
    f = open(file_new,'rb')
    mail_body =f.read()
    f.close()

    msg = MIMEText(mail_body,'html','utf-8')
    msg['Subject'] = Header("API TEST REPORT")
    msg['From'] = emailFrom
    msg['To'] = ','.join(emailTo)

    smtp = smtplib.SMTP()
    smtp.connect(emailSmtp)
    smtp.login(emailFrom,emailFromPassWord)
    smtp.sendmail(emailFrom,emailTo,msg.as_string())
    smtp.quit()
    print("send success!")

# 查找测试目录，找到最新生成的测试报告
def new_report(test_report):
    lists = os.listdir(test_report)
    lists.sort(key=lambda fn:os.path.getatime(test_report+'/'+fn))
    file_new = os.path.join(test_report,lists[-1])
    return file_new
#################################################################
# ---------------------------执行用例-------------------------- #
#################################################################
if __name__=="__main__": # 请点击左侧箭头执行脚本
    test_dir = os.path.split(os.path.realpath(__file__))[0]+"/test_case"
    test_report = os.path.split(os.path.realpath(__file__))[0]+"/test_report/"

    #################################################################
    # --------------根据用例名称匹配需要执行的用例----------------- #
    #################################################################
    discover = unittest.defaultTestLoader.discover(test_dir, pattern='test_a_demo.py')
    # print(discover)

    # -----*------*-----*-----*------执行测试用例并写报告-----*------*-----*-----*------
    filename = test_report + timestr + "_testResult.html"
    fp = open(filename, "wb")
    runner = HTMLTestRunner3.HTMLTestRunner(stream=fp,
                                            title="API TEST REPORT",
                                            description="TESTCASE RUNNING REPORT:")
    runner.run(discover)
    fp.close()
    new_report = new_report(test_report)
    # send_mail(new_report)
