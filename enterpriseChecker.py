# coding=utf-8

import xlrd,xlwt
import requests,json,time
from func import get_info
from xlutils.copy import copy

xlspath = '/Users/jackietsoi/Documents/workDirectory/zhtb/Docs/xk/cp.xls'
# 打开文件
data = xlrd.open_workbook(xlspath)

wb = copy(data)
# 利用xlutils.copy函数，将xlrd.Book转为xlwt.Workbook，再用xlwt模块进行存储

# 通过get_sheet()获取的sheet有write()方法
ws = wb.get_sheet(0)

# 通过文件名获得工作表,获取工作表1
table = data.sheet_by_name('Sheet1')

print("总行数：" + str(table.nrows))
print("总列数：" + str(table.ncols))

rowlist=[]
dictlist=[]
for i in range(table.nrows):

    if str(table.cell(i,10).value) == '内贸' and str(table.cell(i,14).value)=='':
        rowlist.append(i)

print(len(rowlist))

for i in rowlist:
    corpname=table.cell(i,0).value
    info=get_info(corpname)
    if info != None:
        # 社会信用编号
        ws.write(i, 14, info['uniscId'])
        ws.write(i, 15, info['estDate'])
        ws.write(i, 16, info['corpStatusString'])
        ws.write(i, 17, info['legelRep'])
        ws.write(i, 18, info['regCap'])
        ws.write(i, 19, info['inv'])

        wb.save('/Users/jackietsoi/Documents/workDirectory/zhtb/Docs/xk/cp.xls')
    else:
        continue



