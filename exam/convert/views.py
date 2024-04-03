from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import UploadedFile


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
            with row_data.file.open('rb') as file:
                file_content = file.read()
                # 处理文件内容，例如打印到控制台
                print(file_content)
            # 删除数据库中的当前文件记录和文件本身
            print('开始删除文件...')
            file.delete()
            print('删除成功')

            # 删除数据库中的所有文件记录和文件本身
            # all_files = UploadedFile.objects.all()
            # for f in all_files:
            #     print(f.file)
            #     f.delete()

            # return render(request, 'convert/index.html', {'form': form, 'message': '文件上传成功'})
            # 重定向到相同的 URL，避免文件重复上传
            # return redirect('index')
            # 重定向并添加查询参数来指示成功上传
            return redirect(f'{request.path}?success=1')
    else:
        form = UploadFileForm()
    return render(request, 'convert/index.html', {'form': form})


# def upload_file(request):
#     if request.method == 'POST' and request.FILES['myfile']:
#         myfile = request.FILES['myfile']
#         # 处理上传的文件，比如保存到服务器上的某个位置
#         with open('uploaded_files/' + myfile.name, 'wb+') as destination:
#             for chunk in myfile.chunks():
#                 destination.write(chunk)
#         return render(request, 'convert/upload_success.html')
#     return render(request, 'convert/upload_file.html')
