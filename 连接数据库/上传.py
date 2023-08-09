import os
from 连接数据库.data_base import DB
from win32com import client

"""
把excel表格的数据上传到数据库，速度非常慢！
"""


class XlsxTable:
    def __init__(self):
        self.name = ''
        self.titleList = []
        self.rowList = []


def loadXlsx(filename):
    table_list = []
    excel = client.Dispatch("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False
    wb = excel.Workbooks.Open(filename, True)  # 以只读模式打开工作簿
    # 取每个工作表的数据
    for sheet in wb.Sheets:
        table = XlsxTable()
        table.name = sheet.Name
        ws = wb.Worksheets(sheet.Name)
        # 获取有数据的区域, 返回为一个二维元组
        data_range = ws.Range(ws.Cells(1, 1), ws.Cells(ws.UsedRange.Rows.Count, ws.UsedRange.Columns.Count)).Value
        table.titleList = data_range[0]
        table.rowList = data_range[1:]
        table_list.append(table)

    wb.Close()
    excel.Quit()
    return table_list


path = 'F:/用户目录/桌面/语文.xlsx'
full_name = os.path.basename(path)
file_name = full_name[:full_name.find('.')].strip()

table_list = loadXlsx(path)
table = table_list[0]


with DB(host='120.78.9.140', user='root', passwd='qingandsql', database='exam') as db:
    # 检查表是否存在，不存在才创建
    db.execute('show tables;')
    flag = False
    for t in db:
        if t[0] == file_name:
            flag = True
            break

    if not flag:
        title = list(table.titleList)
        for i, n in enumerate(title):
            if isinstance(n, float):
                title[i] = int(n)

        num_title = title[3:]
        text = ''
        for t in num_title:
            text += f'小题{t} int,'
        text = text[:-1]

        sql = f'create table {file_name}({title[0]} varchar(16),{title[1]} varchar(16),{title[2]} varchar(100),{text});'
        db.execute(sql)

    # 上传
    for row in table.rowList:
        line = list(row)
        for i, cell in enumerate(line):
            line[i] = f'"{cell}"'
        text = ','.join(line)
        sql = f'insert into {file_name} values({text});'
        db.execute(sql)


