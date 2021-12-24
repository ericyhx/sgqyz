import subprocess
import time

import cv2
import numpy as np

from game.logutils.mylog import log
from game.utils.tools import chuzheng, processEx, reStartDnplayer


def checkLiuKou(device: int):
    ret=fightLiuKou(device)
    if ret==-1:
        log("攻打流寇时出错")
        processEx(device)
    elif ret==0:
        log("暂时不存在流寇")
    else:
        log("攻打流程耗时：{}".format(ret))
        time.sleep(ret)


def fightLiuKou(device: int):
    a=0
    while subprocess.call("adb -s emulator-{} exec-out screencap -p > liukou/temp.png".format(device),shell=True):
        time.sleep(1)
        a+=1
        if a >5:
            log("=====================重新启动雷电模拟器3=====================")
            # reStartDnplayer()
            return -1
        True
    lk=cv2.imread("liukou/temp.png")
    lkTag=lk[1365:1410,967:1020]
    cv2.imwrite("liukou/temp.png",lkTag)
    curlk=cv2.imread("liukou/temp.png",0)
    factLk=cv2.imread("liukou/liukou.png",0)
    ret,curlk = cv2.threshold(curlk,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
    ret,factLk = cv2.threshold(factLk,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
    dx=(curlk-factLk).sum()
    log("流寇按钮偏差：{}".format(dx))
    if dx <2000:
        # 点击流寇
        subprocess.call("adb -s emulator-{} shell input tap 993 1385".format(device),shell=True)
        time.sleep(2)
        res=getQianWangLoc(device)
        log("歼灭流寇的坐标：{}".format(res))
        if len(res) ==2:
            subprocess.call("adb -s emulator-{} shell input tap {} {}".format(device,res[0],res[1]-90),shell=True)
            time.sleep(1)
        c=0
        while True:
            a=0
            while subprocess.call("adb -s emulator-{} exec-out screencap -p > liukou/temp.png".format(device),shell=True):
                time.sleep(1)
                a+=1
                if a >5:
                    log("=====================重新启动雷电模拟器4=====================")
                    # reStartDnplayer()
                    return -1
                True
            lk=cv2.imread("liukou/temp.png")
            cz=lk[1307:1401,374:707]
            cv2.imwrite("liukou/temp.png",cz)
            cz=cv2.imread("liukou/temp.png",0)
            factCz=cv2.imread("liukou/liukouCZ.png",0)
            ret,cz = cv2.threshold(cz,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
            ret,factCz = cv2.threshold(factCz,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
            dx=(cz-factCz).sum()
            log("流寇出征偏差：{}".format(dx))
            if dx <1000:
                subprocess.call("adb -s emulator-{} shell input tap 534 1348".format(device),shell=True)
                time.sleep(1)
                ret=chuzheng(device)
                if ret==180:
                    ret=10
                return ret
            else:
                c+=1
                time.sleep(1)
            if c>10:
                log("获取流程出征按钮超时")
                a=0
                while subprocess.call("adb -s emulator-{} exec-out screencap -p > liukou/exception.png".format(device),shell=True):
                    time.sleep(1)
                    a+=1
                    if a >5:
                        log("=====================重新启动雷电模拟器5=====================")
                        # reStartDnplayer()
                        return -1
                    True
                return -1
    return 0


def getQianWangLoc(device: int):
    a=0
    while subprocess.call("adb -s emulator-{} exec-out screencap -p > liukou/temp.png".format(device),shell=True):
        time.sleep(1)
        a+=1
        if a >5:
            log("=====================重新启动雷电模拟器1=====================")
            # reStartDnplayer()
            return -1
        True
    gray=cv2.imread("liukou/temp.png",0)
    img2=cv2.imread("liukou/jiandi.png",0)

    threshold = 0.99
    res=cv2.matchTemplate(gray,img2,cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    pt = loc[::-1]
    if len(pt[0])>0 and len(pt[1])>0:
        tx=pt[0][0]+105
        ty=pt[1][0]+90
        return [tx,ty]
    else:
        log('未找到目标区域,返回默认值')
        return []