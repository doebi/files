from django.db import models
from django.contrib.auth.models import User

def getPath(f, n):
    return "%s/%s" % (f.folder.name, n)


class Folder(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=32)
    created = models.DateTimeField(auto_now=True)
    ACCESS_TYPES = (
        (True, 'public'),
        (False, 'private'),
    )
    name = models.CharField(max_length=8)
    is_public = models.BooleanField(choices=ACCESS_TYPES, default=False)
    def __unicode__(self):
        return self.name

class File(models.Model):
    name = models.CharField(max_length=8)
    dl_count = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now=True)
    data = models.FileField(upload_to=getPath)
    folder = models.ForeignKey('Folder')
