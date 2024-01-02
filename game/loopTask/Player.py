import ast
import configparser
import logging.handlers
import logging.handlers
import os
import re
import time

import cv2
import numpy as np
from PIL import Image
from pytesseract import pytesseract

from game.utils.tools import expIds

logging.basicConfig(level=logging.DEBUG,#控制台打印的日志级别
                    filename='log.log',
                    encoding='utf-8',
                    filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    #a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    #日志格式
                    )
console = 'D:\\LeiDian\\LDPlayer4.0\\ldconsole.exe '
ld = 'D:\\LeiDian\\LDPlayer4.0\\ld.exe '
processName="LdVBoxHeadless.exe"
pattern = re.compile(r'([^\s]+)\s+(\d+)\s.*\s([^\s]+\sK)')
share_path = 'C:\\Users\\hello world\\Documents\\leidian\\Pictures'


class SG_Player(object):
    cf = None
    cf_file = None
    def __init__(self,file,file_cf):
        self.cf_file = file
        self.cf=file_cf
    def changeToCityOut(self,id: int):
        cityIn1 = cv2.imread("login/neiwaichengqiehuan1.png", 0)
        cityIn2 = cv2.imread("login/neiwaichengqiehuan2.png", 0)
        cityOut = cv2.imread("login/chengwaishiBtn1.png", 0)
        isfinish = False
        c = 0
        while True:
            mainP = self.take_pic(id)
            swImg = mainP[1720:1842, 73:244]
            bufIn1 = self.check_pic(swImg, cityIn1)
            bufIn2 = self.check_pic(swImg, cityIn2)
            bufOut = self.check_pic(swImg, cityOut)
            logging.info("in1->{},in2->{},out->{}".format(bufIn1, bufIn2, bufOut))
            # 在城内有蒙层
            if bufIn1 < 20000:
                logging.info("在城内有蒙层")
                self.touch(id, 158, 1780)
            elif bufIn2 < 20000:
                logging.info("在城内无蒙层")
                self.touch(id, 158, 1780)
            elif bufOut < 30000:
                logging.info("在城外")
                isfinish = True
            else:
                logging.info("未知区域")
                c += 1
            if isfinish:
                return 0
            if c > 5:
                return -1
            time.sleep(3)

    def login(self,id: int):
        self.reStartDnplayer(id)
        time.sleep(1)
        print("app is starting")
        logging.info("开始启动app")
        while not self.is_running(id):
            time.sleep(1)
        time.sleep(3)
        s = self.startApp(id)
        logging.info("启动app-{} result：started".format(id))
        loginTap1 = cv2.imread("login/login1.png", 0)
        loginTap2 = cv2.imread("login/login2.png", 0)
        twoClick = False
        c = 0
        while True:
            time.sleep(3)
            deskTmp = self.take_pic(id)
            startTap = deskTmp[1672:1769, 336:757]
            msg = deskTmp[715:1109, 105:974]
            cv2.imwrite("login/msgTemp.png", msg)
            msg0 = cv2.imread("login/loginMsg.png", 0)
            msg = cv2.imread("login/msgTemp.png", 0)
            dx = self.check_pic(msg0, msg)
            logging.info("进入游戏界面是否存在提示偏差：{}".format(dx))
            if dx < 50000:
                self.touch(id, 486, 1209)
                time.sleep(1)
            buf1Sum = self.check_pic(startTap, loginTap1)
            buf2Sum = self.check_pic(startTap, loginTap2)
            logging.info("登录界面的开始游戏按钮偏差：{},{}".format(buf1Sum, buf2Sum))
            c += 1
            if buf2Sum < 10000:
                logging.info("开始游戏")
                break
            if buf1Sum < 10000:
                twoClick = True
                logging.info("开始游戏")
                break
            if c > 10:
                logging.info("开始界面获取超时")
                return -1
        print("app is started")
        if twoClick:
            self.touch(id, 516, 1728)
            time.sleep(1)
            self.touch(id, 516, 1728)
            time.sleep(1)
            self.touch(id, 516, 1728)
            time.sleep(1)
            self.touch(id, 516, 1728)
        else:
            time.sleep(1)
            self.touch(id, 516, 1728)
            time.sleep(0.5)
            self.touch(id, 516, 1728)
            time.sleep(0.5)
            self.touch(id, 516, 1728)
        return self.changeToCityOut(id)

    # 点击采集按钮
    def goCaiji(self,id: int):
        c = 0
        while True:
            mainImg = self.take_pic(id)
            caiji = mainImg[1129:1221, 660:740]
            cv2.imwrite("wakuang/temp.png", caiji)
            factCaiji = cv2.imread("wakuang/caiji.png", 0)
            caiji = cv2.imread("wakuang/temp.png", 0)
            dx = self.check_pic(caiji, factCaiji)
            logging.info("采集的偏差：{}".format(dx))
            if dx < 10000:
                self.touch(id, 695, 1178)
                return 0
            else:
                time.sleep(1)
                c += 1
            if c > 20:
                logging.info("跳转采集出错")
                return -1

    def wakuang(self,id:int):
        ret = self.searchBtn(id)
        if ret:
            kdCnt = (int)(self.getNum(id, 0))
            if kdCnt >0:
                #点击矿洞
                r=self.takeList(183,1137,id)
                if not(r is None) and r==-1:
                    return -1
                r=self.goCaiji(id)
                if not(r is None) and r==-1:
                    return -1
                r=self.chuzheng(id)
                if r is None:
                    r=0
                return r
            elif kdCnt ==0:
                cnt=self.backKuangdui(id,False)
                if cnt < 3:
                    logging.info("等待队伍返回")
                    self.touch(id,845,63)
                    time.sleep(2)
                    self.touch(id, 845, 63)
                    time.sleep(8)
                    return 20
                #挖矿结束
                return -2
            else:
                logging.info("矿洞获取有误")
                return -1

        else:
            return -1

    def startOrRestart(self,id: int):
        print("{} device[{}] is starting to wakuang".format(time.strftime('%m-%d %H:%M:%S', time.localtime(time.time())),id))
        logging.info("execute waKuang|device[{}] is starting".format(id))
        ret = self.login(id)
        exc = 0
        while True:
            if exc > 5:
                logging.info("进入游戏异常，重新启动app")
                ret = self.login(id)
            if ret == -1:
                exc += 1
                ret = self.processEx(id)
                time.sleep(1)
            else:
                logging.info("进入游戏成功")
                break

    def processEx(self,id: int):
        ex = self.take_pic(id)
        fanhui = ex[22:82, 15:105]
        factFh = cv2.imread("utils/fanhui.png", 0)
        factFh1 = cv2.imread("utils/fanhui1.png", 0)
        dx = self.check_pic(fanhui, factFh)
        dx2 = self.check_pic(fanhui, factFh1)
        if dx < 1000 or dx2 < 1000:
            logging.info("界面存在返回按钮，按钮偏差：{}".format(dx))
            self.touch(id, 54, 47)
            time.sleep(1)
            return 0
        else:
            logging.info("界面不存在返回按钮，与返回按钮的偏差为：{}".format(dx))
            self.touch(id, 855, 58)
            time.sleep(1)
            for i in range(4):
                self.touch(id, 283, 1864)
                time.sleep(1)
            return 0

    def launchDn(self,index: int):
        cmd = console + 'launch --index ' + str(index)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    def quitDn(self,index: int):
        cmd = console + 'quit --index ' + str(index)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    def get_list(self):
        cmd = os.popen(console + 'list2')
        text = cmd.read()
        cmd.close()
        info = text.split('\n')
        result = list()
        for line in info:
            if len(line) > 1:
                dnplayer = line.split(',')
                result.append(self.result2list(dnplayer))
        return result

    def result2list(self,info: list):
        index = int(info[0])
        name = info[1]
        top_win_handler = int(info[2])
        bind_win_handler = int(info[3])
        is_in_android = True if int(info[4]) == 1 else False
        pid = int(info[5])
        vbox_pid = int(info[6])
        return index, name, top_win_handler, bind_win_handler, is_in_android, pid, vbox_pid

    def reStartDnplayer(self,id: int):
        self.quitDn(id)
        time.sleep(4)
        logging.info("关闭雷电模拟器:{}".format(id))
        time.sleep(1)
        self.launchDn(id)
        time.sleep(2)
        return 0

    def is_running(self,index: int) -> bool:
        all = self.get_list()
        if index >= len(all):
            raise False
        return all[index][4]

    def startApp(self,id:int):
        cmd = console + 'runapp --index %d --packagename %s' % (id, 'com.tencent.tmgp.sgqyz')
        process = os.popen(cmd)
        result = process.read()
        process.close()
        logging.info("app start result:"+result)
        return result

    def drawView(self,id: int):
        return self.dnld(id, 'input swipe %d %d %d %d' % (800, 1162, 400, 1162))

    def dnld(self,index: int, command: str, silence: bool = True):
        cmd = ld + '-s %d %s' % (index, command)
        if silence:
            os.system(cmd)
            return ''
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    def take_pic(self,id: int):
        self.dnld(id, 'screencap -p /sdcard/Pictures/apk_scr_' + str(id) + '.png')
        time.sleep(0.5)
        imgs = cv2.imread(share_path + '/apk_scr_' + str(id) + '.png', 0)
        return imgs

    def getNum(self,id: int, index: int):
        self.drawView(id)
        imgs = self.take_pic(id)
        wkNum = imgs[1280:1320, 230:306]
        tfNum = imgs[1280:1320, 465:521]
        hjNum = imgs[1280:1320, 695:751]
        nmNum = imgs[1280:1320, 929:985]
        text = "0"
        # 返回矿洞的数量
        if index == 0:
            msg = "可采集的矿洞"
            text = pytesseract.image_to_string(Image.fromarray(wkNum), lang="eng",
                                               config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')
        elif index == 1:
            msg = "可攻打的土匪"
            over = cv2.imread("utils/ftOver.png", 0)
            r = self.check_pic(over, tfNum)
            if r < 100:
                text = "0"
            else:
                text = pytesseract.image_to_string(Image.fromarray(tfNum), lang="eng",
                                                   config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')
        elif index == 2:
            msg = "可攻打的黄巾"
            text = pytesseract.image_to_string(Image.fromarray(hjNum), lang="eng",
                                               config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')
        elif index == 3:
            msg = "可攻打的南蛮"
            text = pytesseract.image_to_string(Image.fromarray(nmNum), lang="eng",
                                               config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')

        logging.info("{}数量：{}".format(msg, text))
        text = text.strip().replace("\n", "")
        return text

    def check_pic(self,cur, src):
        ret, factCz = cv2.threshold(cur, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)
        ret, cz = cv2.threshold(src, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)
        dx = (cz - factCz).sum()
        return dx

    # 队伍出征
    def chuzheng(self,id: int):
        c = 0
        while True:
            time.sleep(0.5)
            mainImg = self.take_pic(id)
            cz = mainImg[1767:1857, 605:933]
            dw = mainImg[852:1010, 33:1040]
            cv2.imwrite("utils/temp.png", cz)
            cv2.imwrite("utils/dwTemp.png", dw)
            factCz = cv2.imread("utils/chuzheng.png", 0)
            cz = cv2.imread("utils/temp.png", 0)
            dx = self.check_pic(factCz, cz)
            dw0 = cv2.imread("utils/dwTemp.png", 0)
            dw = cv2.imread("utils/duiwu.png", 0)
            dx2 = self.check_pic(dw0, dw)
            logging.info("出征按钮偏差：{}|队伍编队偏差：{}".format(dx, dx2))
            if dx < 100000 and dx2 > 100000:
                ts = mainImg[1650:1692, 632:780]
                t = self.parseTime(ts)
                self.touch(id, 616, 1842)
                time.sleep(0.3)
                return t
            else:
                time.sleep(0.3)
                c += 1
            if c > 10:
                logging.info("出征界面错误，超时")
                return -1

    # 获取列表
    def takeList(self,tx, ty, id):
        # 点击目标
        self.touch(id, tx, ty)
        time.sleep(0.5)
        # 点击搜索
        self.touch(id, 230, 1815)
        time.sleep(1)
        c = 0
        while True:
            mainImg = self.take_pic(id)
            goTap = mainImg[549:620, 745:952]
            factGoTap = cv2.imread("utils/qiangwang.png", 0)
            dx = self.check_pic(goTap, factGoTap)
            logging.info("搜索列表的偏差：{}".format(dx))
            if dx < 100000:
                res = self.getQianWangLoc(id)
                if res is None:
                    return -1
                self.touch(id, res[0], res[1])
                return 0
            else:
                c += 1
                time.sleep(1)
            if c > 10:
                logging.info("获取列表超时：{}".format(c))
                return -1

    def touch(self,index: int, x: int, y: int):
        return self.dnld(index, 'input tap %d %d' % (x, y))

    def parseTime(self,img):
        text = pytesseract.image_to_string(Image.fromarray(img), lang="eng",config="-c tessedit_char_whitelist=0123456789: -psm 6")
        logging.info(text)
        text = text.strip().replace("\n", "")
        logging.info("获取出征时间文本：{}".format(text))
        sec = 180
        if len(text) == 8 and text[2] == ":" and text[5] == ":":
            logging.info(text)
            sec = (int(text[0]) * 10 + int(text[1])) * 3600 + (int(text[3]) * 10 + int(text[4])) * 60 + (
                        int(text[6]) * 10 + int(text[7]))
            sec = (sec) * 2
        else:
            logging.info("解析出征时间出错：{}".format(text))
        return sec

    def find_pic(self,src,temp):
        threshold = 0.99
        res = cv2.matchTemplate(src, temp, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        pt = loc[::-1]
        if len(pt[0]) > 0 and len(pt[1]) > 0:
            tx = pt[0][0]
            ty = pt[1][0]
            return [tx, ty]
        else:
            return None
    # 获取可以攻打的坐标
    def getQianWangLoc(self,id: int):
        gray = self.take_pic(id)
        img2 = cv2.imread("utils/nor.png", 0)

        threshold = 0.99
        res = cv2.matchTemplate(gray, img2, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        pt = loc[::-1]
        if len(pt[0]) > 0 and len(pt[1]) > 0:
            tx = pt[0][0] + 105
            ty = pt[1][0] + 90
            return [tx, ty]
        else:
            logging.info('未找到目标区域,返回默认值')
            return [813, 588]

    def searchBtn(self,id: int):
        # 1、判断是不是城外
        a = 0
        logging.info("开始截屏")
        mainImg = self.take_pic(id)
        logging.info("截屏结束")
        tianxiaTag = mainImg[19:148, 13:146]
        worldTag = cv2.imread("utils/world.png", 0)
        buf = self.check_pic(tianxiaTag, worldTag)
        logging.info("主城外图标的偏移:{}".format(buf))
        if buf < 10000:
            logging.info("确认是在城外，满足打野条件")
            # 点击搜索
            if expIds.count(id):
                self.touch(id, 80, 1550)
            else:
                self.touch(id, 81, 1376)
            time.sleep(0.3)
            return True
        return False

    # def execute(self,id:int):
    #     c=0
    #     while True:
    #         try:
    #             logging.info("index:{},第{}此开始启动".format(id,c))
    #             ret = self.startOrRestart(id)
    #             logging.info("index:{},模拟器启动结果：{},启动次数：{}".format(id,ret,c))
    #             if ret is None or ret == 0:
    #                 break
    #         except BaseException as e:
    #             logging.info("index:{} 启动异常，清错重试：{}".format(id,c))
    #             logging.error(e, exc_info=True, stack_info=True)
    #             self.processEx(id)
    #             c += 1
    #             time.sleep(2)
    #         if c >4 :
    #             return 0
    #     try:
    #         if id != 10 and id !=11:
    #             self.backKuangdui(id,True)
    #     except BaseException as e:
    #         logging.error(e, exc_info=True, stack_info=True)
    #     c=0
    #     while True:
    #         try:
    #             ret =  self.wakuang(id)
    #             logging.info("index:{} 执行挖矿结果：{}，次数：{}".format(id,ret,c))
    #             if ret == -1:
    #                 raise Exception()
    #             if ret == -2:
    #                 logging.info("index:{},挖矿执行完成，重启次数：{}".format(id, c))
    #                 return 0
    #         except BaseException as e:
    #             logging.info("index:{} 挖矿，清错重试：{}".format(id,c))
    #             logging.error(e, exc_info=True, stack_info=True)
    #             self.processEx(id)
    #             c += 1
    #             time.sleep(1)
    #         if c >6 :
    #             return 0

    def execute(self,id: int):
        c = 0
        while True:
            try:
                logging.info("index:{},第{}此开始启动".format(id, c))
                ret = self.startOrRestart(id)
                logging.info("index:{},模拟器启动结果：{},启动次数：{}".format(id, ret, c))
                if ret is None or ret == 0:
                    break
            except BaseException as e:
                logging.info("index:{} 启动异常，清错重试：{}".format(id, c))
                logging.error(e, exc_info=True, stack_info=True)
                self.processEx(id)
                c += 1
                time.sleep(2)
            if c > 4:
                return 0
        try:
            unBackIds=ast.literal_eval(self.cf.get("used-device","un_back_ids"))
            if id not in unBackIds:
                self.backKuangdui(id, True)
        except BaseException as e:
            logging.error(e, exc_info=True, stack_info=True)
        c = 0
        while True:
            try:
                ret = self.wakuang(id)
                logging.info("index:{} 执行挖矿结果：{}，次数：{}".format(id, ret, c))
                if ret == -1:
                    raise Exception()
                if ret == -2:
                    logging.info("execute waKuang|index:{},挖矿执行完成，重启次数：{}".format(id, c))
                    #记录挖矿剩余时间
                    self.recordKuangduiTime(id)
                    return 0
            except BaseException as e:
                logging.info("index:{} 挖矿，清错重试：{}".format(id, c))
                logging.error(e, exc_info=True, stack_info=True)
                self.processEx(id)
                c += 1
                time.sleep(1)
            if c > 6:
                return 0
    def recordKuangduiTime(self, id: int):
        self.take_pic(id)
        time.sleep(1)
        imgs = cv2.imread(share_path + '/apk_scr_' + str(id) + '.png', 0)
        minTime=20000;
        for i in range(4):
            y0 = 454 + i * 75
            y1 = 517 + i * 75
            y2 = 486 + i * 75
            temp1 = imgs[y0:y1, 232:339]
            text = pytesseract.image_to_string(Image.fromarray(temp1), lang="chi_sim")
            text = text.strip().replace("\n", "")
            logging.info(text)
            if text == '返回':
                tm = imgs[y2:y1, 95:212]
                retval, dst = cv2.threshold(tm, 127, 255, cv2.THRESH_BINARY)
                t = self.parseTime(dst)
                t = int(t / 2)
                if t == 90:
                    cv2.imwrite("backup/time_" + str(id) + "_" + str(i) + ".png", tm)
                logging.info("index：{} 剩余挖矿时间：{}".format(id, t))
                if t<minTime:
                    minTime=t
        cur_t=int(time.time())
        self.cf.set("kuang-time-conf", "device_"+str(id), str(int(cur_t+minTime+120)))
        self.cf.write(open(self.cf_file, 'w'))
        logging.info("index:{} 记录挖矿时间完成,剩余最少时间为：{}".format(id,minTime))
        return 0
    def backKuangdui(self,id:int,isBack:bool):
        self.take_pic(id)
        time.sleep(1)
        imgs = cv2.imread(share_path + '/apk_scr_' + str(id) + '.png', 0)
        count = 0
        for i in range(4):
            y0 = 454 + i * 75
            y1 = 517 + i * 75
            y2 = 486 + i * 75
            temp1 = imgs[y0:y1, 232:339]
            text = pytesseract.image_to_string(Image.fromarray(temp1), lang="chi_sim")
            text = text.strip().replace("\n", "")
            logging.info(text)
            if text == '返回':
                tm = imgs[y2:y1, 95:212]
                retval, dst = cv2.threshold(tm, 127, 255, cv2.THRESH_BINARY)
                t = self.parseTime(dst)
                t = int(t / 2)
                if t == 90:
                    cv2.imwrite("backup/time_" + str(id) + "_" + str(i) + ".png", tm)
                logging.info("index：{} 剩余挖矿时间：{},isBack:{}".format(id,t,isBack))
                if t < 1800 and isBack:
                    self.touch(id, 250, y2)
                    time.sleep(1)
                    self.touch(id, 700, 1200)
                else:
                    count += 1
        return count
if __name__ == '__main__':
    print(None == "123")
    player = SG_Player(None, None)
    lst=os.listdir("D:/idea_python/Demo-kuang/game/backup")
    for i in lst:
        print(i)
        tm = cv2.imread("D:/idea_python/Demo-kuang/game/backup/"+i)
        player.parseTime(tm)


