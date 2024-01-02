import configparser
import datetime
import os
import sys
import time

sys.path.append("D:\\idea_python\\Demo-kuang")
from game.cityTask.city import doTask
from game.liukou.liukou import checkLiuKou
from game.login.doLogin import login
from game.logutils.mylog import log
import ast

from game.utils.tools import processEx, getLDMem, quitDn, get_list, searchBtn, getNum, touch
from game.wakuang.kuang import wakuang
from game.loopTask.Player import SG_Player

isExecOther = True


def startOrRestart(id: int):

    print("{} device {} is starting to execute task".format(time.strftime('%m-%d %H:%M:%S', time.localtime(time.time())),id))
    ret = login(id)
    exc = 0
    while True:
        if exc > 3:
            log("app：{} 进入游戏异常，切换下一个app".format(id))
            return -2
        if ret == -1:
            exc += 1
            processEx(id)
            time.sleep(1)
            ret = login(id)
        else:
            log("进入游戏成功")
            return ret


def checkAndExecWakuang(cf, pl,cur_id):
    item = cf.options("kuang-time-conf")
    #不执行挖矿的设备ids
    unWKIds=ast.literal_eval(cf.get("used-device", "un_wk_ids"))
    for i in item:
        index = int(i.split("_")[1])
        if index in unWKIds or index == cur_id:
            continue
        v = int(cf.get("kuang-time-conf", i))
        t = int(time.time())
        if t > v:
            pl.execute(index)
            pl.quitDn(index)
    return 0


