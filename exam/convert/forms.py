from django import forms
from .models import UploadedFile


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']


# class UploadFileForm(forms.Form):
#     file = forms.FileField(label='选择文件')
