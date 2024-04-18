from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UploadFileForm
from .models import ConvertConfig
from django.http import HttpResponse
from io import BytesIO, StringIO
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import ConvertConfigForm, GradeForm
import pandas as pd
from . import data_processing


possible_subjects = ('语文', '数学', '数学文', '数学理', '英语', '外语', '政治', '历史', '地理', '物理', '化学',
                     '生物', '总分', '总成绩', '全科')


def sort_rule(score):
    """定义排序规则"""
    if isinstance(score, str) or score is None:
        return 0
    else:
        return float(score)


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            # print(uploaded_file.id, uploaded_file.file.name)
            # 读取当前文件
            df = pd.read_excel(file)

            # 将数据存储到 session 中
            df_json = df.to_json()
            request.session['df_json'] = df_json
            request.session['file'] = True

            # 如果使用redirect，需要将title再次存储到session中，因为redirect函数默认会将重定向的请求视为全新的请求，这意味着会创建一个新的session，而不是继续使用原始请求的session。这可能会导致在新的请求中无法访问到之前存储在session中的数据。
            request.session['df_json'] = request.session['df_json']
            request.session['file'] = True
            return redirect('index')
            # return render(request, 'convert/index.html')
    else:
        form = UploadFileForm()
    return render(request, 'convert/upload_file.html', {'form': form})


def index(request):
    # 如果没有上传文件，就跳转到上传文件页面
    if request.session.get('file', False):
        return render(request, 'convert/index.html')
    else:
        message = '请先上传文档！'
        messages.error(request, message)  # 添加错误消息
        return redirect('upload_file')


def convert_page(request):
    if request.method == 'POST':
        # 获取被选中的下拉列表的值
        selected_config_name = request.POST.get('config')  # 获取用户提交的config_name
        # 获取被选中的复选框的值
        selected_items = request.POST.getlist('selected_items')
        # 交给其他函数处理数据
        data_processing.convert(request, selected_config_name, selected_items)
        return redirect(request.path)
    else:
        # 根据需要获取或使用会话中的数据
        df_json = request.session.get('df_json', [])
        # 使用StringIO对象包装JSON字符串，然后再读取
        df = pd.read_json(StringIO(df_json))
        subjects = []
        for i, item in enumerate(df.columns):
            if item[:2] in possible_subjects:
                subjects.append(item)

        if request.user.is_authenticated:
            # 如果用户已经登录，获取当前用户的数据和管理员的数据
            configs = ConvertConfig.objects.filter(
                Q(author=request.user) | Q(author__username='jiayezi')
            ).values_list('config_name', flat=True)
        else:
            # 如果用户没有登录，只获取jiayezi的数据
            configs = ConvertConfig.objects.filter(author__username='jiayezi').values_list('config_name', flat=True)

        context = {
            'items': subjects,
            'configs': configs,
        }
        return render(request, 'convert/convert_page.html', context)


def rank_page(request):
    if request.method == 'POST':
        # 获取被选中的复选框的值
        selected_subjects = request.POST.getlist('selected_subjects')
        selected_groups = request.POST.getlist('selected_groups')
        # 交给其他函数处理数据
        rank(request, selected_subjects, selected_groups)
        return redirect(request.path)
    else:
        # 根据需要获取或使用会话中的数据
        title = request.session.get('title', [])
        # student_list = request.session.get('student_list', [])
        subjects = []
        groups = []
        for item in title:
            if item[:2] in possible_subjects:
                subjects.append(item)
            else:
                groups.append(item)

        context = {
            'subjects': subjects,
            'groups': groups,
        }
    return render(request, 'convert/rank_page.html', context)


def rank(request, selected_subjects, selected_groups):
    print(selected_subjects)
    print(selected_groups)


def sum_page(request):
    if request.method == 'POST':
        # 获取被选中的复选框的值
        selected_subjects = request.POST.getlist('selected_subjects')
        selected_subjects2 = request.POST.getlist('selected_subjects2')
        # 交给其他函数处理数据
        score_sum(request, selected_subjects, selected_subjects2)
        return redirect(request.path)
    else:
        # 根据需要获取或使用会话中的数据
        title = request.session.get('title', [])
        # student_list = request.session.get('student_list', [])
        subjects = []
        for item in title:
            if item[:2] in possible_subjects:
                subjects.append(item)

        context = {
            'subjects': subjects,
        }
    return render(request, 'convert/sum_page.html', context)


