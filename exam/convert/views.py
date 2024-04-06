import os

from openpyxl import load_workbook
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UploadFileForm
from .models import UploadedFile
from django.http import FileResponse, HttpResponse
from django.urls import reverse

title = None
student_list = []
possible_subjects = ('语文', '数学', '数学文', '数学理', '英语', '外语', '政治', '历史', '地理', '物理', '化学',
                     '生物', '总分', '总成绩', '全科')


def open_file(file_id):
    """打开Excel，读取数据"""
    # info_text.set('正在读取数据')
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    wb = load_workbook(uploaded_file.file.path, read_only=True)
    ws = wb.active

    # 存为对象
    global title
    student_list.clear()
    for i, row in enumerate(ws.values):
        if i == 0:
            title = list(row)
            continue
        student_list.append({'row': list(row)})
    wb.close()


def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            print(uploaded_file.id, uploaded_file.file.name)
            # myfile = request.FILES['file']
            # print(myfile.name)

            # 读取当前文件
            # with uploaded_file.file.open('rb') as file:
            # 查找指定文件并读取
            # row_data = UploadedFile.objects.get(id=uploaded_file.id)
            # 读取文件内容
            open_file(uploaded_file.id)
            # 删除数据库中的当前文件记录和文件本身
            # print('开始删除文件...')
            # file.delete()
            # print('删除成功')

            # 删除数据库中的所有文件记录和文件本身
            # all_files = UploadedFile.objects.all()
            # for f in all_files:
            #     print(f.file)
            #     f.delete()

            # 重定向到相同的 URL，避免文件重复上传
            # return redirect('index')
            # 重定向并添加查询参数来指示成功上传，添加文件 ID 作为查询参数
            return redirect(f'{request.path}?success=1&file_id={uploaded_file.id}')
    else:
        form = UploadFileForm()
    return render(request, 'convert/index.html', {'form': form})


def convert_page(request, file_id):
    if request.method == 'POST':
        # 获取被选中的复选框的值
        selected_items = request.POST.getlist('selected_items')

        # 在这里进行进一步的处理，例如保存到数据库或执行其他操作
        # 例如，假设您想要将被选中的项目保存到数据库中：
        # for item in selected_items:
        #     MyModel.objects.create(name=item)

        # 返回一个简单的响应
        return HttpResponse("Selected items: " + ", ".join(selected_items))
    else:
        subjects = []
        for i, item in enumerate(title):
            if item[:2] in possible_subjects:
                subjects.append(item)

        context = {
            'items': subjects,
        }
        return render(request, 'convert/convert_page.html', context)


def convert(request, file_id):
    """计算赋分成绩"""
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
    return render(request, 'convert/convert_page.html')


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
