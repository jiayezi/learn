from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'convert/index.html')


def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        # 保存文件到服务器的逻辑
        # 可以是保存到某个目录，或者保存到数据库中
        # 示例仅打印文件名
        print(uploaded_file.name)
        return HttpResponse("文件上传成功")
    return HttpResponse("无效的请求")



# def upload_file(request):
#     print(0)
#     if request.method == 'POST' and request.FILES['myfile']:
#         myfile = request.FILES['myfile']
#         # 处理上传的文件，比如保存到服务器上的某个位置
#         with open('uploaded_files/' + myfile.name, 'wb+') as destination:
#             for chunk in myfile.chunks():
#                 destination.write(chunk)
#         return render(request, 'convert/upload_success.html')
#     return render(request, 'convert/upload_file.html')
