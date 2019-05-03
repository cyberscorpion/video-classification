from django.db import models
import os
import re
from datetime import datetime

def directory_path(instance, filename):
    filename, file_extension = os.path.splitext(filename)
    return re.sub('[-:. ]','',str(datetime.today()))+file_extension


class File(models.Model):
    file = models.FileField(upload_to = directory_path,blank=False, null=False)
    remark = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)   
    
    def filename(self):
        return os.path.basename(self.file.name)