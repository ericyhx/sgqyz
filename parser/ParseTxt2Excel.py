import datetime
import os

# import openpyxl as xw
#
#
# def gongxian():
#     f=open("C:/Users/hello world/Desktop/tongji/gongxian.txt",encoding="UTF-8")
#     ret=f.readlines()
#     lst=[]
#     for i in range(ret.__len__()):
#         if ret[i] == '\n' or not len(ret[i]) or len(ret[i])==1:
#             continue
#         else:
#           line=ret[i].replace("\n",'')
#           ls=line.split("共赠送了")
#           lst.append(ls[0])
#     f.close()
#     return lst
#
# def parseName():
#     f=open("C:/Users/hello world/Desktop/tongji/name.txt",encoding="UTF-8")
#     ret=f.readlines()
#     lst=[];
#     for i in range(len(ret)):
#         if ret[i] == '\n' or not len(ret[i]) or len(ret[i])==1:
#             continue
#         else:
#             lst.append(ret[i].replace("\n",""))
#     return lst;
# def exportExcel():
#     fileName='C:/Users/hello world/Desktop/tongji/baoxinggongxian.xlsx'
#     if not os.path.exists(fileName):
#         workbook=xw.Workbook()
#         sheet=workbook.active
#         title=['序号','角色','星期一','星期二','星期三','星期四','星期五','星期六','星期日']
#         sheet.append(title)
#         names=parseName()
#         for i in range(len(names)):
#             _=sheet.cell(i+2,1,i+1)
#             _=sheet.cell(i+2,2,names[i])
#         workbook.save(fileName)
#         ret=gongxian()
#         weedday=datetime.datetime.now().weekday()
#         for rx in range(1,sheet.max_row+1):
#             name=sheet.cell(rx,2).value
#             if ret.__contains__(name):
#                 sheet.cell(rx,3+weedday,1)
#         workbook.save(fileName)
#     else:
#         workbook=xw.load_workbook(fileName)
#         ws=workbook.active
#         ret=gongxian()
#         weedday=datetime.datetime.now().weekday()
#         for rx in range(1,ws.max_row+1):
#             name=ws.cell(rx,2).value
#             if ret.__contains__(name):
#                 ws.cell(rx,3+weedday,1)
#         workbook.save(fileName)
#     workbook.close()
import time
if __name__ == '__main__':
   t = time.time()
   print(int(t)+3*3600+0*60)
