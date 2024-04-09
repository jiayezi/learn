from openpyxl import load_workbook, Workbook
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UploadFileForm
from .models import UploadedFile, ConvertConfig
from django.http import HttpResponse
from io import BytesIO


possible_subjects = ('语文', '数学', '数学文', '数学理', '英语', '外语', '政治', '历史', '地理', '物理', '化学',
                     '生物', '总分', '总成绩', '全科')


def sort_rule(score):
    """定义排序规则"""
    if isinstance(score, str) or score is None:
        return 0
    else:
        return float(score)


def open_file(request, file_id):
    """打开Excel，读取数据"""
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    wb = load_workbook(uploaded_file.file.path, read_only=True)
    ws = wb.active

    # 从session中获取或设置student_list和title
    if 'student_list' not in request.session:
        request.session['student_list'] = []
    if 'title' not in request.session:
        request.session['title'] = []

    student_list = request.session['student_list']
    title = request.session['title']
    # 清空现有数据
    title.clear()
    student_list.clear()

    # 存为对象
    student_list.clear()
    for i, row in enumerate(ws.values):
        if i == 0:
            title.extend(list(row))
            continue
        student_list.append({'row': list(row)})
    wb.close()


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            # print(uploaded_file.id, uploaded_file.file.name)
            # myfile = request.FILES['file']
            # print(myfile.name)

            # 读取当前文件
            # with uploaded_file.file.open('rb') as file:
            # 交给其他函数读取文件内容
            open_file(request, uploaded_file.id)

            # 如果使用redirect，需要将title再次存储到session中，因为redirect函数默认会将重定向的请求视为全新的请求，这意味着会创建一个新的session，而不是继续使用原始请求的session。这可能会导致在新的请求中无法访问到之前存储在session中的数据。
            # request.session['title'] = request.session['title']
            # request.session['student_list'] = request.session['student_list']

            return render(request, 'convert/index.html')
    else:
        form = UploadFileForm()
    return render(request, 'convert/upload_file.html', {'form': form})


def convert_page(request):
    if request.method == 'POST':
        # 获取被选中的下拉列表的值
        selected_config_name = request.POST.get('config')  # 获取用户提交的config_name
        # 获取被选中的复选框的值
        selected_items = request.POST.getlist('selected_items')
        # 交给其他函数处理数据
        convert(request, selected_config_name, selected_items)
        return redirect(request.path)
    else:
        # 根据需要获取或使用会话中的数据
        title = request.session.get('title', [])
        # student_list = request.session.get('student_list', [])
        subjects = []
        for i, item in enumerate(title):
            if item[:2] in possible_subjects:
                subjects.append(item)

        configs = ConvertConfig.objects.values_list('config_name', flat=True)

        context = {
            'items': subjects,
            'configs': configs,
        }
        return render(request, 'convert/convert_page.html', context)


