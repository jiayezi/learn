import os
from django.db import models


class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploaded_files/')

    def delete(self, *args, **kwargs):
        if self.file:
            # 删除文件系统中的文件
            if os.path.exists(self.file.path):
                os.remove(self.file.path)
        super(UploadedFile, self).delete(*args, **kwargs)
