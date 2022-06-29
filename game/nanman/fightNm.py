import math
import subprocess
import time

import cv2

from game.logutils.mylog import log
# from game.startGame import cf
from game.utils.tools import getNum, takeList, chuzheng, searchBtn


def yaoqingzhuchengBtn(n,device):
    c=0
    while True:
        a=0
        while subprocess.call("adb -s emulator-{} exec-out screencap -p > nanman/temp.png".format(device),shell=True):
            time.sleep(1)
            a+=1
            if a >5:
                log("=====================重新启动雷电模拟器1=====================")
                # reStartDnplayer()
            return -1
            True
        zzlist=cv2.imread("nanman/temp.png")
        zz=zzlist[11:75,421:654]
        cv2.imwrite("nanman/temp.png",zz)
        zz=cv2.imread("nanman/temp.png",0)
        factzz=cv2.imread("nanman/zhuzhenliebiao.png",0)
        ret,zz = cv2.threshold(zz,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
        ret,factzz = cv2.threshold(factzz,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
        dx=(zz-factzz).sum()
        log("南蛮前往邀请助阵按钮偏差：{}".format(dx))
        if dx<100000 or dx==278829:
            return 0
        else:
            time.sleep(1)
            c+=1
        if c >n:
            log("请求助阵列表界面错误，超时")
            return -1


def fightNanman(device: int,fnm: int):
    if not int(fnm):
    # 用于暂停南蛮
        subprocess.call("adb -s emulator-{} shell input tap 855 58".format(device),shell=True)
        time.sleep(1)
        return 0


    # t=datetime.now()
    # if t.day<24:
    #     return 0
    start=time.time()
    ret=searchBtn(device)
    if ret:
        nmText=getNum(3,device)
        nmNum=0
        if len(nmText)==1:
            nmNum=int(nmText[0])
        if len(nmText)==2:
            nmNum=int(nmText[0])*10 + int(nmText[1])
        if nmNum ==1 or nmNum ==0:
            subprocess.call("adb -s emulator-{} shell input tap 855 58".format(device),shell=True)
            return 0
        # check南蛮
        # wkTag=imgs[1101:1191,131:248]
        # tfTag=imgs[1101:1191,368:489]
        # hjTag=imgs[1101:1191,604:723]
        # nmTag=imgs[1101:1191,839:967]
        #点击南蛮
        r=takeList(902,1142,2,device)
        if not(r is None) and r==-1:
            return -1
        time.sleep(1)
        #发起南蛮集结
        c=0
        while True:
            a=0
            while subprocess.call("adb -s emulator-{} exec-out screencap -p > nanman/temp.png".format(device),shell=True):
                time.sleep(1)
                a+=1
                if a >5:
                    log("=====================重新启动雷电模拟器1=====================")
                    # reStartDnplayer()
                    return -1
                True
            jijieImg=cv2.imread("nanman/temp.png")
            jijie=jijieImg[1274:1365,374:702]
            cv2.imwrite("nanman/temp.png",jijie)
            jiie=cv2.imread("nanman/temp.png",0)
            factJijie=cv2.imread("nanman/jijie.png",0)
            ret,jiie = cv2.threshold(jiie,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
            ret,factJijie = cv2.threshold(factJijie,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
            dx=(jiie-factJijie).sum()
            log("发起集结按钮偏差：{}".format(dx))
            if dx <3000:
                # 点击集结
                subprocess.call("adb -s emulator-{} shell input tap 538 1319".format(device),shell=True)
                time.sleep(1)
                c=0
                while c<2:
                    c+=1
                    a=0
                    while subprocess.call("adb -s emulator-{} exec-out screencap -p > nanman/temp.png".format(device),shell=True):
                        time.sleep(1)
                        a+=1
                        if a >5:
                            log("=====================重新启动雷电模拟器1=====================")
                            # reStartDnplayer()
                            return -1
                        True
                    msg=cv2.imread("nanman/temp.png")
                    msg=msg[627:1284,70:1000]
                    cv2.imwrite("nanman/temp.png",msg)
                    msg=cv2.imread("nanman/temp.png",0)
                    msg1=cv2.imread("nanman/msg1.png",0)
                    msg2=cv2.imread("nanman/msg2.png",0)
                    ret,msg = cv2.threshold(msg,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
                    ret,msg1 = cv2.threshold(msg1,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
                    ret,msg2 = cv2.threshold(msg2,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
                    dx1=(msg-msg1).sum()
                    dx2=(msg-msg2).sum()
                    log("南蛮发起集结前的兵力提示偏差：{}：{}".format(dx1,dx2))
                    if dx2 <60000:
                        # 选择本次登录不在显示
                        subprocess.call("adb -s emulator-{} shell input tap 596 1052".format(device),shell=True)
                        time.sleep(1)
                        subprocess.call("adb -s emulator-{} shell input tap 698 1201".format(device),shell=True)
                        time.sleep(1)
                        break
                    if dx1 <60000:
                        subprocess.call("adb -s emulator-{} shell input tap 698 1201".format(device),shell=True)
                        time.sleep(1)
                        break
                    time.sleep(1)
                c=0
                while c<2:
                    c+=1
                    a=0
                    while subprocess.call("adb -s emulator-{} exec-out screencap -p > nanman/temp.png".format(device),shell=True):
                        time.sleep(1)
                        a+=1
                        if a >5:
                            log("=====================重新启动雷电模拟器1=====================")
                            # reStartDnplayer()
                            return -1
                        True
                    msg=cv2.imread("nanman/temp.png")
                    msg=msg[627:1284,70:1000]
                    cv2.imwrite("nanman/temp.png",msg)
                    msg=cv2.imread("nanman/temp.png",0)
                    msg4=cv2.imread("nanman/msg4.png",0)
                    ret,msg = cv2.threshold(msg,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
                    ret,msg4 = cv2.threshold(msg4,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
                    dx4=(msg-msg4).sum()
                    log("南蛮发起集结前的其他人提示偏差：{}".format(dx4))
                    if dx4 <60000:
                        subprocess.call("adb -s emulator-{} shell input tap 698 1201".format(device),shell=True)
                        time.sleep(1)
                        break
                    time.sleep(1)
                c=0
                while c<3:
                    c+=1
                    a=0
                    while subprocess.call("adb -s emulator-{} exec-out screencap -p > nanman/temp.png".format(device),shell=True):
                        time.sleep(1)
                        a+=1
                        if a >5:
                            log("=====================重新启动雷电模拟器1=====================")
                            # reStartDnplayer()
                            return -1
                        True
                    msg=cv2.imread("nanman/temp.png")
                    msg=msg[692:1289,74:998]
                    cv2.imwrite("nanman/temp.png",msg)
                    msg=cv2.imread("nanman/temp.png",0)
                    msg3=cv2.imread("nanman/msg3.png",0)
                    ret,msg = cv2.threshold(msg,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
                    ret,msg3 = cv2.threshold(msg3,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
                    dx =(msg-msg3).sum()
                    log("南蛮发起集结前目标丢失的提示偏差：{}".format(dx4))
                    if dx <80000:
                        # 选择本次登录不在显示
                        subprocess.call("adb -s emulator-{} shell input tap 596 1052".format(device),shell=True)
                        time.sleep(1)
                        subprocess.call("adb -s emulator-{} shell input tap 698 1201".format(device),shell=True)
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
            a=0
            while subprocess.call("adb -s emulator-{} exec-out screencap -p > nanman/temp.png".format(device),shell=True):
                time.sleep(1)
                a+=1
                if a >5:
                    log("=====================重新启动雷电模拟器1=====================")
                    # reStartDnplayer()
                    return -1
                True
            bdImg=cv2.imread("nanman/temp.png")
            bd=bdImg[1528:1623,370:704]
            jijieLoc=bdImg[1408:1472,160:458]
            cv2.imwrite("nanman/jiijeLoc0.png",jijieLoc)
            cv2.imwrite("nanman/temp.png",bd)
            bd=cv2.imread("nanman/temp.png",0)
            factBd=cv2.imread("nanman/biandui.png",0)
            ret,bd = cv2.threshold(bd,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
            ret,factBd = cv2.threshold(factBd,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
            dx=(bd-factBd).sum()
            jiijeLoc0=cv2.imread("nanman/jiijeLoc0.png",0)
            jiijeLoc=cv2.imread("nanman/jiijeLoc.png",0)
            ret,jiijeLoc0 = cv2.threshold(jiijeLoc0,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
            ret,jiijeLoc = cv2.threshold(jiijeLoc,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
            jijieDx=(jiijeLoc0-jiijeLoc).sum()
            log("南蛮前往编队按钮的偏差：{},集结点偏差：{}".format(dx,jijieDx))
            if dx <5000 and jijieDx <5000:
                subprocess.call("adb -s emulator-{} shell input tap 527 1578".format(device),shell=True)
                time.sleep(1)
                break
            else:
                time.sleep(1)
                c+=1
            if c >10:
                log("南蛮前往编队按钮界面错误，超时")
                return -1
        cost=chuzheng(device)
        log(cost)
        if cost==-1:
            return -1
        time.sleep(1)
        subprocess.call("adb -s emulator-{} shell input tap 370 992".format(device),shell=True)
        time.sleep(2)
        #邀请助阵
        re=yaoqingzhuchengBtn(10,device)
        if re==-1:
            return -1
        a=0
        while subprocess.call("adb -s emulator-{} exec-out screencap -p > nanman/temp.png".format(device),shell=True):
            time.sleep(1)
            a+=1
            if a >5:
                log("=====================重新启动雷电模拟器1=====================")
                # reStartDnplayer()
                return -1
            True
        yqimg=cv2.imread("nanman/temp.png")
        yq=yqimg[751:820,799:1002]
        cv2.imwrite("nanman/temp.png",yq)
        yq=cv2.imread("nanman/temp.png",0)
        factyq=cv2.imread("nanman/yaoqing.png",0)
        ret,yq = cv2.threshold(yq,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
        ret,factyq = cv2.threshold(factyq,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
        dx=(yq-factyq).sum()
        log("邀请助阵按钮的偏差：{}".format(dx))
        if dx<50000:
            subprocess.call("adb -s emulator-{} shell input tap 887 794".format(device),shell=True)
            time.sleep(3)
            subprocess.call("adb -s emulator-{} shell input tap 55 48".format(device),shell=True)
            time.sleep(1)
            re=yaoqingzhuchengBtn(3,device)
            if re==0:
                subprocess.call("adb -s emulator-{} shell input tap 55 48".format(device),shell=True)
                time.sleep(1)
                subprocess.call("adb -s emulator-{} shell input tap 975 625".format(device),shell=True)
                time.sleep(1)
                subprocess.call("adb -s emulator-{} shell input tap 715 1198".format(device),shell=True)

        else:
            subprocess.call("adb -s emulator-{} shell input tap 55 48".format(device),shell=True)
            time.sleep(1)
            subprocess.call("adb -s emulator-{} shell input tap 975 625".format(device),shell=True)
            time.sleep(1)
            subprocess.call("adb -s emulator-{} shell input tap 715 1198".format(device),shell=True)
        end=time.time()
        return math.floor(end-start)
    else:
        return -1