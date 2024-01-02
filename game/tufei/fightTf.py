import subprocess
import time
import datetime

import cv2
from PIL import Image
from pytesseract import pytesseract

from game.logutils.mylog import log
from game.fightHJ.fightHJ import fightHuangjin
from game.nanman.fightNm import fightNanman
from game.utils.tools import getNum, takeList, chuzheng, take_pic,check_pic,touch,searchBtn

fightTime=0
def fightTF(id,fnm,waitWuKao,wuKaoDate,exNMIds):
    tfNum=0
    time_now=datetime.datetime.now()
    hour_now=time_now.hour
    if hour_now < -1:
        tfNum=0
    else:
        tfText=getNum(id,1)
        if len(tfText)==1:
            tfNum=int(tfText[0])
        if len(tfText)==2:
            tfNum=int(tfText[0])*10 + int(tfText[1])
    if tfNum > 0:
        #点击土匪
        r=takeList(426,1144,id)
        if not (r is None) and r==-1:
            return -1
        c=0
        while True:
            time.sleep(2)
            tfImg=take_pic(id)
            fightImg=tfImg[1321:1407,374:695]
            cv2.imwrite("tufei/tmp.png",fightImg)
            fightImg=cv2.imread("tufei/tmp.png",0)
            factFight=cv2.imread("tufei/fight.png",0)
            dx=check_pic(fightImg,factFight)
            log("前往歼敌的偏差：{}".format(dx))
            if dx <100000 :
                break
            else:
                time.sleep(1)
                c+=1
            if c>20:
                log("攻打土匪超时，失败")
                return -1
        buf=tfImg[1209:1251,480:599]
        text = pytesseract.image_to_string(Image.fromarray(buf),lang="eng",config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789/')
        text=text.strip().replace("\n","")
        l=len(text)
        xg=text[l-2]
        if xg == "/":
            num=int(text[l-1])
        else:
            num=int(text[l-1])+int(text[l-2])*10
        if num <12:
            touch(id,734, 1232)
            time.sleep(1)
            for i in range (11-num):
                touch(id, 844, 975)
                time.sleep(1)
            touch(id,646, 1205)
            time.sleep(1)
        touch(id,440, 1368)
        time.sleep(1)
        fightTime=chuzheng(id)
        log("土匪出征cost:{}".format(fightTime))
        if -1 == fightTime:
            return -1
        time.sleep(0.3)
        ret = searchBtn(id)
        if not ret:
            return -1
        cost2=fightHuangjin(id, fnm, waitWuKao, wuKaoDate,exNMIds)
        log("攻打黄巾、南蛮后剩余出征cost:{}".format(cost2))
        if cost2==-1:
            return -1
        cost=fightTime-cost2
        log("打野完成后剩余出征cost:{}".format(cost))
        return fightTime if cost > 0 else cost2
    else:
        #攻打黄巾
        return fightHuangjin(id,fnm,waitWuKao,wuKaoDate,exNMIds)
