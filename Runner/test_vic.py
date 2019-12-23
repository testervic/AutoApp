# -*- coding: utf-8 -*-
import os
from appium import webdriver
import time
coordinates = {
    '1080p': {
    '首页_+': (548, 1839),
    '登录页_邮箱图标': (147, 1802),
    '登录页_邮箱地址': (264, 370),
    '登录页_邮箱密码': (264, 570),
    '登录页_登录按钮': (264, 780),
    }, '720p': {
    '首页_+': (640, 1250),
    '登录页_邮箱图标': (147, 1802),
    '登录页_邮箱地址': (264, 370),
    '登录页_邮箱密码': (264, 570),
    '登录页_登录按钮': (264, 570),
    }
}
cfg_phone_resolution = '1080p'

desired_caps = {}
desired_caps['platformName'] = 'Android'  # 测试平台
desired_caps['platformVersion'] = '6.0.1'  # 平台版本,不能写错
desired_caps['deviceName'] = 'emulator-5554'  # 设备名称，多设备时需区分
# desired_caps['app'] = r'd:\apk\toutiao.apk'
desired_caps['appPackage'] = 'com.jm.video'  # app package名
desired_caps['appActivity'] = '.ui.main.SplashActivity'  # app默认Activity
desired_caps['unicodeKeyboard'] = True  # 一定要有该参数，否则unicode 输入的中文无效
desired_caps['noReset'] = True
desired_caps['newCommandTimeout'] = 6000
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)  # 启动Remote RPC
driver.implicitly_wait(10)
print(driver.session_id)
# 不得不用sleep
screen_width = driver.get_window_size()['width']  # 获取当前屏幕的宽
screen_height = driver.get_window_size()['height']  # 获取当前屏幕的高
print(screen_width)
print(screen_height)
time.sleep(5)
#cmd = "adb -s emulator-5554 shell input tap 620 110"
os.system('adb -s emulator-5554 shell input tap 660 110')
time.sleep(5)
os.system('adb -s emulator-5554 shell input tap 140 100')
time.sleep(5)
os.system('adb shell ime set com.android.adbkeyboard/.AdbIME')
#os.system('adb shell am broadcast -a ADB_INPUT_TEXT --es msg '上海'\')
os.system("adb shell am broadcast -a ADB_INPUT_TEXT --es msg '上海'")
os.system("adb shell am broadcast -a ADB_INPUT_TEXT --es msg '上海'")
#driver.tap([(622,62),(710,150)], 300)
# time.sleep(10)
# #
# # coordinate = coordinates[cfg_phone_resolution]
# # driver.tap([coordinate['首页_+']], 300)
# # time.sleep(2)
# # driver.tap([coordinate['登录页_邮箱图标']], 300)
# # time.sleep(1)
# # driver.tap([coordinate['登录页_邮箱地址']], 300)
# # time.sleep(1)
# # # 没有WebElement对象 ，如何输入字符？
# # # adb shell input text "<your string>"
# # import os
# # os.system('adb shell input text "qqqqrss@163.com"')
# # #注意，如果要输入中文，需要下载一个adb键盘应用，
# # # 参考 https://blog.csdn.net/slimboy123/article/details/54140029
# # time.sleep(1)
# # driver.tap([coordinate['登录页_邮箱密码']], 300)
# # time.sleep(1)
# # os.system('adb shell input text "sdqwefsdf"')
# # driver.tap([coordinate['登录页_登录按钮']], 300)
# # input('**** Press to quit..')
# driver.quit()
