import subprocess
import time

import cv2

from game.logutils.mylog import log
from game.tufei.fightTf import fightTF
from game.utils.tools import getNum, takeList, chuzheng, searchBtn,take_pic,check_pic,touch


def wakuang(id,fnm,waitWuKao,wuKaoDate,exNMIds):
    ret=searchBtn(id)
    if ret:
        text=getNum(id,0)
        if len(text) ==1:
            kdCnt=int(text[0])
            if kdCnt >0:
                #点击矿洞
                r=takeList(183,1137,id)
                if not(r is None) and r==-1:
                    return -1
                r=goCaiji(id)
                if not(r is None) and r==-1:
                    return -1
                r=chuzheng(id)
                if r is None:
                    r=0
                return r
            elif kdCnt ==0:
                #跳转到土匪
                return fightTF(id,fnm,waitWuKao,wuKaoDate,exNMIds)
            else:
                log("矿洞获取有误")
                return -1
        else:
            log("不满足挖矿条件")
            return -1
    else:
        return -1
#点击采集按钮
def goCaiji(id: int):
    c=0
    while True:
        mainImg=take_pic(id)
        caiji=mainImg[1129:1221,660:740]
        cv2.imwrite("wakuang/temp.png",caiji)
        factCaiji=cv2.imread("wakuang/caiji.png",0)
        caiji=cv2.imread("wakuang/temp.png",0)
        dx=check_pic(caiji,factCaiji)
        log("采集的偏差：{}".format(dx))
        if dx <100000:
            touch(id,695, 1178)
            return 0
        else:
            time.sleep(1)
            c+=1
        if c > 10:
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
