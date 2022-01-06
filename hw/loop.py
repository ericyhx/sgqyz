import re,os

import psutil

def getLDMem():
    processName="LdVBoxHeadless.exe"
    pattern = re.compile(r'([^\s]+)\s+(\d+)\s.*\s([^\s]+\sK)')
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
        print("name:{}|pid:{}|used memory:{} MB".format(processName,pid,used))
        if used >3000:
            ret=True
    return ret




if __name__ == '__main__':
    print(getLDMem())