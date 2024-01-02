import configparser
import time

file_path='D:/idea_python/Demo-kuang/game/config.ini'
cf = configparser.ConfigParser()
cf.read(file_path)
Prompt = ''
while Prompt != 'save':
    Prompt = input("device_info: ")
    try:
        if Prompt == 'save':
            cf.write(open(file_path, 'w'))
            print('update success!')
            break
        data = Prompt.split(',')
        if len(data) != 3:
            print("输入的数据格式有问题，请检查！data=" + Prompt)
            continue

        deviceId = data[0]
        h = data[1]
        m = data[2]
        t = time.time()
        lastestTime = int(t) + int(h) * 3600 + int(m) * 60
        cf.set("kuang-time-conf", "device_" + deviceId, str(lastestTime))
        print('update device:' + str(deviceId) + ',lastestTime:' + str(lastestTime) + '\n')
    except:
        print('输入有误，重新输入！|data='+Prompt)

