import cv2
import numpy as np


# 获取可以攻打的坐标
def getQianWangLoc():
    gray=cv2.imread("D:/idea_workspace/TaskScript/temp.png")
    img2=cv2.imread("D:/idea_python/Demo/game/utils/qiangwang.png")
    # cv2.imshow("1",gray)
    # cv2.waitKey()
    # cv2.imshow("2",img2)
    # cv2.waitKey()
    threshold = 0.99
    res=cv2.matchTemplate(gray,img2,cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    pt = loc[::-1]
    if len(pt[0])>0 and len(pt[1])>0:
        tx=pt[0][0]+105
        ty=pt[1][0]+90
        return [tx,ty]
    else:
        return [813, 588]


if __name__ == '__main__':
    ret=getQianWangLoc()
    print(ret)