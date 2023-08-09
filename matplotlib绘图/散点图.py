from matplotlib import pyplot as plt
from win32com写报告.docx import loadXlsx

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 设置样式
plt.style.use('Solarize_Light2')
fig, ax = plt.subplots()

tableList = loadXlsx(r'F:\code\PythonProjects\项目交接资料\青岛学情检测报告\21年初中\教师\data\教师职业状态.xlsx')
for table in tableList:
    if table.name == '归属感和关系指数 全部':
        for row in table.rowList[::20]:
            ax.scatter(row[3], row[4], s=100)

# 添加散点图数据，参数s设置点的大小， 参数c和color设置点的颜色（两种方式：color=(1, 0, 0)，color='red'）
# ax.scatter(x_values, y_values, s=100, color=(1, 0, 1))

# 设置标题和坐标轴标签
ax.set_title('归属感和关系指数', fontsize=16)
ax.set_xlabel('学校归属感', fontsize=14)
ax.set_ylabel('同事关系', fontsize=14)
# 设置刻度标记的字号
ax.tick_params(axis='both', labelsize=14)
# 设置每个坐标轴的取值范围
# ax.axis([0, 1, 0, 1])

# 保存图片
# plt.savefig('img.png')
plt.show()
