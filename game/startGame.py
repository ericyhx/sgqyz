import configparser
import datetime
import os
import sys
import time
sys.path.append("D:\\idea_python\\Demo")
from game.cityTask.city import doTask
from game.liukou.liukou import checkLiuKou
from game.login.doLogin import login
from game.logutils.mylog import log
from game.loopTask.fightTask import gongji

from game.utils.tools import processEx, getLDMem, quitDn
from game.wakuang.kuang import wakuang, singleWK

isExecOther=True

def startOrRestart(id: int,device: int):
    ret=login(id,device)
    exc=0
    while True:
        if exc >5:
            log("进入游戏异常，重新启动app")
            ret=login(id,device)
        if ret==-1:
            exc+=1
            ret=processEx(device)
            time.sleep(1)
        else:
            log("进入游戏成功")
            break

def startTask(id,device,fnm,file,parse,waitWuKao,wuKaoDate,otherDevices):
    try:
        global isExecOther
        lastCityTaskHour=0
        lastCityTaskMin=0
        # startOrRestart(id,device)
        exc=0
        while True:
            parse.read(file)
            pause=parse.get("device-conf","pause")
            cityTask=parse.get("device-conf","cityTask")
            log("当前系统配置状态：pasue:{},cityTask:{},isExecOther={}".format(pause,cityTask,isExecOther))
            if int(pause)==0:
                reboot=getLDMem()
                if reboot:
                    return
                time.sleep(0.3)
                # checkLiuKou(device,waitWuKao,wuKaoDate)
                time_now=datetime.datetime.now()
                hour_now=time_now.hour
                min_now=time_now.minute
                log("上一次执行城市任务的时间=>{}：{}".format(lastCityTaskHour,lastCityTaskMin))
                if hour_now==0:
                    lastCityTaskHour=0
                gap_hour=hour_now-lastCityTaskHour
                gap_min=min_now-lastCityTaskMin
                if gap_min<0:
                    gap_min=60+gap_min
                if int(cityTask)==0 and (gap_hour>1 or gap_min >30):
                    res=doTask(device)
                    if res==-1:
                        processEx(device)
                    else:
                        lastCityTaskHour=hour_now
                        lastCityTaskMin=min_now
                    log("执行联盟任务:{}".format(res))
                ret=wakuang(device,fnm,waitWuKao,wuKaoDate)
                gap=hour_now%3
                log("打野任务总计花费时间：{}，isExecOther={}，hour_now={},gap={}".format(ret,isExecOther,hour_now,gap))
                if int(otherDevices) and gap==0 and isExecOther:
                    isExecOther=False
                    quitDn(id)
                    execOtherDevice()
                    startOrRestart(id,device)
                else:
                    if gap !=0:
                        isExecOther=True
                    if ret==-1:
                        exc+=1
                        processEx(device)
                    else:
                        exc=0
                        time.sleep(ret)
                        # cur=datetime.datetime.now()
                        # h=cur.hour
                        # m=cur.minute
                        # if ret ==300 and h>8 and (h < 23 or (h == 23 and m < 50)):
                        #     gongji()
                        # else:
                        #     time.sleep(ret)
                    if exc>10:
                        log("游戏中运行异常，重新启动app")
                        return
            else:
                log("当前系统处于暂停状态")
                time.sleep(300)
        return 0
    except BaseException:
        log("系统运行出错，重新启动app")
        return -1

def execOtherDevice():
    idLst=[2]
    deviceLst=[5558]
    for i in range(len(idLst)):
        c=1
        while c<4:
            try:
                startOrRestart(idLst[i],deviceLst[i])
                while True:
                    result=singleWK(deviceLst[i])
                    if result == -1:
                        break
                    time.sleep(1)
                # quitDn(idLst[i])
                time.sleep(1)
                log("index :{} device:{} 执行挖矿结束,执行次数：{}".format(idLst[i],deviceLst[i],c))
                break
            except BaseException:
                quitDn(idLst[i])
                time.sleep(1)
                log("index :{} device:{} 执行挖矿失败,失败次数：{}".format(idLst[i],deviceLst[i],c))
                c=c+1
    for i in range(len(idLst)):
        quitDn(idLst[i])
        time.sleep(1)
        log("关闭设备id:{},设备：{}".format(idLst[i],deviceLst[i]))
    return 0




if __name__ == '__main__':
    # 获取当前路径
    curr_dir = os.path.dirname(os.path.realpath(__file__))

    # 合成完整路径
    config_file = curr_dir + os.sep + "config.ini"
    cf = configparser.ConfigParser()
    cf.read(config_file)
    id=cf.get("device-conf","id")
    device=cf.get("device-conf","device")
    fnm=cf.get("device-conf","fightNm")
    waitWuKao=cf.get("device-conf","waitWuKao")
    wuKaoDate=cf.get("device-conf","wuKaoDate")
    otherDevices=cf.get("device-conf","otherDevices")
    log("load conf：id={},device={},fightNm={},waitWuKao={},wuKaoDate={}".format(id,device,fnm,waitWuKao,wuKaoDate))    
    while True:
            res=startTask(id,device,fnm,config_file,cf,waitWuKao,wuKaoDate,otherDevices)
            time.sleep(5)



