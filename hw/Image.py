import subprocess
import time
import datetime

import cv2
from PIL import Image
from pytesseract import pytesseract

from game.utils.tools import dateStr

# ret=subprocess.call("tasklist|findstr dnplayer",shell=True)
# print("查找进程：{}".format(ret))
# time.sleep(1)
# ret=subprocess.call("taskkill /f /im dnplayer.exe",shell=True)
# print("杀死进程：{}".format(ret))
# time.sleep(1)
# ret=subprocess.call("start D:\LeiDian\LDPlayer4.0\dnplayer.exe",shell=True)
# print("启动进程进程：{}".format(ret))
# time.sleep(1)

# print(subprocess.call("adb shell am start -n com.tencent.tmgp.sgqyz/.AppActivity",shell=True))
# print(subprocess.call("adb shell am force-stop com.tencent.tmgp.sgqyz",shell=True))
# print("kill-server:{}".format(subprocess.call("adb kill-server",shell=True)))
# time.sleep(1)
c=0
while subprocess.call("adb -s emulator-5554 exec-out screencap -p > temp.png",shell=True):
    time.sleep(1)
    print("获取截屏:{}".format(c))
    c+=1
    True
mainImg=cv2.imread("temp.png")
loc=mainImg[1632:1690,50:370]
cv2.imwrite("dayeLoc.png",loc)

cur=datetime.datetime.now()
h=cur.hour
m=cur.minute
print("{}：{}:{}".format(cur,h,m))
n=0
while True:
    subprocess.call("adb -s emulator-5554 shell input tap 540 1038",shell=True)
    time.sleep(0.3)
    n+=1
    print(n)
zzlist=cv2.imread("temp.png")
zz=zzlist[11:75,421:654]
cv2.imwrite("tempx.png",zz)
zz=cv2.imread("tempx.png",0)
factzz=cv2.imread("zhuzhenliebiao.png",0)
dx=(zz-factzz).sum()
print(dx)
ret,zz = cv2.threshold(zz,100,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
ret,factzz = cv2.threshold(factzz,100,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
cv2.imshow("1",zz)
cv2.waitKey()
cv2.imshow("2",factzz)
cv2.waitKey()
dx=(zz-factzz).sum()
print(dx)



text=""
for i in range (5):
    while subprocess.call("adb -s emulator-5554 exec-out screencap -p > temp{}.png".format(i),shell=True):
        time.sleep(1)
        print("获取截屏:{}".format(c))
        c+=1
        True
    mainIn=cv2.imread("temp{}.png".format(i))
    fightImg=mainIn[1170:1880,119:1012]
    cv2.imwrite("temp1{}.png".format(i),fightImg)
    mainIn=cv2.imread("temp1{}.png".format(i))
    tmp = pytesseract.image_to_string(mainIn,lang='chi_sim')
    text=text+tmp
    subprocess.call("adb -s emulator-5554 shell input swipe 820 1844 820 1120 3000",shell=True)

lstt=text.split("\n")
file_handle=open("D:\\var\\data.txt",mode='w')
for i in range(len(lstt)):
    if lstt[i] is "":
        continue
    l=lstt[i].replace("\n","")
    file_handle.writelines(l+"\n")

file_handle.close()

# mainIn=cv2.imread("temp.png")
# fightImg=mainIn[1170:1880,119:1012]
# cv2.imwrite("temp1.png",fightImg)
# mainIn=cv2.imread("temp1.png")
# # ret,msg = cv2.threshold(mainIn,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
# # cv2.imshow("1",msg)
# # cv2.waitKey()
# text = pytesseract.image_to_string(mainIn,lang='chi_sim')
# print(text)


# resImg = cv2.absdiff(msg, msg1)
# print(resImg.shape[0]*resImg.shape[1])
#
# print(resImg.sum())
# ret,msg = cv2.threshold(msg,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
# ret,msg1 = cv2.threshold(msg1,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
# print((msg-msg1).sum())


def parseSimple(img):
    mainIn=cv2.imread(img)
    text = pytesseract.image_to_string(mainIn,lang='chi_sim')
    print(text)