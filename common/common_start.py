
import unittest, os, sys
sys.path.append(os.path.dirname(os.getcwd()))
from common import common_log
#################################################################
# ---------------------------启动模块-------------------------- #
#################################################################
class MyTest(unittest.TestCase):

    def setUp(self):
        _info = common_log.Common_Log()
        _info.set_result_true()   # set result is True
        _info.log("======== Start Test ========")
        # _info.log(__file__)
        print("Start Test")
        pass

    def tearDown(self):
        _info = common_log.Common_Log()
        if _info.get_result()[0] == "True":
            _info.log("-------- Pass Test --------")
            _info.log()
            print("Pass Test")
            pass
        else:
            _info.log("******** Fail Test ********")
            _info.log()
            print("Fail Test")
            assert False


if __name__ == "__main__":
    unittest.main()
