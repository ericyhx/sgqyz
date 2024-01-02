import math
import subprocess
import time

import cv2

from game.logutils.mylog import log
from game.utils.tools import take_pic,check_pic,touch


def doTask(id: int):
    # return 0
    start=time.time()
    lianmeng=take_pic(id)
    lianmeng=lianmeng[1795:1889,936:1036]
    cv2.imwrite("cityTask/temp.png",lianmeng)
    lm=cv2.imread("cityTask/temp.png",0)
    factLm=cv2.imread("cityTask/lianmeng.png",0)
    dx=check_pic(lm,factLm)
    log("联盟按钮的偏差：{}".format(dx))
    if dx <300000:
        #点击联盟
        touch(id,986, 1832)
        time.sleep(1)
        #点击主页
        touch(id, 216, 1847)
        time.sleep(1)
        touch(id, 216, 1847)
        time.sleep(1)
        #点击联盟城市
        touch(id, 838, 925)
        time.sleep(1)
        #判断城市任务
        c=0
        while True:
            task=take_pic(id)
            task=task[1771:1865,626:959]
            cv2.imwrite("cityTask/temp.png",task)
            task=cv2.imread("cityTask/temp.png",0)
            oneKey=cv2.imread("cityTask/oneKey.png",0)
            dx = check_pic(task,oneKey)
            log("一键执行按钮的偏差：{}".format(dx))
            if dx <100000:
                #点击一键执行
                touch(id,771, 1822)
                time.sleep(1)
                touch(id, 771, 1822)
                time.sleep(1)
                touch(id, 771, 1822)
                time.sleep(1)
                touch(id,58, 47)
                time.sleep(1)
                touch(id, 58, 47)
                time.sleep(1)
                end=time.time()
                return math.floor(end-start)
            else:
                c+=1
                time.sleep(1)
            if c >10:
                return -1
    else:
        return -1