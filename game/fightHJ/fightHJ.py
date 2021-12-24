import subprocess
import time

import cv2

from game.logutils.mylog import log
from game.nanman.fightNm import fightNanman
from game.utils.tools import getNum, takeList, chuzheng, reStartDnplayer


def fightHuangjin(device: int,fnm: int):
    a=0
    while subprocess.call("adb -s emulator-{} exec-out screencap -p > fightHJ/main.png".format(device),shell=True):
        time.sleep(1)
        a+=1
        if a >5:
            log("=====================重新启动雷电模拟器1=====================")
            # reStartDnplayer()
            return -1
        True
    hjText=getNum(2,device)
    if len(hjText)==1:
        hjNum=int(hjText[0])
    if len(hjText)==2:
        hjNum=int(hjText[0])*10 + int(hjText[1])
    # if hjNum ==0:
    if hjNum <6:
        cost=fightNanman(device,fnm)
        log("攻打南蛮后耗时cost:{}".format(cost))
        if cost is None or cost==0:
            cost=300
        return cost
    #点击黄巾
    r=takeList(666,1144,1,device)
    if not(r is None) and r==-1:
        return -1
    time.sleep(1)
    c=0
    while True:
        a=0
        while subprocess.call("adb -s emulator-{} exec-out screencap -p > fightHJ/main.png".format(device),shell=True):
            time.sleep(1)
            a+=1
            if a >5:
                log("=====================重新启动雷电模拟器1=====================")
                # reStartDnplayer()
                return -1
            True
        tfImg=cv2.imread("fightHJ/main.png")
        fightImg=tfImg[1372:1461,374:695]
        cv2.imwrite("fightHJ/tmp.png",fightImg)
        fightImg=cv2.imread("fightHJ/tmp.png",0)
        factFight=cv2.imread("fightHJ/fight.png",0)
        ret,fightImg = cv2.threshold(fightImg,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
        ret,factFight = cv2.threshold(factFight,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
        dx=(fightImg-factFight).sum()
        log("黄巾前往歼敌的偏差：{}".format(dx))
        if dx <10000 :
            break
        else:
            time.sleep(1)
            c+=1
        if c>20:
            log("攻打黄巾超时，失败")
            break
    subprocess.call("adb -s emulator-{} shell input tap 410 1402".format(device),shell=True)
    time.sleep(1)
    r=chuzheng(device)
    log("攻打黄巾出征cost:{}".format(r))
    if not(r is None) and r==-1:
        return -1
    time.sleep(2)
    cost2=fightNanman(device,fnm)
    if cost2==-1:
        return -1
    cost=r-cost2
    log("攻打南蛮后剩余黄巾出征cost:{}".format(cost))
    return cost if cost > 0 else 0