# coding=utf-8

import xlrd,time,random
from func import get_info
from xlutils.copy import copy

# 设置表格路径
xlspath = 'F:/暂存/USB Drive/0715/zhtb/Docs/财务信控资料/cp.xls'

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
    info = None
    corpname = table.cell(i, 0).value
    while info == None:
        info = get_info(corpname)
        # 随机延迟sec秒再请求
        sec = random.randint(0, 9)
        print('延迟==================[' + sec.__str__() + 's]')
        time.sleep(sec)

    if info['hasRecord'] == True:
        # 社会信用编号
        ws.write(i, 14, info['uniscId'])
        # 成立日期
        ws.write(i, 15, info['estDate'])
        # 登记状态
        ws.write(i, 16, info['corpStatusString'])
        # 法人
        ws.write(i, 17, info['legelRep'])
        # 注册资本
        ws.write(i, 18, info['regCap'])
        # 股本结构
        ws.write(i, 19, info['inv'])

        # 保存行
        wb.save(xlspath)
    else:
        continue




