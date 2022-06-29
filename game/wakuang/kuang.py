import subprocess
import time

import cv2

from game.logutils.mylog import log
from game.tufei.fightTf import fightTF
from game.utils.tools import getNum, takeList, chuzheng, searchBtn, reStartDnplayer


def wakuang(device,fnm,waitWuKao,wuKaoDate):
    ret=searchBtn(device)
    if ret:
        text=getNum(0,device)
        if len(text) ==1:
            kdCnt=int(text[0])
            if kdCnt >0:
                #点击矿洞
                r=takeList(183,1137,0,device)
                if not(r is None) and r==-1:
                    return -1
                r=goCaiji(device)
                if not(r is None) and r==-1:
                    return -1
                r=chuzheng(device)
                if r is None:
                    r=0
                return r
            elif kdCnt ==0:
                #跳转到土匪
                return fightTF(device,fnm,waitWuKao,wuKaoDate)
            else:
                log("矿洞获取有误")
                return -1
        else:
            log("不满足挖矿条件")
            return -1
    else:
        return -1
#点击采集按钮
def goCaiji(device: int):
    c=0
    while True:
        a=0
        while subprocess.call("adb -s emulator-{} exec-out screencap -p > wakuang/main.png".format(device),shell=True):
            time.sleep(1)
            a+=1
            if a >5:
                log("=====================重新启动雷电模拟器11=====================")
                # reStartDnplayer()
                return -1
            True
        mainImg=cv2.imread("wakuang/main.png")
        caiji=mainImg[1129:1221,660:740]
        cv2.imwrite("wakuang/temp.png",caiji)
        factCaiji=cv2.imread("wakuang/caiji.png",0)
        caiji=cv2.imread("wakuang/temp.png",0)
        ret,factCaiji = cv2.threshold(factCaiji,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
        ret,caiji = cv2.threshold(caiji,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
        dx=(caiji-factCaiji).sum()
        log("采集的偏差：{}".format(dx))
        if dx <100000:
            subprocess.call("adb -s emulator-{} shell input tap 695 1178".format(device),shell=True)
            return 0
        else:
            time.sleep(1)
            c+=1
        if c > 20:
            log("跳转采集出错")
            return -1



def singleWK(device):
    ret=searchBtn(device)
    if ret:
        text=getNum(0,device)
        if len(text) ==1:
            kdCnt=int(text[0])
            if kdCnt >0:
                #点击矿洞
                r=takeList(183,1137,0,device)
                if not(r is None) and r==-1:
                    return -1
                r=goCaiji(device)
                if not(r is None) and r==-1:
                    return -1
                r=chuzheng(device)
                if r is None:
                    r=0
                return r
            elif kdCnt ==0:
                #结束
                return -1
            else:
                log("矿洞获取有误")
                return -1
        else:
            log("不满足挖矿条件")
            return -1
    else:
        return -1