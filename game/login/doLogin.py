import subprocess
import time

import cv2

from game.logutils.mylog import log
from game.utils.tools import reStartDnplayer,is_running,startApp,take_pic,check_pic,touch


def login(id: int):
    reStartDnplayer(id)
    time.sleep(1)
    print("app is starting")
    log("开始启动app")
    while not is_running(id):
        time.sleep(1)
    time.sleep(3)
    s=startApp(id)
    log("启动app-{} result：started".format(id))
    loginTap1=cv2.imread("login/login1.png",0)
    loginTap2=cv2.imread("login/login2.png",0)
    twoClick=False
    c=0
    while True:
        time.sleep(3)
        deskTmp=take_pic(id)
        startTap=deskTmp[1672:1769,336:757]
        msg=deskTmp[715:1109,105:974]
        cv2.imwrite("login/msgTemp.png",msg)
        msg0=cv2.imread("login/loginMsg.png",0)
        msg=cv2.imread("login/msgTemp.png",0)
        dx=check_pic(msg0,msg)
        log("进入游戏界面是否存在提示偏差：{}".format(dx))
        if dx<50000:
            touch(id,486, 1209)
            time.sleep(1)
        # imageBuf1=startTap-loginTap1
        # imageBuf2=startTap-loginTap2
        # buf1Sum=imageBuf1.sum()
        # buf2Sum=imageBuf2.sum()
        buf1Sum=check_pic(startTap,loginTap1)
        buf2Sum=check_pic(startTap,loginTap2)
        log("登录界面的开始游戏按钮偏差：{},{}".format(buf1Sum,buf2Sum))
        c+=1
        if buf2Sum < 10000:
            log("开始游戏")
            break
        if buf1Sum<10000 :
            twoClick=True
            log("开始游戏")
            break
        if c > 10:
            log("开始界面获取超时")
            return -1
    print("app is started")
    if twoClick:
        touch(id,516, 1728)
        time.sleep(1)
        touch(id, 516, 1728)
        time.sleep(1)
        touch(id, 516, 1728)
    else:
        touch(id, 516, 1728)
    return changeToCityOut(id)

def changeToCityOut(id: int):
    cityIn1=cv2.imread("login/neiwaichengqiehuan1.png",0)
    cityIn2=cv2.imread("login/neiwaichengqiehuan2.png",0)
    cityOut=cv2.imread("login/chengwaishiBtn1.png",0)
    isfinish=False
    c=0
    while True:
        mainP=take_pic(id)
        swImg=mainP[1720:1842,73:244]
        bufIn1=check_pic(swImg,cityIn1)
        bufIn2=check_pic(swImg,cityIn2)
        bufOut=check_pic(swImg,cityOut)
        log("in1->{},in2->{},out->{}".format(bufIn1,bufIn2,bufOut))
        # 在城内有蒙层
        if bufIn1 <20000 :
            log("在城内有蒙层")
            touch(id,158, 1780)
        elif bufIn2 < 20000 :
            log("在城内无蒙层")
            touch(id, 158, 1780)
        elif bufOut <30000:
            log("在城外")
            isfinish=True
        else:
            log("未知区域")
            c+=1
        if isfinish :
            return 0
        if c >5:
            return -1
        time.sleep(3)

