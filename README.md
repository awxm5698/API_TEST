# API_TEST
1.WIN
2.Python （pip）
3.Requests  --->pip install requests
4.Unittest   --->unittest 框架是python自带的单元测试框架，python2.1及其以后的版本已将unittest作为一个标准块放入python开发包中，所以unittest不用单独安装。
5.测试报告利用HTMLTestRunner生成。

测试思路：

1、先把每个http接口一个一个写脚本测试。（提交的json串直接放在data字典中，这里没有用到excel等写测试用例，测试用例直接用脚本实现。）
2、写完所有接口的测试脚本后，由于一个接口有好几个测试用例，所有要把同一个接口的py脚本封装成方法，每一个接口封装成一个接口类。
3、用testsuite直接调用这些接口类，构造测试集；或利用unittest自动识别测试用例，TestLoader类中提供的discover（）方法。
  （命名规则：接口名称要以test_XXX开头）
   就好把所有的接口测试用例连起来构建自动化测试了。
4、最后利用HTMLTestRunner生成测试报告。

5.，参考test_case下的脚本写接口用例，然后执行runtest_email即可（发件邮箱和收件邮箱请自行修改）

参考文件：
http://blog.csdn.net/jojoy_tester/article/details/53258261
http://blog.csdn.net/shanzhizi/article/details/50903748
https://wenku.baidu.com/view/0eae84b7f90f76c661371aba.html
