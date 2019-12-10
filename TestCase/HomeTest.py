
from Base.BaseRunner import ParametrizedTestCase
import os
import sys

from PageObject.Home.FirstOpenClick import FirstOpenClick
from PageObject.Home.FirstOpenPage import *
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class HomeTest(ParametrizedTestCase):
    # def testFirstOpen(self):
    #     app = {"logTest": self.logTest, "driver": self.driver, "path": PATH("../yamls/home/demo.yaml"),
    #            "device": self.devicesName, "caseName": sys._getframe().f_code.co_name}
    #     page = FirstOpenPage(app)
    #     page.operate()
    #     page.checkPoint()

    def testFirstClick(self):
        app = {"logTest": self.logTest, "driver": self.driver, "path": PATH("../yamls/home/firstClick.yaml"),
               "device": self.devicesName, "caseName": sys._getframe().f_code.co_name}
        page = FirstOpenClick(app)
        page.operate()
        page.checkPoint()




    @classmethod
    def setUpClass(cls):
        super(HomeTest, cls).setUpClass()



    @classmethod
    def tearDownClass(cls):
        super(HomeTest, cls).tearDownClass()
