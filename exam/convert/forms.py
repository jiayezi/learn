from django import forms
from .models import ConvertConfig, Grade


# class UploadFileForm(forms.ModelForm):
#     class Meta:
#         model = UploadedFile
#         fields = ['file']


class UploadFileForm(forms.Form):
    # 如果不上传文件到服务器，可以简单地创建一个空的表单类，不再需要继承forms.ModelForm，也不再需要file字段。
    # file = forms.FileField(label='选择文件')
    pass


class ConvertConfigForm(forms.ModelForm):
    class Meta:
        model = ConvertConfig
        fields = ['config_name']
        labels = {'config_name': '配置名称'}


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['grade_name', 'high_score', 'low_score', 'percent']
        widgets = {
            'grade_name': forms.TextInput(attrs={'placeholder': '等级'}),
            'high_score': forms.NumberInput(attrs={'placeholder': '高分'}),
            'low_score': forms.NumberInput(attrs={'placeholder': '低分'}),
            'percent': forms.NumberInput(attrs={'placeholder': '占比'})
        }
