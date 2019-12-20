# -*- coding: utf-8 -*-
import sys

sys.path.append("..")
import platform
from Base.BaseAndroidPhone import *
from Base.BaseAdb import *
from Base.BaseRunner import ParametrizedTestCase
from TestCase.HomeTest import HomeTest
from Base.BaseAppiumServer import AppiumServer
from multiprocessing import Pool
import unittest
from Base.BaseInit import init, mk_file
from Base.BaseStatistics import *
from Base.BasePickle import *
from datetime import datetime
from Base.BaseApk import ApkInfo
from Base.BaseEmail import *
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)
import time
now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime())
now2 = time.strftime("%Y-%m-%d", time.localtime())
def kill_adb():
    if platform.system() == "Windows":
        # os.popen("taskkill /f /im adb.exe")
        os.system(PATH("../app/kill5037.bat"))
    else:
        os.popen("killall adb")
    os.system("adb start-server")

def runnerPool(getDevices):
    devices_Pool = []

    for i in range(0, len(getDevices)):
        _pool = []
        _initApp = {}
        _initApp["deviceName"] = getDevices[i]["devices"]
        _initApp["platformVersion"] = getPhoneInfo(devices=_initApp["deviceName"])["release"]
        _initApp["platformName"] = "android"
        _initApp["port"] = getDevices[i]["port"]
        _initApp["automationName"] = "uiautomator2"
        _initApp["systemPort"] = getDevices[i]["systemPort"]

        _initApp["app"] = getDevices[i]["app"]
        apkInfo = ApkInfo(_initApp["app"])
        #_initApp["appPackage"] = apkInfo.getApkBaseInfo()[0]
        #_initApp["appPackage"] = " test.joko.com.myapplication"
        #_initApp["appActivity"] = apkInfo.getApkActivity()
        #_initApp["appActivity"] = ".welcome"
        _pool.append(_initApp)
        devices_Pool.append(_initApp)

    pool = Pool(len(devices_Pool))
    pool.map(runnerCaseApp, devices_Pool)
    pool.close()
    pool.join()


def runnerCaseApp(devices):
    starttime = datetime.now()
    suite = unittest.TestSuite()
    suite.addTest(ParametrizedTestCase.parametrize(HomeTest, param=devices))
    # suite.addTest(ParametrizedTestCase.parametrize(HomeTest, param=devices)) #加入测试类
    unittest.TextTestRunner(verbosity=2).run(suite)
    endtime = datetime.now()
    countDate(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str((endtime - starttime).seconds) + "秒")



def runner():
    i=1
    while True:
        kill_adb()
        devicess = AndroidDebugBridge().attached_devices()
        if len(devicess) > 0:
            mk_file()
            l_devices = []
            for dev in devicess:
                app = {}
                app["devices"] = dev
                init(dev)
                app["port"] = str(random.randint(4700, 4900))
                app["bport"] = str(random.randint(4700, 4900))
                app["systemPort"] = str(random.randint(4700, 4900))
                app["app"] = PATH("../app/com.jm.android.jumei_8.601_8601.apk") # 测试的app路径
                #app["app"] = "/Users/vic/work/WORK/Work/Py_script/appium-master/app/android-system-webview-60.apk"  # 测试的app路径,喜马拉雅app
                l_devices.append(app)

            appium_server = AppiumServer(l_devices)
            appium_server.start_server()
            #print(l_devices)
            runnerPool(l_devices)
            writeExcel()
            filepath = PATH("../Report/ReportDetail.xlsx")
            excel_to_html(filepath)
            appium_server.stop_server(l_devices)
            data = getData()
            if data["pass"] >0:
                print("执行成功，发送邮件")
                isSend()
                break
            else:
                time.sleep(5)
                i+=1
                if i==4:
                    print("执行失败")
                    break
                print("执行失败重试三次，第" + str(i) + "次......")
        else:
            print("没有可用的安卓设备")
            break