from 连接数据库.data_base import DB
import openpyxl

# 创建工作簿对象
workbook = openpyxl.Workbook()
# 获得默认的工作表
sheet = workbook.active
# 修改工作表的标题
sheet.title = '基本信息'

title = []

with DB(host='120.78.9.140', user='root', passwd='qingandsql', database='myemployees') as db:
    db.execute('desc `employees`')
    for row in db:
        title.append(row[0])
    sheet.append(title)

    db.execute('select * from `employees`')
    for row in db:
        sheet.append(row)
    workbook.save('F:/用户目录/桌面/0.xlsx')

