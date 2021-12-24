import os

console = 'D:\\LeiDian\\LDPlayer4.0\\ldconsole.exe '

def list_running() -> list:
    result = list()
    all = get_list()
    for dn in all:
        if dn.is_running() is True:
            result.append(dn)
    return result

def get_list():
    cmd = os.popen(console + 'list2')
    text = cmd.read()
    cmd.close()
    info = text.split('\n')
    result = list()
    for line in info:
        if len(line) > 1:
            dnplayer = line.split(',')
            # result.append(DnPlayer(dnplayer))
    return result

if __name__ == '__main__':
    # cmd = console + 'launch --index ' + str(2)
    # process = os.popen(cmd)
    # result = process.read()
    # process.close()
    print(get_list())