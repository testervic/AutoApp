from Base.BaseError import get_error
from Base.BaseYaml import getYam
from Base.BaseOperate import OperateElement
import time
from Base.BaseElementEnmu import Element as be
import os
from PageObject.SumResult import statistics_result

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class PagesObjects:
    '''
    page层
    kwargs: WebDriver driver, String path(yaml配置参数)
    isOperate: 操作失败，检查点就失败
    testInfo：
    testCase：
    '''

    def __init__(self, kwargs):
        self.driver = kwargs["driver"]
        if kwargs.get("launch_app", "0") == "0":  # 若为空，重新打开app
            self.driver.launch_app()
        # self.path = kwargs["path"]
        self.operateElement = OperateElement(self.driver)
        self.isOperate = True
        self.test_msg = kwargs["test_msg"]
        self.testInfo = self.test_msg[1]["testinfo"]
        self.testCase = self.test_msg[1]["testcase"]
        self.testcheck = self.test_msg[1]["check"]
        self.device = kwargs["device"]
        self.logTest = kwargs["logTest"]
        self.caseName = kwargs["caseName"]
        self.get_value = []
        self.is_get = False  # 检查点特殊标志，结合get_value使用。若为真，说明检查点要对比历史数据和实际数据
        self.msg = ""

    '''
     操作步骤
    '''

    def operate(self):
        if self.test_msg[0] is False: # 如果用例编写错误
            self.isOperate = False
            return False
        for item in self.testCase:
            m_s_g = self.msg + "\n" if self.msg != "" else ""
            result = self.operateElement.operate(item, self.testInfo, self.logTest, self.device)
            if not result["result"]:
                msg = "执行过程中失败，请检查元素是否存在" + item["element_info"] + "," + result.get("text", " ")
                if not result.get("webview", True):
                    msg = "切换到webview失败，请确定是否在webview页面"
                #print(type(item))
                print(item)
                print(result)
                print(msg)
                self.msg = m_s_g + msg
                self.testInfo[0]["msg"] = msg
                self.isOperate = False
                return False
            if item.get("is_time", "0") != "0":
                time.sleep(item["is_time"])  # 等待时间
                print("--等待下---")

            if item.get("operate_type", "0") == be.GET_VALUE or item.get("operate_type", "0") == be.GET_CONTENT_DESC:
                self.get_value.append(result["text"])
                self.is_get = True  # 对比数据

        return True

    def checkPoint(self, kwargs={}):
        result = self.check(kwargs)
        if self.test_msg[0] is not False:  # 如果用例编写正确
            if result is not True and be.RE_CONNECT:
                self.msg = "用例失败重连过一次，失败原因:" + self.testInfo[0]["msg"]
                self.logTest.buildStartLine(self.caseName + "_失败重连")  # 记录日志
                self.operateElement.switchToNative()
                self.driver.launch_app()
                self.isOperate = True
                self.get_value = []
                self.is_get = False
                self.operate()
                result = self.check(kwargs)
                self.testInfo[0]["msg"] = self.msg
            self.operateElement.switchToNative()

        statistics_result(result=result, testInfo=self.testInfo, caseName=self.caseName,
                          driver=self.driver, logTest=self.logTest, devices=self.device,
                          testCase=self.testCase,
                          testCheck=self.testcheck)

    '''
    检查点
    caseName:测试用例函数名 用作统计
    logTest： 日志记录
    devices 设备名
    contrary：相反检查点，传1表示如果检查元素存在就说明失败
    toast: 表示提示框检查点
    contrary_getval: 相反值检查点，如果对比成功，说明失败
    check_point: 自定义检查结果    
    '''

    def check(self, kwargs):
        result = True
        m_s_g = self.msg + "\n" if self.msg != "" else ""
        # 如果有重跑机制，成功后会默认把日志传进来


        # if kwargs.get("check_point", "0") != "0": 自定义检查点
        #     return kwargs["check_point"]

        if self.isOperate:
            for item in self.testcheck:
                if kwargs.get("check", be.DEFAULT_CHECK) == be.TOAST:
                    result = \
                    self.operateElement.toast(item["element_info"], testInfo=self.testInfo, logTest=self.logTest)[
                        "result"]
                    if result is False:
                        m = get_error(
                            {"type": be.DEFAULT_CHECK, "element_info": item["element_info"], "info": item["info"]})
                        self.msg = m_s_g + m
                        print(m)
                        self.testInfo[0]["msg"] = m
                    break
                else:
                    resp = self.operateElement.operate(item, self.testInfo, self.logTest, self.device)

                if kwargs.get("check", be.DEFAULT_CHECK) == be.DEFAULT_CHECK and not resp["result"]:
                    m = get_error(
                        {"type": be.DEFAULT_CHECK, "element_info": item["element_info"], "info": item["info"]})
                    self.msg = m_s_g + m
                    print(m)
                    self.testInfo[0]["msg"] = m
                    result = False
                    break
                if kwargs.get("check", be.DEFAULT_CHECK) == be.CONTRARY and resp["result"]:
                    m = get_error({"type": be.CONTRARY, "element_info": item["element_info"], "info": item["info"]})
                    self.msg = m_s_g + m
                    print(m)
                    self.testInfo[0]["msg"] = self.msg
                    result = False
                    break
                # 检查点关键字contrary_getval: 相反值检查点，如果对比成功，说明失败
                if kwargs.get("check", be.DEFAULT_CHECK) == be.CONTRARY_GETVAL and self.is_get and resp["result"] \
                        in self.get_value:
                    m = get_error(
                        {"type": be.CONTRARY_GETVAL, "current": item["element_info"], "history": resp["text"]})
                    self.msg = m_s_g + m
                    print(m)
                    self.testInfo[0]["msg"] = m
                    result = False
                    break
                if kwargs.get("check", be.DEFAULT_CHECK) == be.COMPARE and self.is_get and resp["text"] \
                        not in self.get_value:  # 历史数据和实际数据对比
                    result = False
                    m = get_error({"type": be.COMPARE, "current": item["element_info"], "history": resp["text"]})
                    self.msg = m_s_g + m
                    print(m)
                    self.testInfo[0]["msg"] = m
                    break
        else:
            result = False
        return result
