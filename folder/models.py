from django.db import models
from django.conf import settings


FOLDER_STORAGE_PATH = '/tmp'
if hasattr(settings, FOLDER_STORAGE_PATH):
    FOLDER_STORAGE_PATH = settings.FOLDER_STORAGE_PATH


class File(models.Model):
    """File, md5sum is used for deduplication and as name of file"""

    md5sum = models.CharField(max_length=32, unique=True, db_index=True)
    created = models.DateField(auto_now_add=True)
    size = models.PositiveIntegerField()

    @property
    def name(self):
        return '%s/%s' % (FOLDER_STORAGE_PATH, self.md5sum)


class FileLink(models.Model):
    """Link to file, one file can have many links of different users"""

    name = models.CharField(max_length=64, unique=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    target = models.ForeignKey('File', related_name='filelinks')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='files')

    def __unicode__(self):
        return 'Name: %s, Created: %s, Size: %d bytes' % (
            self.name, self.created.strftime('%d.%m.%Y %H:%M'),
            self.target.size)
