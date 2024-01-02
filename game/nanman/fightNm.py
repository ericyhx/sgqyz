import math
import subprocess
import time

import cv2

from game.logutils.mylog import log
from game.utils.tools import getNum, takeList, chuzheng, searchBtn,take_pic,check_pic,touch


def yaoqingzhuchengBtn(n,id):
    c=0
    while True:
        zzlist=take_pic(id)
        zz=zzlist[11:75,421:654]
        factzz=cv2.imread("nanman/zhuzhenliebiao.png",0)
        dx=check_pic(zz,factzz)
        log("南蛮前往邀请助阵按钮偏差：{}".format(dx))
        if dx<100000 or dx==278829:
            return 0
        else:
            time.sleep(1)
            c+=1
        if c >n:
            log("请求助阵列表界面错误，超时")
            return -1


def fightNanman(id: int,fnm: int,exNMIds):
    if not int(fnm) or id in exNMIds:
    # 用于暂停南蛮
        touch(id,855, 58)
        time.sleep(1)
        return 0


    # t=datetime.now()
    # if t.day<24:
    #     return 0
    start=time.time()
    ret=searchBtn(id)
    if ret:
        nmText=getNum(id,3)
        nmNum=0
        if len(nmText)==1:
            nmNum=int(nmText[0])
        if len(nmText)==2:
            nmNum=int(nmText[0])*10 + int(nmText[1])
        if nmNum ==1 or nmNum ==0:
            touch(id,855, 58)
            return 0
        # check南蛮
        # wkTag=imgs[1101:1191,131:248]
        # tfTag=imgs[1101:1191,368:489]
        # hjTag=imgs[1101:1191,604:723]
        # nmTag=imgs[1101:1191,839:967]
        #点击南蛮
        r=takeList(902,1142,id)
        if not(r is None) and r==-1:
            return -1
        time.sleep(1)
        #发起南蛮集结
        c=0
        while True:
            jijieImg=take_pic(id)
            jijie=jijieImg[1274:1365,374:702]
            cv2.imwrite("nanman/temp.png",jijie)
            jiie=cv2.imread("nanman/temp.png",0)
            factJijie=cv2.imread("nanman/jijie.png",0)
            dx=check_pic(jiie,factJijie)
            log("发起集结按钮偏差：{}".format(dx))
            if dx <3000:
                # 点击集结
                touch(id,538, 1319)
                time.sleep(1)
                c=0
                while c<2:
                    c+=1
                    msg=take_pic(id)
                    msg=msg[627:1284,70:1000]
                    cv2.imwrite("nanman/temp.png",msg)
                    msg=cv2.imread("nanman/temp.png",0)
                    msg1=cv2.imread("nanman/msg1.png",0)
                    msg2=cv2.imread("nanman/msg2.png",0)
                    dx1=check_pic(msg,msg1)
                    dx2=check_pic(msg,msg2)
                    log("南蛮发起集结前的兵力提示偏差：{}：{}".format(dx1,dx2))
                    if dx2 <60000:
                        # 选择本次登录不在显示
                        touch(id,596, 1052)
                        time.sleep(1)
                        touch(id, 698, 1201)
                        time.sleep(1)
                        break
                    if dx1 <60000:
                        touch(id,698, 1201)
                        time.sleep(1)
                        break
                    time.sleep(1)
                c=0
                while c<2:
                    c+=1
                    msg=take_pic(id)
                    msg=msg[627:1284,70:1000]
                    cv2.imwrite("nanman/temp.png",msg)
                    msg=cv2.imread("nanman/temp.png",0)
                    msg4=cv2.imread("nanman/msg4.png",0)
                    dx4=check_pic(msg,msg4)
                    log("南蛮发起集结前的其他人提示偏差：{}".format(dx4))
                    if dx4 <60000:
                        touch(id,698, 1201)
                        time.sleep(1)
                        break
                    time.sleep(1)
                c=0
                while c<3:
                    c+=1
                    msg=take_pic(id)
                    msg=msg[692:1289,74:998]
                    cv2.imwrite("nanman/temp.png",msg)
                    msg=cv2.imread("nanman/temp.png",0)
                    msg3=cv2.imread("nanman/msg3.png",0)
                    dx=check_pic(msg,msg3)
                    log("南蛮发起集结前目标丢失的提示偏差：{}".format(dx4))
                    if dx <80000:
                        # 选择本次登录不在显示
                        touch(id,596, 1052)
                        time.sleep(1)
                        touch(id,698, 1201)
                        break
                    time.sleep(1)
                break

            else:
                time.sleep(1)
                c+=1
            if c >30:
                log("集结界面错误，超时")
                return -1
        #前往编队
        c=0
        while True:
            bdImg=take_pic(id)
            bd=bdImg[1528:1623,370:704]
            jijieLoc=bdImg[1408:1472,160:458]
            cv2.imwrite("nanman/jiijeLoc0.png",jijieLoc)
            cv2.imwrite("nanman/temp.png",bd)
            bd=cv2.imread("nanman/temp.png",0)
            factBd=cv2.imread("nanman/biandui.png",0)
            dx=check_pic(bd,factBd)
            jiijeLoc0=cv2.imread("nanman/jiijeLoc0.png",0)
            jiijeLoc=cv2.imread("nanman/jiijeLoc.png",0)
            jijieDx=check_pic(jiijeLoc0,jiijeLoc)
            log("南蛮前往编队按钮的偏差：{},集结点偏差：{}".format(dx,jijieDx))
            if dx <5000 and jijieDx <50000:
                touch(id,527, 1578)
                time.sleep(1)
                break
            else:
                time.sleep(1)
                c+=1
            if c >10:
                log("南蛮前往编队按钮界面错误，超时")
                return -1
        cost=chuzheng(id)
        log(cost)
        if cost==-1:
            return -1
        time.sleep(1)
        touch(id,370, 992)
        time.sleep(2)
        #邀请助阵
        # re=yaoqingzhuchengBtn(10,id)
        # if re==-1:
        #     return -1
        # a=0
        yqimg=take_pic(id)
        yq=yqimg[751:820,799:1002]
        cv2.imwrite("nanman/temp.png",yq)
        yq=cv2.imread("nanman/temp.png",0)
        factyq=cv2.imread("nanman/yaoqing.png",0)
        dx=check_pic(yq,factyq)
        log("邀请助阵按钮的偏差：{}".format(dx))
        if dx<50000:
            touch(id,887, 794)
            time.sleep(6)
            touch(id,55, 48)
            time.sleep(1)
        else:
            touch(id,55, 48)
            time.sleep(1)
            touch(id,975, 625)
            time.sleep(1)
            touch(id,715, 1198)
        end=time.time()
        return math.floor(end-start)
    else:
        return -1