def score_sum(request, selected_subjects, selected_subjects2):
    print(selected_subjects)
    print(selected_subjects2)
    pass


def download_file(request):
    # 获取或使用会话中的数据
    df_json = request.session.get('df_json', [])
    df = pd.read_json(StringIO(df_json))

    # 将Excel数据写入BytesIO对象
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    # 构建HTTP响应以供下载
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="students.xlsx"'

    return response


def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # 检查密码是否一致
        if password != confirm_password:
            return render(request, 'convert/register.html', {'error_message': '密码不匹配'})

        # 检查用户名是否已存在
        if User.objects.filter(username=username).exists():
            return render(request, 'convert/register.html', {'error_message': '该用户名已被注册'})

        # 创建用户
        user = User.objects.create_user(username=username, password=password)
        user.save()

        # 注册成功后
        login(request, user)
        return redirect('index')
    else:
        # 如果不是POST请求，则显示注册表单页面
        return render(request, 'convert/register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # 获取重定向目标，如果没有则重定向到默认页面
            redirect_to = request.GET.get('next', 'index')
            return redirect(redirect_to)
        else:
            # 登录失败的处理
            return render(request, 'convert/login.html', {'error_message': '无效的用户名或密码'})
    else:
        # 如果不是POST请求，则显示登录表单页面
        return render(request, 'convert/login.html')


def user_logout(request):
    logout(request)
    # 注销后重定向到某个页面
    return redirect('index')


@login_required
def config_list(request):
    configs = ConvertConfig.objects.filter(author=request.user)
    return render(request, 'convert/config_list.html', {'configs': configs})


@login_required
def create_config(request):
    if request.method == 'POST':
        config_form = ConvertConfigForm(request.POST)
        form_count = int(request.POST.get('form_count'))
        grade_forms = [GradeForm(request.POST, prefix=str(i)) for i in range(form_count)]
        if config_form.is_valid() and all(grade_form.is_valid() for grade_form in grade_forms):
            config = config_form.save(commit=False)
            config.author = request.user
            config.save()
            for grade_form in grade_forms:
                grade = grade_form.save(commit=False)
                grade.config_name = config
                grade.save()
            return redirect('config_list')
    else:
        config_form = ConvertConfigForm()
        grade_forms = [GradeForm(prefix=str(i)) for i in range(3)]  # 初始3个grade表单

    return render(request, 'convert/create_config.html', {'config_form': config_form, 'grade_forms': grade_forms})


@login_required
def modify_config(request, config_id):
    config = ConvertConfig.objects.get(pk=config_id)
    grade_forms = [GradeForm(instance=grade, prefix=str(i)) for i, grade in enumerate(config.grade_set.all())]

    if request.method == 'POST':
        config_form = ConvertConfigForm(request.POST, instance=config)
        form_count = int(request.POST.get('form_count'))
        grade_forms = [GradeForm(request.POST, prefix=str(i)) for i in range(form_count)]

        if config_form.is_valid() and all(grade_form.is_valid() for grade_form in grade_forms):
            config = config_form.save(commit=False)
            config.author = request.user
            config.save()

            # 从数据库中删除config关联的所有Grade数据
            for grade in config.grade_set.all():
                grade.delete()

            # 保存这个配置下的所有等级数据
            for grade_form in grade_forms:
                grade = grade_form.save(commit=False)
                grade.config_name = config
                grade.save()

            return redirect('config_list')
    else:
        config_form = ConvertConfigForm(instance=config)

    return render(request, 'convert/modify_config.html',
                  {'config': config, 'config_form': config_form, 'grade_forms': grade_forms})


@login_required
def delete_config(request, config_id):
    config = get_object_or_404(ConvertConfig, pk=config_id)
    if request.method == 'POST':
        config.delete()
        return redirect('config_list')  # Replace with your success URL
    return redirect('config_list')  # Redirect back to the list view if not a POST request




# 删除数据库中的所有文件记录和文件本身
# all_files = UploadedFile.objects.all()
# for f in all_files:
#     print(f.file)
#     f.delete()
