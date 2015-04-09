from django.db import models
from django.conf import settings


FOLDER_STORAGE_PATH = '/tmp'
if hasattr(settings, 'FOLDER_STORAGE_PATH'):
    FOLDER_STORAGE_PATH = settings.FOLDER_STORAGE_PATH


class File(models.Model):
    """File, md5sum is used for deduplication and as name of file"""

    md5sum = models.CharField(max_length=32, unique=True, db_index=True)
    created = models.DateField(auto_now_add=True)
    size = models.PositiveIntegerField()
    content_type = models.ForeignKey('FileContentType', related_name='files',
                                     blank=True, null=True)

    @property
    def name(self):
        return '%s/%s' % (FOLDER_STORAGE_PATH, self.md5sum)

    def __unicode__(self):
        return self.name


class FileLink(models.Model):
    """Link to file, one file can have many links of different users"""

    name = models.CharField(max_length=64, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    target = models.ForeignKey('File', related_name='filelinks')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='files')
    shared = models.OneToOneField('FileSharedLink', related_name='filelink',
                                  blank=True, null=True)
    directory = models.ForeignKey('Directory', related_name='filelinks',
                                  blank=True, null=True)
    star = models.NullBooleanField()

    def __unicode__(self):
        return 'Name: %s, Created: %s, Size: %d bytes' % (
            self.name, self.created.strftime('%d.%m.%Y %H:%M'),
            self.target.size)


class FileContentType(models.Model):
    """Content-Type of uploaded file"""

    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name


class FileSharedLink(models.Model):
    """Anonymous shared link to user file"""

    name = models.CharField(max_length=10, unique=True, db_index=True)

    def __unicode__(self):
        return self.name


class Directory(models.Model):
    """Directory of file"""

    name = models.CharField(max_length=64, db_index=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='directories')

    def __unicode__(self):
        return self.name
