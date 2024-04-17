import pandas as pd


def calculate_convert(score, source_range, target_range):
    if pd.isnull(score) or score == 0:
        return None
    source_min, source_max = source_range
    target_min, target_max = target_range
    converts = (target_max * (score - source_min) + target_min * (source_max - score)) / (source_max - source_min)
    return converts


def main():
    import numpy as np
    # np.random.seed(21)
    # data = {
    #     '姓名': [f'学生{i}' for i in range(1, 1001)],
    #     'math_score': np.random.randint(5, 95, size=1000)}

    df = pd.read_excel('E:/库/桌面/考生成绩明细_玉林中学.xlsx', sheet_name='Sheet1')
    subject = '生物'

    # 将无效数据标记为 NaN
    df[subject] = pd.to_numeric(df[subject], errors='coerce')
    # 标记小于等于0的数值为 NaN
    df.loc[(df[subject] <= 0), subject] = None

    # 计算每个学生的排名百分比
    df['grade'] = pd.qcut(df[subject], [0, 0.02, 0.15, 0.5, 0.85, 1], labels=['E', 'D', 'C', 'B', 'A'])

    # 统计每个等级的最高分和最低分
    grade_ranges = {}
    for grade, group in df.groupby('grade'):
        grade_ranges[grade] = (group[subject].max(), group[subject].min())

    print(grade_ranges)

    # 每个等级的目标分数区间
    target_ranges = {'A': (100, 86), 'B': (85, 71), 'C': (70, 56), 'D': (55, 41), 'E': (40, 30)}
    # 如果分数为缺考或0，则没有等级，没有等级就无法获取原始分和目标分的分数区间，可以加个判断

    df[f'{subject}赋分'] = df.apply(
        lambda row: calculate_convert(row[subject],
                                      grade_ranges[row['grade']],
                                      target_ranges[row['grade']])
        if pd.notnull(row[subject]) else None,
        axis=1)

    print(df)

    df.to_excel('E:/库/桌面/考生成绩明细_玉林中学_转换.xlsx', index=False)


if __name__ == "__main__":
    main()

