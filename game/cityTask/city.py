import math
import subprocess
import time

import cv2

from game.logutils.mylog import log
from game.utils.tools import reStartDnplayer


def doTask(device: int):
    # return 0
    start=time.time()
    a=0
    while subprocess.call("adb -s emulator-{} exec-out screencap -p > cityTask/temp.png".format(device),shell=True):
        time.sleep(0.3)
        a+=1
        if a >5:
            log("=====================重新启动雷电模拟器6=====================")
            # reStartDnplayer()
            return -1
        True
    lianmeng=cv2.imread("cityTask/temp.png")
    lianmeng=lianmeng[1795:1889,936:1036]
    cv2.imwrite("cityTask/temp.png",lianmeng)
    lm=cv2.imread("cityTask/temp.png",0)
    factLm=cv2.imread("cityTask/lianmeng.png",0)
    ret,lm = cv2.threshold(lm,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
    ret,factLm = cv2.threshold(factLm,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
    dx=(lm-factLm).sum()
    log("联盟按钮的偏差：{}".format(dx))
    if dx <300000:
        #点击联盟
        subprocess.call("adb -s emulator-{} shell input tap 986 1832".format(device),shell=True)
        time.sleep(1)
        #点击主页
        subprocess.call("adb -s emulator-{} shell input tap 216 1847".format(device),shell=True)
        time.sleep(1)
        subprocess.call("adb -s emulator-{} shell input tap 216 1847".format(device),shell=True)
        time.sleep(1)
        #点击联盟城市
        subprocess.call("adb -s emulator-{} shell input tap 838 925".format(device),shell=True)
        time.sleep(1)
        #判断城市任务
        c=0
        while True:
            a=0
            while subprocess.call("adb -s emulator-{} exec-out screencap -p > cityTask/temp.png".format(device),shell=True):
                time.sleep(0.3)
                a+=1
                if a >5:
                    log("=====================重新启动雷电模拟器7=====================")
                    # reStartDnplayer()
                    return -1
                True
            task=cv2.imread("cityTask/temp.png")
            task=task[1771:1865,626:959]
            cv2.imwrite("cityTask/temp.png",task)
            task=cv2.imread("cityTask/temp.png",0)
            oneKey=cv2.imread("cityTask/oneKey.png",0)
            ret,task = cv2.threshold(task,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
            ret,oneKey = cv2.threshold(oneKey,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
            dx=(task-oneKey).sum()
            log("一键执行按钮的偏差：{}".format(dx))
            if dx <100000:
                #点击一键执行
                subprocess.call("adb -s emulator-{} shell input tap 771 1822".format(device),shell=True)
                time.sleep(1)
                subprocess.call("adb -s emulator-{} shell input tap 771 1822".format(device),shell=True)
                time.sleep(1)
                subprocess.call("adb -s emulator-{} shell input tap 771 1822".format(device),shell=True)
                time.sleep(1)
                subprocess.call("adb -s emulator-{} shell input tap 58 47".format(device),shell=True)
                time.sleep(1)
                subprocess.call("adb -s emulator-{} shell input tap 58 47".format(device),shell=True)
                time.sleep(1)
                end=time.time()
                return math.floor(end-start)
            else:
                c+=1
                time.sleep(1)
            if c >10:
                return -1
    else:
        return -1