import datetime
import subprocess
import time

import cv2

from game.logutils.mylog import log
from game.nanman.fightNm import fightNanman
from game.utils.tools import getNum, takeList, chuzheng, take_pic,check_pic,touch


def fightHuangjin(id,fnm,waitWuKao,wuKaoDate,exNMIds):
    time_now=datetime.datetime.now()
    day_now=time_now.day
    if int(waitWuKao) and day_now!=int(wuKaoDate):
        cost=fightNanman(id,fnm,exNMIds)
        log("攻打南蛮后耗时cost:{}".format(cost))
        if cost is None or cost==0:
            cost=300
        return cost
    a=0
    hjText=getNum(id,2)
    if len(hjText)==1:
        hjNum=int(hjText[0])
    if len(hjText)==2:
        hjNum=int(hjText[0])*10 + int(hjText[1])
    # if hjNum ==0:
    if hjNum <6:
        cost=fightNanman(id,fnm,exNMIds)
        log("攻打南蛮后耗时cost:{}".format(cost))
        if cost is None or cost==0:
            cost=300
        return cost
    #点击黄巾
    r=takeList(666,1144,id)
    if not(r is None) and r==-1:
        return -1
    time.sleep(1)
    c=0
    while True:
        tfImg=take_pic(id)
        fightImg=tfImg[1372:1461,374:695]
        cv2.imwrite("fightHJ/tmp.png",fightImg)
        fightImg=cv2.imread("fightHJ/tmp.png",0)
        factFight=cv2.imread("fightHJ/fight.png",0)
        dx=check_pic(fightImg,factFight)
        log("黄巾前往歼敌的偏差：{}".format(dx))
        if dx <10000 :
            break
        else:
            time.sleep(1)
            c+=1
        if c>20:
            log("攻打黄巾超时，失败")
            break
    touch(id,410, 1402)
    time.sleep(1)
    r=chuzheng(id)
    log("攻打黄巾出征cost:{}".format(r))
    if not(r is None) and r==-1:
        return -1
    time.sleep(0.3)
    cost2=fightNanman(id,fnm,exNMIds)
    if cost2==-1:
        return -1
    cost=r-cost2
    log("攻打南蛮后剩余黄巾出征cost:{}".format(cost))
    return cost if cost > 0 else 0
