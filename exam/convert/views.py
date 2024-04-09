from openpyxl import load_workbook
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UploadFileForm
from .models import UploadedFile, ConvertConfig
from django.http import FileResponse

possible_subjects = ('语文', '数学', '数学文', '数学理', '英语', '外语', '政治', '历史', '地理', '物理', '化学',
                     '生物', '总分', '总成绩', '全科')


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


def index(request):
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

            # 将title再次存储到session中。redirect函数默认会将重定向的请求视为全新的请求，这意味着会创建一个新的session，而不是继续使用原始请求的session。这可能会导致在新的请求中无法访问到之前存储在session中的数据。
            request.session['title'] = request.session['title']
            request.session['student_list'] = request.session['student_list']
            # 重定向并添加查询参数来指示成功上传，添加文件 ID 作为查询参数
            return redirect(f'{request.path}?success=1&file_id={uploaded_file.id}')
    else:
        form = UploadFileForm()
    return render(request, 'convert/index.html', {'form': form})


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
        print(title)
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
    # rate_exceed = []
    # rate_dist = []
    # grade_dict = {}
    # with open(f'conf/{cbox.get()}', 'rt', encoding='utf8') as f:
    #     data = f.read()
    # row_list = data.split('\n')
    # rate_sum = 0
    # for index, row in enumerate(row_list):
    #     value_list = row.split('\t')
    #     grade_dict[index] = value_list[0]
    #     rg = (float(value_list[1]), float(value_list[2]))
    #     rate_dist.append(rg)
    #     rate_sum += float(value_list[3])
    #     value = (100 - rate_sum) / 100.0
    #     rate_exceed.append(value)

    # uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    # # 检查文件是否存在
    # if uploaded_file.file and os.path.exists(uploaded_file.file.path):
    #     # 使用 openpyxl 打开 Excel 文件
    #     workbook = load_workbook(uploaded_file.file.path)
    #     # 对 Excel 文件进行修改
    #     # 例如，修改第一个工作表的 A1 单元格的值
    #     sheet = workbook.active
    #     sheet['A1'] = '修改后的值'
    #     # 保存修改后的 Excel 文件
    #     workbook.save(uploaded_file.file.path)
    #     # 构建带参数的 URL
    #     url = reverse('convert') + f'?success=1&file_id={uploaded_file.id}'
    #     # 重定向回上传页面，或返回一个成功修改的消息
    #     # return redirect(url)


def rank_page(request, file_id):
    pass
    return render(request, 'convert/rank_page.html')


def sum_page(request, file_id):
    pass
    return render(request, 'convert/sum_page.html')


def download_file(request, file_id):
    # 获取上传的文件对象
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)

    # 创建一个文件响应对象来发送文件给客户端
    response = FileResponse(uploaded_file.file.open('rb'))
    response['Content-Disposition'] = f'attachment; filename="{uploaded_file.file.name}"'

    return response


# 删除数据库中的所有文件记录和文件本身
# all_files = UploadedFile.objects.all()
# for f in all_files:
#     print(f.file)
#     f.delete()
