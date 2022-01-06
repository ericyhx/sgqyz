import re,os
import subprocess
import time
from datetime import datetime

import psutil
import cv2
import numpy as np
from PIL import Image
from game.logutils.mylog import log
from pytesseract import pytesseract


console = 'D:\\LeiDian\\LDPlayer4.0\\ldconsole.exe '
processName="LdVBoxHeadless.exe"
pattern = re.compile(r'([^\s]+)\s+(\d+)\s.*\s([^\s]+\sK)')
def drawView(device: int):
    subprocess.call("adb -s emulator-{} shell input swipe 800 1162 400 1162".format(device),shell=True)

def getNum(index :int,device: int):
    drawView(device)
    a=0
    while subprocess.call("adb -s emulator-{} exec-out screencap -p > utils/main.png".format(device),shell=True):
        time.sleep(1)
        a+=1
        if a >5:
            log("=====================重新启动雷电模拟器9=====================")
            # reStartDnplayer()
            return -1
        True
    imgs=cv2.imread("utils/main.png",0)
    wkNum=imgs[1280:1320,230:306]
    tfNum=imgs[1280:1320,465:521]
    hjNum=imgs[1280:1320,695:751]
    nmNum=imgs[1280:1320,929:985]

    cv2.imwrite("utils/kdNum.png",wkNum)
    cv2.imwrite("utils/tfNum.png",tfNum)
    cv2.imwrite("utils/hjNum.png",hjNum)
    cv2.imwrite("utils/nmNum.png",nmNum)
    text="0"
    # 返回矿洞的数量
    if index==0:
        msg="可采集的矿洞"
        text = pytesseract.image_to_string(Image.open("utils/kdNum.png"),lang="eng",config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')
    elif index==1:
         msg="可攻打的土匪"
         over=cv2.imread("utils/ftOver.png")
         cur=cv2.imread("utils/tfNum.png")
         r=(over-cur).sum()
         if r <1000:
            text="0"
         else:
            text = pytesseract.image_to_string(Image.open("utils/tfNum.png"),lang="eng",config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')
    elif index==2:
        msg="可攻打的黄巾"
        text = pytesseract.image_to_string(Image.open("utils/hjNum.png"),lang="eng",config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')
    elif index==3:
        msg="可攻打的南蛮"
        text = pytesseract.image_to_string(Image.open("utils/nmNum.png"),lang="eng",config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')

    log("{}数量：{}".format(msg,text))
    text=text.strip().replace("\n","")
    return text

def showImage(img):
    cv2.imshow("img-colo",img)
    cv2.waitKey()


# 队伍出征
def chuzheng(device: int):
    c=0
    while True:
        a=0
        time.sleep(3)
        while subprocess.call("adb -s emulator-{} exec-out screencap -p > utils/main.png".format(device),shell=True):
            time.sleep(1)
            a+=1
            if a >5:
                log("=====================重新启动雷电模拟器12=====================")
                # reStartDnplayer()
                return -1
            True
        mainImg=cv2.imread("utils/main.png")
        cz=mainImg[1767:1857,605:933]
        dw=mainImg[852:1010,33:1040]
        cv2.imwrite("utils/temp.png",cz)
        cv2.imwrite("utils/dwTemp.png",dw)
        factCz=cv2.imread("utils/chuzheng.png",0)
        cz=cv2.imread("utils/temp.png",0)
        ret,factCz = cv2.threshold(factCz,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
        ret,cz = cv2.threshold(cz,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
        dx=(cz-factCz).sum()
        dw0=cv2.imread("utils/dwTemp.png",0)
        dw=cv2.imread("utils/duiwu.png",0)
        ret,dw0 = cv2.threshold(dw0,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
        ret,dw = cv2.threshold(dw,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
        dx2=(dw-dw0).sum()
        log("出征按钮偏差：{}|队伍编队偏差：{}".format(dx,dx2))
        if dx <1000 and dx2 > 10000:
            ts=mainImg[1650:1692,632:780]
            cv2.imwrite("utils/time.png",ts)
            t=parseTime("utils/time.png")
            subprocess.call("adb -s emulator-{} shell input tap 616 1842".format(device),shell=True)
            time.sleep(1)
            return t
        else:
            time.sleep(1)
            c+=1
        if c >10:
            log("出征界面错误，超时")
            return -1
# 获取列表
def takeList(tx,ty,n,device):
    #点击目标
    subprocess.call("adb -s emulator-{} shell input tap {} {}".format(device,tx,ty),shell=True)
    time.sleep(1)
    c=0
    while True:
        a=0
        while subprocess.call("adb -s emulator-{} exec-out screencap -p > utils/main.png".format(device),shell=True):
            time.sleep(1)
            a+=1
            if a >5:
                log("=====================重新启动雷电模拟器10=====================")
                # reStartDnplayer()
                return -1
            True
        mainImg=cv2.imread("utils/main.png")
        loc=mainImg[1632:1690,50:370]
        cv2.imwrite("utils/temp.png",loc)
        msg=cv2.imread("utils/temp.png",0)
        msg1=cv2.imread("utils/kuagLoc.png",0)
        msg2=cv2.imread("utils/dayeLoc.png",0)
        msg3=cv2.imread("utils/nanManLoc.png",0)
        ret,msg = cv2.threshold(msg,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
        ret,msg1 = cv2.threshold(msg1,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
        ret,msg2 = cv2.threshold(msg2,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
        ret,msg3 = cv2.threshold(msg3,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
        wkDx=(msg-msg1).sum()
        dayeDx=(msg-msg2).sum()
        nmDx=(msg-msg3).sum()
        c+=1
        log("index:{}|矿洞搜索中心偏差：{}，土匪黄巾搜索中心偏差：{}，南蛮搜索中心偏差：{}".format(n,wkDx,dayeDx,nmDx))
        if n==0 and wkDx <2000:
            break
        if n==1 and dayeDx <2000:
            break
        if n==2 and nmDx<2000:
            break
        time.sleep(1)
        if c>15:
            log("比对搜索中心超时")
            return -1


    # 点击搜索
    subprocess.call("adb -s emulator-{} shell input tap 230 1815".format(device),shell=True)
    time.sleep(1)
    c=0
    while True:
        a=0
        while subprocess.call("adb -s emulator-{} exec-out screencap -p > utils/main.png".format(device),shell=True):
            time.sleep(1)
            a+=1
            if a >5:
                log("=====================重新启动雷电模拟器1=====================")
                # reStartDnplayer()
                return -1
            True
        mainImg=cv2.imread("utils/main.png")
        goTap=mainImg[549:620,745:952]
        factGoTap=cv2.imread("utils/qiangwang.png")
        dx=(goTap-factGoTap).sum()
        log("搜索列表的偏差：{}".format(dx))
        if dx <1000:
            res=getQianWangLoc(device)
            if res is None:
                return -1
            subprocess.call("adb -s emulator-{} shell input tap {} {}".format(device,res[0],res[1]),shell=True)
            return 0
        else:
            c+=1
            time.sleep(1)
        if c > 10:
            log("获取列表超时：{}".format(c))
            return -1

def parseTime(img):
    text = pytesseract.image_to_string(Image.open(img),lang="eng")
    log(text)
    text=text.strip().replace("\n","")
    log("获取出征时间文本：{}".format(text))
    sec=180
    if len(text)==8 and text[2]==":" and text[5]==":":
        log(text)
        sec = (int(text[0])*10 + int(text[1]))*3600 + (int(text[3])*10 + int(text[4]))*60 + (int(text[6])*10 + int(text[7]))
        sec=(sec+2)*2
    else:
        log("解析出征时间出错：{}".format(text))
    return sec

# 获取可以攻打的坐标
def getQianWangLoc(device: int):
    a=0
    while subprocess.call("adb -s emulator-{} exec-out screencap -p > utils/main.png".format(device),shell=True):
        time.sleep(1)
        a+=1
        if a >5:
            log("=====================重新启动雷电模拟器1=====================")
            # reStartDnplayer()
            return None
        True
    gray=cv2.imread("utils/main.png",0)
    img2=cv2.imread("utils/nor.png",0)

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
        return [813, 588]


def searchBtn(device: int):
    # 1、判断是不是城外
    a=0
    while subprocess.call("adb -s emulator-{} exec-out screencap -p > utils/main.png".format(device),shell=True):
        time.sleep(1)
        a+=1
        if a >5:
            log("=====================重新启动雷电模拟器8=====================")
            # reStartDnplayer()
            return False
        True
    mainImg=cv2.imread("utils/main.png")
    tianxiaTag=mainImg[19:148,13:146]
    worldTag=cv2.imread("utils/world.png")
    buf=(worldTag-tianxiaTag).sum()
    log("主城外图标的偏移:{}".format(buf))
    if buf <10000:
        log("确认是在城外，满足打野条件")
        # 点击搜索
        subprocess.call("adb -s emulator-{} shell input tap 81 1376".format(device),shell=True)
        time.sleep(1)
        return True
    return False


#用于计算图像匹配的阈值
# 通过分别设置阈值为0.1、0.2、0.5、0.6、0.8、0.9，打印loc的个数可以知道，
# 当阈值较小时，候选坐标会很多，当阈值较大时，候选坐标会为空，
# 我们只要设置合理的算法找出阈值时候选坐标唯一，这个唯一的坐标就是我们要求的坐标
def getLimit(img,gray,img2):
    w,h = img2.shape[::-1]
    res=cv2.matchTemplate(gray,img2,cv2.TM_CCOEFF_NORMED)
    L = 0
    R = 1
    count = 0
    while 1:
        threshold = (L+R)/2
        count += 1
        log(count)
        loc = np.where(res >= threshold)
        if len(loc[0]) > 1:
            L += (R-L) /2
        elif len(loc[0]) == 1:
            log(loc)
            pt = loc[::-1]
            log('目标区域的左上角坐标:',pt[0],pt[1])
            log('次数:',count)
            log('阀值',threshold)
            break
        elif len(loc[0]) < 1:
            R -= (R-L) / 2
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (7,249,151), 2)
        img = cv2.resize(img, (512, 1025))
        cv2.imshow('pic',img)
        cv2.waitKey(0)

#异常情况处理
def processEx(device: int):
    c=0
    while subprocess.call("adb -s emulator-{} exec-out screencap -p > utils/exception.png".format(device),shell=True):
        time.sleep(1)
        c+=1
        if c >5:
            log("=====================重新启动雷电模拟器1=====================")
            # reStartDnplayer()
            return -1
        True
    ex=cv2.imread("utils/exception.png")
    # cv2.imwrite("exceptions/{}.png".format(dateStr()),ex)
    fanhui=ex[22:82,15:105]
    cv2.imwrite("utils/fanhui0.png",fanhui)
    fanhui=cv2.imread("utils/fanhui0.png",0)
    factFh=cv2.imread("utils/fanhui.png",0)
    factFh1=cv2.imread("utils/fanhui1.png",0)
    ret,fanhui = cv2.threshold(fanhui,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
    ret,factFh = cv2.threshold(factFh,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
    ret,factFh1 = cv2.threshold(factFh1,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
    dx=(fanhui-factFh).sum()
    dx2=(fanhui-factFh1).sum()
    if dx<1000 or dx2 <1000:
        log("界面存在返回按钮，按钮偏差：{}".format(dx))
        subprocess.call("adb -s emulator-{} shell input tap 54 47".format(device),shell=True)
        time.sleep(1)
        return 0
    else:
        log("界面不存在返回按钮，与返回按钮的偏差为：{}".format(dx))
        subprocess.call("adb -s emulator-{} shell input tap 855 58".format(device),shell=True)
        time.sleep(1)
        subprocess.call("adb -s emulator-{} shell input tap 283 1864".format(device),shell=True)
        time.sleep(1)
        subprocess.call("adb -s emulator-{} shell input tap 283 1864".format(device),shell=True)
        time.sleep(1)
        subprocess.call("adb -s emulator-{} shell input tap 283 1864".format(device),shell=True)
        time.sleep(1)
        subprocess.call("adb -s emulator-{} shell input tap 283 1864".format(device),shell=True)
        time.sleep(1)
        return 0


def dateStr():
    dt=datetime.now()
    return dt.strftime('%Y%m%d%H%M%S%f')


def restartApp():
    time.sleep(1)
    subprocess.call("adb -s emulator-5554 shell am force-stop com.tencent.tmgp.sgqyz",shell=True)
    time.sleep(5)
    subprocess.call("adb -s emulator-5554 shell am start -n com.tencent.tmgp.sgqyz/.AppActivity",shell=True)


def reStartDnplayer(id: int):
    quitDn(id)
    time.sleep(1)
    log("关闭雷电模拟器:{}".format(id))
    index=findDnMult()
    ret=0
    if not index==0:
        ret=subprocess.call("start D:\LeiDian\LDPlayer4.0\dnmultiplayer.exe",shell=True)
        log("打开多开模拟器：ret={}".format(ret))
    time.sleep(1)
    launchDn(id)
    time.sleep(2)
    if not ret ==0:
        log("启动雷电模拟器失败，执行重启")
        reStartDnplayer()
    # ret=subprocess.call("tasklist|findstr dnplayer",shell=True)
    # log("查找dnplayer进程：{}".format(ret))
    # time.sleep(1)
    # ret=subprocess.call("taskkill /f /im dnplayer.exe",shell=True)
    # log("杀死dnplayer进程：{}".format(ret))
    # time.sleep(1)
    # ret=subprocess.call("start D:\LeiDian\LDPlayer4.0\dnplayer.exe",shell=True)
    # log("启动dnplayer进程：{}".format(ret))
    # time.sleep(30)
    # ret=subprocess.call("adb start-server",shell=True)
    # log("启动adb-server：{}".format(ret))
    # time.sleep(2)
    return 0
def launchDn(index: int):
    cmd = console + 'launch --index ' + str(index)
    process = os.popen(cmd)
    result = process.read()
    process.close()
    # ret=subprocess.call("start D:\LeiDian\LDPlayer4.0\dnplayer.exe",shell=True)
    return result

def quitDn(index: int):
    cmd = console + 'quit --index ' + str(index)
    process = os.popen(cmd)
    result = process.read()
    process.close()
    subprocess.call("adb kill-server",shell=True)
    # checkDn()
    return result

def checkDn():
    time.sleep(3)
    ret=subprocess.call("tasklist|findstr dnplayer",shell=True)
    log("查找dnplayer进程：{}".format(ret))
    subprocess.call("adb kill-server",shell=True)
    if ret==0:
        time.sleep(1)
        ret=subprocess.call("taskkill /f /im dnplayer.exe",shell=True)
        log("杀死dnplayer进程：{}".format(ret))
        time.sleep(1)


def checkDnMult():
    time.sleep(2)
    ret=subprocess.call("tasklist|findstr dnmultiplayer",shell=True)
    log("dnmultiplayer：{}".format(ret))
    subprocess.call("adb kill-server",shell=True)
    if ret==0:
        time.sleep(1)
        ret=subprocess.call("taskkill /f /im dnmultiplayer.exe",shell=True)
        log("dnmultiplayer：{}".format(ret))
        time.sleep(1)

def findDnMult():
    time.sleep(1)
    ret=subprocess.call("tasklist|findstr dnmultiplayer",shell=True)
    log("dnmultiplayer：{}".format(ret))
    return ret

def getLDMem():
    cmd = 'tasklist /fi "imagename eq ' + processName + '"' + ' | findstr.exe ' + processName
    result = os.popen(cmd).read()
    resultList = result.split("\n")
    ret=False
    for srcLine in resultList:
        srcLine="".join(srcLine.split('\n'))
        if len(srcLine)==0:
            break;
        m=pattern.search(srcLine)
        if m is None:
            continue
        pid=m.group(2)
        if str(os.getpid()) is pid:
            continue
        proc=psutil.Process(int(pid))
        used=proc.memory_info().rss /1024/1024
        log("name:{}|pid:{}|used memory:{} MB".format(processName,pid,used))
        if used >3000:
            ret=True
    return ret




