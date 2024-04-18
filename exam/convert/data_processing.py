from io import StringIO
import pandas as pd


def calculate_convert(score, source_range, target_range):
    # if pd.isnull(score) or score == 0:
    #     return None
    source_min, source_max = source_range
    target_min, target_max = target_range
    converts = (target_max * (score - source_min) + target_min * (source_max - score)) / (source_max - source_min)
    return round(converts)


def convert(request, selected_config_name, selected_items):
    df_json = request.session.get('df_json', [])
    df = pd.read_json(StringIO(df_json))

    for subject in selected_items:
        # 将无效数据标记为 NaN
        df[subject] = pd.to_numeric(df[subject], errors='coerce')
        # 标记小于等于0的数值为 NaN
        df.loc[(df[subject] <= 0), subject] = None

        grade_title = f'{subject}等级'

        # 计算每个学生的排名百分比
        df[grade_title] = pd.qcut(df[subject], [0, 0.02, 0.15, 0.5, 0.85, 1], labels=['E', 'D', 'C', 'B', 'A'])

        # 统计每个等级的最高分和最低分
        grade_ranges = {}
        for grade, group in df.groupby(grade_title, observed=True):
            grade_ranges[grade] = (group[subject].max(), group[subject].min())
        # print(grade_ranges)

        # 每个等级的目标分数区间
        target_ranges = {'A': (100, 86), 'B': (85, 71), 'C': (70, 56), 'D': (55, 41), 'E': (40, 30)}

        # 如果分数为缺考或0，则没有等级，没有等级就无法获取原始分和目标分的分数区间，可以加个判断
        df[f'{subject}赋分'] = df.apply(
            lambda row: calculate_convert(row[subject],
                                          grade_ranges[row[grade_title]],
                                          target_ranges[row[grade_title]])
            if pd.notnull(row[subject]) else None,
            axis=1)
    df_json = df.to_json()
    request.session['df_json'] = df_json

