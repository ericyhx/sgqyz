import subprocess
import time
import datetime

import cv2
from PIL import Image
from pytesseract import pytesseract

from game.logutils.mylog import log
from game.fightHJ.fightHJ import fightHuangjin
from game.nanman.fightNm import fightNanman
from game.utils.tools import getNum, takeList, chuzheng, reStartDnplayer

fightTime=0
def fightTF(device: int,fnm: int):
    # a=0
    # while subprocess.call("adb -s emulator-5554 exec-out screencap -p > tufei/main.png",shell=True):
    #     time.sleep(1)
    #     a+=1
    #     if a >5:
    #         log("=====================重新启动雷电模拟器1=====================")
    #         # reStartDnplayer()
    #         return -1
    #     True
    tfNum=0

    time_now=datetime.datetime.now()
    hour_now=time_now.hour
    if hour_now < 3:
        tfNum=0
    else:
        tfText=getNum(1,device)
        if len(tfText)==1:
            tfNum=int(tfText[0])
        if len(tfText)==2:
            tfNum=int(tfText[0])*10 + int(tfText[1])
    if tfNum > 0:
        #点击土匪
        r=takeList(426,1144,1,device)
        if not (r is None) and r==-1:
            return -1
        c=0
        while True:
            a=0
            while subprocess.call("adb -s emulator-{} exec-out screencap -p > tufei/main.png".format(device),shell=True):
                time.sleep(1)
                a+=1
                if a >5:
                    log("=====================重新启动雷电模拟器1=====================")
                    # reStartDnplayer()
                    return -1
                True
            tfImg=cv2.imread("tufei/main.png")
            fightImg=tfImg[1321:1407,374:695]
            cv2.imwrite("tufei/tmp.png",fightImg)
            fightImg=cv2.imread("tufei/tmp.png",0)
            factFight=cv2.imread("tufei/fight.png",0)
            ret,fightImg = cv2.threshold(fightImg,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
            ret,factFight = cv2.threshold(factFight,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
            dx=(fightImg-factFight).sum()
            log("前往歼敌的偏差：{}".format(dx))
            if dx <10000 :
                break
            else:
                time.sleep(1)
                c+=1
            if c>20:
                log("攻打土匪超时，失败")
                return -1
        buf=tfImg[1209:1251,480:599]
        cv2.imwrite("tufei/tfBuf.png",buf)
        text = pytesseract.image_to_string(Image.open("tufei/tfBuf.png"),lang="eng",config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789/')
        text=text.strip().replace("\n","")
        l=len(text)
        xg=text[l-2]
        if xg is "/":
            num=int(text[l-1])
        else:
            num=int(text[l-1])+int(text[l-2])*10
        if num <12:
            subprocess.call("adb -s emulator-{} shell input tap 734 1232".format(device),shell=True)
            time.sleep(1)
            for i in range (11-num):
                subprocess.call("adb -s emulator-{} shell input tap 844 975".format(device),shell=True)
                time.sleep(1)
            subprocess.call("adb -s emulator-{} shell input tap 646 1205".format(device),shell=True)
            time.sleep(1)
        subprocess.call("adb -s emulator-{} shell input tap 440 1368".format(device),shell=True)
        time.sleep(1)
        fightTime=chuzheng(device)
        log("土匪出征cost:{}".format(fightTime))
        if -1 == fightTime:
            return -1
        time.sleep(2)
        cost2=fightNanman(device,fnm)
        if cost2==-1:
            return -1
        cost=fightTime-cost2
        log("攻打南蛮后剩余出征cost:{}".format(cost))
        return cost if cost > 0 else 0
    else:
        #攻打黄巾
        return fightHuangjin(device,fnm)