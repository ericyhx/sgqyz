import datetime
import subprocess
import time

import cv2
import numpy as np

from game.logutils.mylog import log
from game.utils.tools import chuzheng, processEx,take_pic,check_pic,touch


def checkLiuKou(id,waitWuKao,wuKaoDate):
    ret=fightLiuKou(id,waitWuKao,wuKaoDate)
    if ret==-1:
        log("攻打流寇时出错")
        processEx(id)
    elif ret==0:
        log("暂时不存在流寇")
    else:
        log("攻打流程耗时：{}".format(ret))
        time.sleep(ret)


def fightLiuKou(id,waitWuKao,wuKaoDate):
    time_now=datetime.datetime.now()
    day_now=time_now.day
    if int(waitWuKao) and day_now!=int(wuKaoDate):
        return 0
    lk=take_pic(id)
    lkTag=lk[1365:1410,967:1020]
    cv2.imwrite("liukou/temp.png",lkTag)
    curlk=cv2.imread("liukou/temp.png",0)
    factLk=cv2.imread("liukou/liukou.png",0)
    dx=check_pic(curlk,factLk)
    log("流寇按钮偏差：{}".format(dx))
    if dx <2000:
        # 点击流寇
        touch(id,993, 1385)
        time.sleep(2)
        res=getQianWangLoc(id)
        log("歼灭流寇的坐标：{}".format(res))
        if len(res) ==2:
            touch(id,res[0],res[1]-90)
            time.sleep(1)
        c=0
        while True:
            lk=take_pic(id)
            cz=lk[1307:1401,374:707]
            cv2.imwrite("liukou/temp.png",cz)
            cz=cv2.imread("liukou/temp.png",0)
            factCz=cv2.imread("liukou/liukouCZ.png",0)
            dx=check_pic(cz,factCz)
            log("流寇出征偏差：{}".format(dx))
            if dx <100000:
                touch(id,534, 1348)
                time.sleep(0.3)
                ret=chuzheng(id)
                if ret==180:
                    ret=10
                return ret
            else:
                c+=1
                time.sleep(1)
            if c>10:
                log("获取流程出征按钮超时")
                return -1
    return 0


def getQianWangLoc(id: int):
    gray=take_pic(id)
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