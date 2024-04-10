from django import forms
# from .models import UploadedFile


# class UploadFileForm(forms.ModelForm):
#     class Meta:
#         model = UploadedFile
#         fields = ['file']


class UploadFileForm(forms.Form):
    # 如果不上传文件到服务器，可以简单地创建一个空的表单类，不再需要继承forms.ModelForm，也不再需要file字段。
    # file = forms.FileField(label='选择文件')
    pass