def startTask(file, parse, player):
    try:
        id = (int)(parse.get("device-conf", "id"))
        global isExecOther
        lastCityTaskHour = 0
        lastCityTaskMin = 0
        r = startOrRestart(id)
        r = 0
        if -2 == r:
            quitDn(id)
            lst = get_list()
            unTaskIds = ast.literal_eval(parse.get("used-device", "un_task"))
            id = id + 1
            while True:
                if id in unTaskIds:
                    id = id + 1
                else:
                    break
            if id > len(lst) - 1:
                id = 0
            parse.set("device-conf", "id", str(int(id)))
            parse.write(open(file, 'w'))
            return
        print("login is successed")
        exc = 0
        while True:
            parse.read(file)
            fnm = parse.get("device-conf", "fightNm")
            waitWuKao = parse.get("device-conf", "waitWuKao")
            wuKaoDate = parse.get("device-conf", "wuKaoDate")
            otherDevices = parse.get("device-conf", "otherDevices")
            exNMIds = ast.literal_eval(parse.get("used-device", "un_nanMan_ids"))
            pause = parse.get("device-conf", "pause")
            cityTask = parse.get("device-conf", "cityTask")
            log("load conf：id={},pasue:{},fightNm={},waitWuKao={},wuKaoDate={},cityTask:{},isExecOther={}".format(id,
                                                                                                                  pause,
                                                                                                                  fnm,
                                                                                                                  waitWuKao,
                                                                                                                  wuKaoDate,
                                                                                                                  cityTask,
                                                                                                                  isExecOther))
            if int(pause) == 0:
                reboot = getLDMem()
                if reboot:
                    return
                time.sleep(0.3)
                checkLiuKou(id, waitWuKao, wuKaoDate)
                time_now = datetime.datetime.now()
                hour_now = time_now.hour
                min_now = time_now.minute
                log("上一次执行城市任务的时间=>{}：{}".format(lastCityTaskHour, lastCityTaskMin))
                if hour_now == 0:
                    lastCityTaskHour = 0
                gap_hour = hour_now - lastCityTaskHour
                gap_min = min_now - lastCityTaskMin
                if gap_min < 0:
                    gap_min = 60 + gap_min
                if int(cityTask) == 0 and (gap_hour > 1 or gap_min > 30):
                    res = doTask(id)
                    if res == -1:
                        processEx(id)
                    else:
                        lastCityTaskHour = hour_now
                        lastCityTaskMin = min_now
                    log("执行联盟任务:{}".format(res))
                ret = wakuang(id, fnm, waitWuKao, wuKaoDate,exNMIds)
                if ret != -1:
                    # 查看是否切换id
                    tempRet = searchBtn(id)
                    if tempRet:
                        hjText = getNum(id, 2)
                        if len(hjText) == 1:
                            hjNum = int(hjText[0])
                        if len(hjText) == 2:
                            hjNum = int(hjText[0]) * 10 + int(hjText[1])
                        touch(id, 54, 47)
                        time.sleep(1)
                        if hjNum < 6:
                            player.recordKuangduiTime(id)
                            quitDn(id)
                            lst = get_list()
                            unTaskIds = ast.literal_eval(parse.get("used-device", "un_task"))
                            id = id + 1
                            while True:
                                if id in unTaskIds:
                                    id = id + 1
                                else:
                                    break
                            if id > len(lst) - 1:
                                id = 0
                            parse.set("device-conf", "id", str(int(id)))
                            parse.write(open(file, 'w'))
                            return
                # 检查是否有需要挖矿的
                checkAndExecWakuang(parse, player,id)
                # gap = int(parse.get("device-conf", "execute_gap"))
                # if gap != 0:
                #     cur_t = int(time.time())
                #     gap = cur_t - gap
                #     if gap > 5400 and int(otherDevices):
                #         quitDn(id)
                #         log("开始执行其他用户挖矿")
                #         execOtherDevice(player)
                #         log("执行其他用户挖矿完成")
                #         t = time.time()
                #         parse.set("device-conf", "execute_gap", str(int(t)))
                #         lst = get_list()
                #         id = id + 1
                #         while True:
                #             if id == 4 or id == 5:
                #                 id = id + 1
                #             else:
                #                 break
                #
                #         if id == 12 or id > len(lst) - 1:
                #             id = 0
                #         parse.set("device-conf", "id", str(int(id)))
                #         parse.write(open(file, 'w'))
                #         return
                if ret == -1:
                    exc += 1
                    processEx(id)
                else:
                    exc = 0
                    log("index:{} 需要等待队伍返回|cost：{}".format(id,ret))
                    time.sleep(ret)
                if exc > 10:
                    log("游戏中运行异常，重新启动app")
                    return
                log("打野任务总计花费时间：{}，isExecOther={}".format(ret, isExecOther))
            else:
                log("当前系统处于暂停状态")
                time.sleep(300)
        return 0
    except BaseException:
        log("系统运行出错，重新启动app")
        return -1


def execOtherDevice(pl):
    lst = get_list()
    for index in range(len(lst)):
        if index == 5:
            continue
        pl.execute(index)
        pl.quitDn(index)
    return 0


def execAllDevice(cf, pl):
    lst = get_list()
    un_wk_ids = ast.literal_eval(cf.get("used-device", "un_wk_ids"))
    for index in range(len(lst)):
        if index in un_wk_ids:
            continue
        pl.execute(index)
        pl.quitDn(index)
    return 0


def test(config_file, parse):
    i = "device_" + str(7)
    v = int(parse.get("kuang-time-conf", i))
    t = int(time.time())
    id = int(i.split("_")[1])
    print(t > v)
    print(id)
    unTaskIds = ast.literal_eval(parse.get("used-device", "un_task"))
    item = cf.options("time-conf")
    for i in item:
        v = int(cf.get("time-conf", i))
        t = int(time.time())
        print(t - v)
    print(item)


if __name__ == '__main__':
    # 获取当前路径
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    config_file = curr_dir + os.sep + "config.ini"
    # 合成完整路径
    cf = configparser.ConfigParser()
    cf.read(config_file)
    player = SG_Player(config_file, cf)
    while True:
        res = startTask(config_file, cf, player)
        time.sleep(5)
