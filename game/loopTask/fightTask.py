import datetime
import subprocess
import time

import cv2

from game.logutils.mylog import log
from game.utils.tools import processEx


def findTager(c,device):
    subprocess.call("adb -s emulator-{} shell input tap 700 1579".format(device),shell=True)
    time.sleep(0.5)
    a=0
    while subprocess.call("adb -s emulator-{} exec-out screencap -p > loopTask/temp.png".format(device),shell=True):
        time.sleep(0.3)
        a+=1
        if a >5:
            log("=====================寻找目标失败=====================")
            return -1
        True
    img=cv2.imread("loopTask/temp.png",)
    index=img[699:746,457:638]
    cv2.imwrite("loopTask/temp.png",index)
    img=cv2.imread("loopTask/temp.png",0)
    xy=cv2.imread("loopTask/xytap.png",0)
    ret,img = cv2.threshold(img,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
    ret,xy = cv2.threshold(xy,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
    dx=(xy-img).sum()
    log("坐标搜索偏差：{}".format(dx))
    if dx <150000:
        subprocess.call("adb -s emulator-{} shell input tap 243 967".format(device),shell=True)
        time.sleep(0.1)
        subprocess.call("adb -s emulator-{} shell input text 664".format(device),shell=True)
        time.sleep(0.1)
        subprocess.call("adb -s emulator-{} shell input tap 646 967".format(device),shell=True)
        time.sleep(0.1)
        subprocess.call("adb -s emulator-{} shell input text 553".format(device),shell=True)
        time.sleep(0.1)
        subprocess.call("adb -s emulator-{} shell input tap 562 1140".format(device),shell=True)
        time.sleep(0.8)
        subprocess.call("adb -s emulator-{} shell input tap 858 1061".format(device),shell=True)
        time.sleep(0.5)
        subprocess.call("adb -s emulator-{} shell input tap 714 1816".format(device),shell=True)
        if c==1:
            time.sleep(2)
        time.sleep(0.5)
        return 0
    else:
        return -1
        #     # print("寨子")
        #     # subprocess.call("adb -s emulator-5554 shell input tap 540 1022",shell=True)
        #     # time.sleep(1)
        #     ret=check()
        #     end=datetime.datetime.now()
        #     print("gap:{}|ret:{}".format((end-start).min,ret))


def findTager2():
    subprocess.call("adb -s emulator-5554 shell input tap 700 1579",shell=True)
    time.sleep(0.5)
    a=0
    while subprocess.call("adb -s emulator-5554 exec-out screencap -p > temp.png",shell=True):
        time.sleep(0.3)
        a+=1
        if a >5:
            log("=====================寻找目标失败=====================")
            return -1
        True
    img=cv2.imread("temp.png",)
    index=img[699:746,457:638]
    cv2.imwrite("temp.png",index)
    img=cv2.imread("temp.png",0)
    xy=cv2.imread("xytap.png",0)
    ret,img = cv2.threshold(img,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
    ret,xy = cv2.threshold(xy,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
    dx=(xy-img).sum()
    print(dx)
    if dx <50000:
        subprocess.call("adb -s emulator-5554 shell input tap 243 967",shell=True)
        time.sleep(0.1)
        subprocess.call("adb -s emulator-5554 shell input text 665",shell=True)
        time.sleep(0.1)
        subprocess.call("adb -s emulator-5554 shell input tap 646 967",shell=True)
        time.sleep(0.1)
        subprocess.call("adb -s emulator-5554 shell input text 550",shell=True)
        time.sleep(0.1)
        subprocess.call("adb -s emulator-5554 shell input tap 562 1140",shell=True)
        time.sleep(1)
        while True:
            subprocess.call("adb -s emulator-5554 shell input tap 858 1061",shell=True)
            time.sleep(0.5)
            subprocess.call("adb -s emulator-5554 shell input tap 714 1816",shell=True)
            time.sleep(0.5)
            subprocess.call("adb -s emulator-5554 shell input tap 540 1038",shell=True)
            time.sleep(0.5)


def check():
    a=0
    while subprocess.call("adb -s emulator-5554 exec-out screencap -p > temp.png",shell=True):
        time.sleep(0.3)
        a+=1
        if a >5:
            log("=====================寻找目标失败=====================")
            return -1
        True
    img=cv2.imread("temp.png",)
    index=img[1009:1090,809:878]
    cv2.imwrite("temp.png",index)
    img=cv2.imread("temp.png",0)
    xy=cv2.imread("cuihui.png",0)
    xy1=cv2.imread("temp1.png",0)
    ret,img = cv2.threshold(img,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
    ret,xy = cv2.threshold(xy,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
    ret,xy1 = cv2.threshold(xy1,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
    dx=(xy-img).sum()
    dx1=(xy1-img).sum()
    print("摧毁dx:{}|dx1:{}".format(dx,dx1))
    if dx <10000 or dx1<10000:
        subprocess.call("adb -s emulator-5554 shell input tap 858 1061",shell=True)
        time.sleep(0.5)
        subprocess.call("adb -s emulator-5554 shell input tap 714 1816",shell=True)
        time.sleep(0.5)
        subprocess.call("adb -s emulator-5554 shell input tap 540 1022",shell=True)
        time.sleep(0.5)
        return 0
    else:
        return 1

def gongji():
    start=time.time()
    c=0
    while True:
        ret=findTager(c)
        c+=1
        if c==2:
            c=0
        end=time.time()
        n=int(end-start)
        log("攻打寨子 result={}|time:{}".format(ret,n))
        if ret==-1:
            processEx()
            r=processEx()
            if r==-1:
                return -1
        if n >300:
            return 0

if __name__ == '__main__':
    findTager2()

