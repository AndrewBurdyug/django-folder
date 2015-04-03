from django.db import models
from django.conf import settings


FOLDER_STORAGE_PATH = '/tmp'
if hasattr(settings, FOLDER_STORAGE_PATH):
    FOLDER_STORAGE_PATH = settings.FOLDER_STORAGE_PATH


class File(models.Model):
    """File, md5sum is used for deduplication and as name of file"""

    md5sum = models.CharField(max_length=32)
    path = models.FilePathField(path=FOLDER_STORAGE_PATH)
    created = models.DateField(auto_now_add=True)

    @property
    def name(self):
        return '%s/%s' % (self.path, self.md5sum)


class FileLink(models.Model):
    """Link to file, one file can have many links of different users"""

    name = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)
    target = models.ForeignKey('File')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
