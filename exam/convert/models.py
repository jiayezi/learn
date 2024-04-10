from django.db import models
from django.contrib.auth.models import User


# class UploadedFile(models.Model):
#     file = models.FileField(upload_to='uploaded_files/')
#     upload_date = models.DateTimeField('Upload date', auto_now_add=True)
#
#     def delete(self, *args, **kwargs):
#         if self.file:
#             # 删除文件系统中的文件
#             if os.path.exists(self.file.path):
#                 os.remove(self.file.path)
#         super(UploadedFile, self).delete(*args, **kwargs)


class ConvertConfig(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    config_name = models.CharField(max_length=20)


class Grade(models.Model):
    config_name = models.ForeignKey(ConvertConfig, on_delete=models.CASCADE)
    grade_name = models.CharField(max_length=4)
    high_score = models.IntegerField()
    low_score = models.IntegerField()
    percent = models.IntegerField()
