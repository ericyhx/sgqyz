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
ld = 'D:\\LeiDian\\LDPlayer4.0\\ld.exe '
processName="LdVBoxHeadless.exe"
pattern = re.compile(r'([^\s]+)\s+(\d+)\s.*\s([^\s]+\sK)')
share_path = 'C:\\Users\\hello world\\Documents\\leidian\\Pictures'
expIds = [10,11]
def drawView(id: int):
   return dnld(id, 'input swipe %d %d %d %d' % (800, 1162, 400, 1162))

def dnld(index: int, command: str, silence: bool = True):
    cmd = ld + '-s %d %s' % (index, command)
    if silence:
        os.system(cmd)
        return ''
    process = os.popen(cmd)
    result = process.read()
    process.close()
    return result
def take_pic(id:int):
    dnld(id, 'screencap -p /sdcard/Pictures/apk_scr_'+str(id)+'.png')
    time.sleep(0.5)
    imgs = cv2.imread(share_path + '/apk_scr_'+str(id)+'.png', 0)
    return imgs
def getNum(id:int,index :int):
    drawView(id)
    imgs=take_pic(id)
    wkNum=imgs[1280:1320,230:306]
    tfNum=imgs[1280:1320,465:521]
    hjNum=imgs[1280:1320,695:751]
    nmNum=imgs[1280:1320,929:985]
    text="0"
    # 返回矿洞的数量
    if index==0:
        msg="可采集的矿洞"
        text = pytesseract.image_to_string(Image.fromarray(wkNum),lang="eng",config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')
    elif index==1:
         msg="可攻打的土匪"
         over=cv2.imread("utils/ftOver.png",0)
         # cur=cv2.imread("utils/tfNum.png")
         r=check_pic(over,tfNum)
         if r <100:
            text="0"
         else:
            text = pytesseract.image_to_string(Image.fromarray(tfNum),lang="eng",config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')
    elif index==2:
        msg="可攻打的黄巾"
        text = pytesseract.image_to_string(Image.fromarray(hjNum),lang="eng",config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')
    elif index==3:
        msg="可攻打的南蛮"
        text = pytesseract.image_to_string(Image.fromarray(nmNum),lang="eng",config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')

    log("{}数量：{}".format(msg,text))
    text=text.strip().replace("\n","")
    return text
def check_pic(cur,src):
    ret, factCz = cv2.threshold(cur, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)
    ret, cz = cv2.threshold(src, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)
    dx = (cz - factCz).sum()
    return dx

# 队伍出征
def chuzheng(id: int):
    c=0
    time.sleep(3)
    while True:
        a=0
        time.sleep(0.5)
        mainImg = take_pic(id)
        cz=mainImg[1767:1857,605:933]
        dw=mainImg[852:1010,33:1040]
        cv2.imwrite("utils/temp.png",cz)
        cv2.imwrite("utils/dwTemp.png",dw)
        factCz=cv2.imread("utils/chuzheng.png",0)
        cz=cv2.imread("utils/temp.png",0)
        dx=check_pic(factCz,cz)
        dw0=cv2.imread("utils/dwTemp.png",0)
        dw=cv2.imread("utils/duiwu.png",0)
        dx2=check_pic(dw0,dw)
        log("出征按钮偏差：{}|队伍编队偏差：{}".format(dx,dx2))
        if dx <100000 and dx2 > 100000:
            ts=mainImg[1650:1692,632:780]
            t=parseTime(ts)
            touch(id,616,1842)
            time.sleep(0.3)
            return t
        else:
            time.sleep(0.3)
            c+=1
        if c >10:
            log("出征界面错误，超时")
            return -1
# 获取列表
def takeList(tx,ty,id):
    #点击目标
    touch(id,tx,ty)
    time.sleep(0.5)
    # c=0
    # while True:
    #     a=0
    #     while subprocess.call("adb -s emulator-{} exec-out screencap -p > utils/main.png".format(device),shell=True):
    #         time.sleep(0.3)
    #         a+=1
    #         if a >5:
    #             log("=====================重新启动雷电模拟器10=====================")
    #             # reStartDnplayer()
    #             return -1
    #         True
    #     mainImg=cv2.imread("utils/main.png")
    #     loc=mainImg[1632:1690,50:370]
    #     cv2.imwrite("utils/temp.png",loc)
    #     msg=cv2.imread("utils/temp.png",0)
    #     msg1=cv2.imread("utils/kuagLoc.png",0)
    #     msg2=cv2.imread("utils/dayeLoc.png",0)
    #     msg3=cv2.imread("utils/nanManLoc.png",0)
    #     ret,msg = cv2.threshold(msg,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
    #     ret,msg1 = cv2.threshold(msg1,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
    #     ret,msg2 = cv2.threshold(msg2,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
    #     ret,msg3 = cv2.threshold(msg3,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
    #     wkDx=(msg-msg1).sum()
    #     dayeDx=(msg-msg2).sum()
    #     nmDx=(msg-msg3).sum()
    #     c+=1
    #     log("index:{}|矿洞搜索中心偏差：{}，土匪黄巾搜索中心偏差：{}，南蛮搜索中心偏差：{}".format(n,wkDx,dayeDx,nmDx))
    #     if n==0 and wkDx <200000:
    #         break
    #     if n==1 and dayeDx <200000:
    #         break
    #     if n==2 and nmDx<200000:
    #         break
    #     time.sleep(0.3)
    #     if c>15:
    #         log("比对搜索中心超时")
    #         return -1


    # 点击搜索
    touch(id,230,1815)
    time.sleep(1)
    c=0
    while True:
        mainImg=take_pic(id)
        goTap=mainImg[549:620,745:952]
        factGoTap=cv2.imread("utils/qiangwang.png",0)
        dx=check_pic(goTap,factGoTap)
        log("搜索列表的偏差：{}".format(dx))
        if dx <100000:
            res=getQianWangLoc(id)
            if res is None:
                return -1
            touch(id,res[0],res[1])
            return 0
        else:
            c+=1
            time.sleep(1)
        if c > 10:
            log("获取列表超时：{}".format(c))
            return -1
def touch(index: int, x: int, y: int):
   return dnld(index, 'input tap %d %d' % (x, y))

def parseTime(img):
    text = pytesseract.image_to_string(Image.fromarray(img),lang="eng")
    log(text)
    text=text.strip().replace("\n","")
    log("获取出征时间文本：{}".format(text))
    sec=180
    if len(text)==8 and text[2]==":" and text[5]==":":
        log(text)
        sec = (int(text[0])*10 + int(text[1]))*3600 + (int(text[3])*10 + int(text[4]))*60 + (int(text[6])*10 + int(text[7]))
        sec=(sec)*2
    else:
        cv2.imwrite("exceptions/time.png",img)
        log("解析出征时间出错：{}".format(text))
    return sec

# 获取可以攻打的坐标
def getQianWangLoc(id: int):
    gray=take_pic(id)
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


def searchBtn(id: int):
    # 1、判断是不是城外
    a=0
    log("开始截屏")
    mainImg=take_pic(id)
    log("截屏结束")
    tianxiaTag=mainImg[19:148,13:146]
    worldTag=cv2.imread("utils/world.png",0)
    buf=check_pic(tianxiaTag,worldTag)
    log("主城外图标的偏移:{}".format(buf))
    if buf <10000:
        log("确认是在城外，满足打野条件")
        # 点击搜索
        if expIds.count(id):
            touch(id, 80, 1550)
        else:
            touch(id,81, 1376)
        time.sleep(0.3)
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
def processEx(id: int):
    ex=take_pic(id)
    fanhui=ex[22:82,15:105]
    factFh=cv2.imread("utils/fanhui.png",0)
    factFh1=cv2.imread("utils/fanhui1.png",0)
    dx=check_pic(fanhui,factFh)
    dx2=check_pic(fanhui, factFh1)
    if dx<1000 or dx2 <1000:
        log("界面存在返回按钮，按钮偏差：{}".format(dx))
        touch(id,54, 47)
        time.sleep(1)
        return 0
    else:
        log("界面不存在返回按钮，与返回按钮的偏差为：{}".format(dx))
        touch(id, 855, 58)
        time.sleep(1)
        for i in range(4):
            touch(id, 283, 1864)
            time.sleep(1)
        return 0


def dateStr():
    dt=datetime.now()
    return dt.strftime('%Y%m%d%H%M%S%f')

def startApp(id:int):
    cmd = console + 'runapp --index %d --packagename %s' % (id, 'com.tencent.tmgp.sgqyz')
    process = os.popen(cmd)
    result = process.read()
    process.close()
    log("app start result:"+result)
    return result
def restartApp(id:int):
    time.sleep(1)
    cmd = console + 'killapp --index %d --packagename %s' % (id, 'com.tencent.tmgp.sgqyz')
    process = os.popen(cmd)
    result = process.read()
    process.close()
    time.sleep(3)
    cmd = console + 'launch --index ' + str(id)
    process = os.popen(cmd)
    result = process.read()
    process.close()
    return result
def get_list():
    cmd = os.popen(console + 'list2')
    text = cmd.read()
    cmd.close()
    info = text.split('\n')
    result = list()
    for line in info:
        if len(line) > 1:
            dnplayer = line.split(',')
            result.append(result2list(dnplayer))
    return result
def result2list(info: list):
    index = int(info[0])
    name = info[1]
    top_win_handler = int(info[2])
    bind_win_handler = int(info[3])
    is_in_android = True if int(info[4]) == 1 else False
    pid = int(info[5])
    vbox_pid = int(info[6])
    return index,name,top_win_handler,bind_win_handler,is_in_android,pid,vbox_pid
def is_running(index: int) -> bool:
    all = get_list()
    if index >= len(all):
        raise False
    return all[index][4]
def reStartDnplayer(id: int):
    log(3)
    quitDn(id)
    time.sleep(4)
    log("关闭雷电模拟器:{}".format(id))
    time.sleep(1)
    launchDn(id)
    time.sleep(2)
    return 0
def launchDn(index: int):
    cmd = console + 'launch --index ' + str(index)
    process = os.popen(cmd)
    result = process.read()
    process.close()
    return result

def quitDn(index: int):
    cmd = console + 'quit --index ' + str(index)
    process = os.popen(cmd)
    result = process.read()
    process.close()
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

if __name__ == '__main__':
    lst=get_list()
    print(len(lst))
    for i in range(len(lst)):
        index = lst[i][0]
        print(index)
    img=cv2.imread("D:\\idea_python\\Demo-dev-2\\game\\exceptions\\1.png")
    text = pytesseract.image_to_string(Image.fromarray(img), lang="eng")
    log(text)
    text = text.strip().replace("\n", "")
    log("获取出征时间文本：{}".format(text))
    sec = 180
    if len(text) == 8 and text[2] == ":" and text[5] == ":":
        log(text)
        sec = (int(text[0]) * 10 + int(text[1])) * 3600 + (int(text[3]) * 10 + int(text[4])) * 60 + (
                    int(text[6]) * 10 + int(text[7]))
        sec = (sec) * 2
    else:
        cv2.imwrite("exceptions/time.png", img)
        log("解析出征时间出错：{}".format(text))