def convert(request, config_name, selected_subject_name):
    """计算赋分成绩"""
    # 根据需要获取或使用会话中的数据
    title = request.session.get('title', [])
    student_list = request.session.get('student_list', [])

    # 查询数据库获取对应的ConvertConfig对象
    selected_config = ConvertConfig.objects.get(config_name=config_name)
    # 使用related_name获取关联的Grade对象列表
    grades = selected_config.grade_set.all()
    # 获取科目索引
    selected_subject_index = []
    for name in selected_subject_name:
        idx = title.index(name)
        selected_subject_index.append(idx)

    # 检查
    grade_info = ""
    for grade in grades:
        grade_info += f"等级: {grade.grade_name}, 高分: {grade.high_score}, 低分: {grade.low_score}, 占比: {grade.percent}\n"
    text = f'选择的科目：{", ".join(selected_subject_name)}\n'
    text += f'选择的配置：{selected_config}\n'
    text += f'配置详情：\n{grade_info}'
    print(text)

    # 加载配置文件，读取领先率、赋分区间和等级
    rate_exceed = []
    rate_dist = []
    grade_dict = {}
    rate_sum = 0
    for index, grade in enumerate(grades):
        grade_dict[index] = grade.grade_name
        rate_dist.append((grade.high_score, grade.low_score))
        rate_sum += grade.percent
        value = (100 - rate_sum) / 100.0
        rate_exceed.append(value)

    for sub_index, subject in enumerate(selected_subject_name):
        score_index = selected_subject_index[sub_index]
        student_list.sort(key=lambda x: sort_rule(x['row'][score_index]), reverse=True)

        # 获取得分大于0分的人数、获取大于0分的最小原始分
        student_data_reverse = student_list[::-1]
        student_num = len(student_data_reverse)
        min_score = 0.0
        for row_index, student in enumerate(student_data_reverse):
            if isinstance(student['row'][score_index], str) or student['row'][score_index] is None:
                continue
            if float(student['row'][score_index]) > 0.0:
                student_num -= row_index
                min_score = float(student['row'][score_index])
                break

        # 获取原始分等级区间
        rate_src = [[float(student_list[0]['row'][score_index])]]
        rate = (student_num - 1) / student_num
        previous_score = -1  # 上个分数，初始值为-1
        temp_dj = 0  # 初始等级和索引
        for row_index, student in enumerate(student_list):
            current_score_str = student['row'][score_index]
            if not isinstance(current_score_str, (int, float)):
                continue

            current_score = float(current_score_str)
            if current_score != previous_score:
                previous_score = current_score
                rate = (student_num - row_index - 1) / student_num  # 领先率
                for e_index, value in enumerate(rate_exceed):
                    # 如果这个学生的领先率大于rate_exceed里的某一个值，并且temp_dj与上次不同，就把当前分数添加到rate_src里面，然后结束内层循环。如果这个学生的领先率大于rate_exceed里的某一个值，并且temp_dj与上次相同，也要结束内层循环，所以break不能写在if内部。
                    if rate >= value:
                        if temp_dj != e_index:
                            temp_dj = e_index
                            rate_src[temp_dj - 1].append(
                                float(student_list[row_index - 1]['row'][score_index]))
                            rate_src.append([float(student['row'][score_index])])
                        break
        # rate_src[-1].append(float(student_data[-1][extra + i]))
        rate_src[-1].append(min_score)
        # print(f'{subject}原始分等级区间：{rate_src}')

        # 计算赋分成绩
        for student in student_list:
            score = student['row'][score_index]
            if not isinstance(score, (int, float)) or score == 0:
                student['row'].append('')
                student['row'].append('')
                continue
            xsdj = 0
            for index, dj_score in enumerate(rate_src):
                if dj_score[0] >= score >= dj_score[1]:
                    xsdj = index
                    break
            m = rate_src[xsdj][1]
            n = rate_src[xsdj][0]
            a = rate_dist[xsdj][1]
            b = rate_dist[xsdj][0]
            converts = (b * (score - m) + a * (n - score)) / (n - m)
            student['row'].append(grade_dict[xsdj])
            student['row'].append(round(converts))
        title.append(f'{subject}等级')
        title.append(f'{subject}赋分')

    # 将修改后的数据保存回session中
    request.session['title'] = title
    request.session['student_list'] = student_list


def rank_page(request, file_id):
    pass
    return render(request, 'convert/rank_page.html')


def sum_page(request, file_id):
    pass
    return render(request, 'convert/sum_page.html')


def download_file(request):
    # 获取或使用会话中的数据
    title = request.session.get('title', [])
    student_list = request.session.get('student_list', [])

    # 生成Excel文件
    wb = Workbook(write_only=True)
    ws = wb.create_sheet()
    ws.append(title)
    for student in student_list:
        ws.append(student['row'])

    # 将Excel数据写入BytesIO对象
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    # 构建HTTP响应以供下载
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="students.xlsx"'

    return response


# 删除数据库中的所有文件记录和文件本身
# all_files = UploadedFile.objects.all()
# for f in all_files:
#     print(f.file)
#     f.delete()
