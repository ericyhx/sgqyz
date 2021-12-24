import subprocess
import time

import cv2

# while subprocess.call("adb -s emulator-5554 exec-out screencap -p > temp.png",shell=True):
#     True
# img=cv2.imread("temp.png",)
# index=img[690:1222,80:990]
# cv2.imwrite("temp.png",index)
# img=cv2.imread("temp.png",0)
# xy=cv2.imread("xytap.png",0)
# ret,img = cv2.threshold(img,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
# ret,xy = cv2.threshold(xy,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
# dx=(xy-img).sum()
# print(dx)
subprocess.call("adb -s emulator-5554 shell input tap 243 967",shell=True)
time.sleep(0.3)
subprocess.call("adb -s emulator-5554 shell input text 666",shell=True)
time.sleep(0.3)
subprocess.call("adb -s emulator-5554 shell input tap 646 967",shell=True)
time.sleep(0.3)
subprocess.call("adb -s emulator-5554 shell input text 550",shell=True)
time.sleep(0.3)
subprocess.call("adb -s emulator-5554 shell input tap 562 1140",shell=True)
