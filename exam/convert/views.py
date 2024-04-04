import os

import openpyxl
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UploadFileForm
from .models import UploadedFile
from django.http import FileResponse
from django.urls import reverse


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
            row_data = UploadedFile.objects.get(id=uploaded_file.id)
            # 读取文件内容
            # with row_data.file.open('rb') as file:
            #     file_content = file.read()
            #     # 处理文件内容，例如打印到控制台
            #     print(file_content)
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


def modify_file(request, file_id):
    # 获取上传的文件对象
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)

    # 检查文件是否存在
    if uploaded_file.file and os.path.exists(uploaded_file.file.path):
        # 使用 openpyxl 打开 Excel 文件
        workbook = openpyxl.load_workbook(uploaded_file.file.path)

        # 对 Excel 文件进行修改
        # 例如，修改第一个工作表的 A1 单元格的值
        sheet = workbook.active
        sheet['A1'] = '修改后的值'

        # 保存修改后的 Excel 文件
        workbook.save(uploaded_file.file.path)
        # 构建带参数的 URL
        url = reverse('index') + f'?success=1&file_id={uploaded_file.id}'

        # 重定向回上传页面，或返回一个成功修改的消息
        return redirect(url)


def download_file(request, file_id):
    # 获取上传的文件对象
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)

    # 创建一个文件响应对象来发送文件给客户端
    response = FileResponse(uploaded_file.file.open('rb'))
    response['Content-Disposition'] = f'attachment; filename="{uploaded_file.file.name}"'

    return response
