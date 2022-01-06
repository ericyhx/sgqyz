import subprocess
import time

import cv2

from game.logutils.mylog import log
from game.utils.tools import reStartDnplayer


def login(id: int,device: int):
    reStartDnplayer(id)
    time.sleep(1)
    c=0
    log("开始启动app")
    s=subprocess.call("adb -s emulator-{} shell am start -n com.tencent.tmgp.sgqyz/.AppActivity".format(device),shell=True)
    log("启动app-{} result：{}".format(device,s))
    while s:
        time.sleep(1)
        c+=1
        s=subprocess.call("adb -s emulator-{} shell am start -n com.tencent.tmgp.sgqyz/.AppActivity".format(device),shell=True)
        log("启动app again result：{}|cnt={}".format(s,c))
        if c>20:
            log("启动app失败")
            reStartDnplayer(id)
            return -1
        True
    loginTap1=cv2.imread("login/login1.png")
    loginTap2=cv2.imread("login/login2.png")
    twoClick=False
    c=0
    while True:
        time.sleep(5)
        a=0
        while subprocess.call("adb -s emulator-{} exec-out screencap -p > login/deskTmp.png".format(device),shell=True):
            time.sleep(1)
            a+=1
            if a >5:
                log("=====================重新启动雷电模拟器1=====================")
                # reStartDnplayer()
                return -1
            True
        deskTmp=cv2.imread("login/deskTmp.png")
        startTap=deskTmp[1672:1769,336:757]
        msg=deskTmp[715:1109,105:974]
        cv2.imwrite("login/msgTemp.png",msg)
        msg0=cv2.imread("login/loginMsg.png",0)
        msg=cv2.imread("login/msgTemp.png",0)
        ret,msg0 = cv2.threshold(msg0,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
        ret,msg = cv2.threshold(msg,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
        dx=(msg0-msg).sum()
        log("进入游戏界面是否存在提示偏差：{}".format(dx))
        if dx<5000:
            subprocess.call("adb -s emulator-{} shell input tap 486 1209".format(device),shell=True)
            time.sleep(1)
        imageBuf1=startTap-loginTap1
        imageBuf2=startTap-loginTap2
        buf1Sum=imageBuf1.sum()
        buf2Sum=imageBuf2.sum()
        log("登录界面的开始游戏按钮偏差：{},{}".format(buf1Sum,buf2Sum))
        c+=1
        if buf1Sum<10000 :
            twoClick=True
            log("开始游戏")
            break
        if buf2Sum<10000:
            log("开始游戏")
            break
        if c > 10:
            log("开始界面获取超时")
            return -1
    if twoClick:
        subprocess.call("adb -s emulator-{} shell input tap 516 1728".format(device),shell=True)
        time.sleep(1)
        subprocess.call("adb -s emulator-{} shell input tap 516 1728".format(device),shell=True)
        time.sleep(1)
        subprocess.call("adb -s emulator-{} shell input tap 516 1728".format(device),shell=True)
    else:
        subprocess.call("adb -s emulator-{} shell input tap 516 1728".format(device),shell=True)
    return changeToCityOut(device)

def changeToCityOut(device: int):
    cityIn1=cv2.imread("login/neiwaichengqiehuan1.png")
    cityIn2=cv2.imread("login/neiwaichengqiehuan2.png")
    cityOut=cv2.imread("login/chengwaishiBtn1.png")
    isfinish=False
    c=0
    while True:
        a=0
        while subprocess.call("adb -s emulator-{} exec-out screencap -p > login/main.png".format(device),shell=True):
            time.sleep(1)
            a+=1
            if a >5:
                log("=====================重新启动雷电模拟器2=====================")
                # reStartDnplayer()
                return -1
            True
        mainP=cv2.imread("login/main.png")
        swImg=mainP[1720:1842,73:244]
        bufIn1=(swImg-cityIn1).sum()
        bufIn2=(swImg-cityIn2).sum()
        bufOut=(swImg-cityOut).sum()
        log("in1->{},in2->{},out->{}".format(bufIn1,bufIn2,bufOut))
        # 在城内有蒙层
        if bufIn1 <10000 :
            log("在城内有蒙层")
            subprocess.call("adb -s emulator-{} shell input tap 158 1780".format(device),shell=True)
        elif bufIn2 < 10000 :
            log("在城内无蒙层")
            subprocess.call("adb -s emulator-{} shell input tap 158 1780".format(device),shell=True)
        elif bufOut <10000:
            log("在城外")
            isfinish=True
        else:
            log("未知区域")
            c+=1
        if isfinish :
            return 0
        if c >25:
            return -1
        time.sleep(3)

