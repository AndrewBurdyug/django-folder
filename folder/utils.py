import os
import uuid
import hashlib
import shutil

from django.conf import settings
from folder.errors import BadData
from folder.models import File, FileLink

FOLDER_MAX_FILE_SIZE = 1024 * 1024 * 2
if hasattr(settings, 'FOLDER_MAX_FILE_SIZE'):
    FOLDER_MAX_FILE_SIZE = settings.FOLDER_MAX_FILE_SIZE


def dehydrate_validation_errors(errors_data):
    """Convert ValidationError objects to their string representation
    it is safe for JsonResponse
    """

    dehydrated_output = {}

    for key, value in errors_data.items():
        errors = ", ".join([str(x).lstrip("[u'").rstrip("']") for x in value])
        dehydrated_output[key] = errors

    return dehydrated_output


def handle_uploaded_file(f, user):
    """
    """

    if f.size >= FOLDER_MAX_FILE_SIZE:
        raise BadData('size', f.size)

    tmp_filename = '/tmp/dfolder_%d_%s' % (user.pk, uuid.uuid4())
    with open(tmp_filename, 'wb+') as destination:
        for chunk in f.chunks(128):
            destination.write(chunk)

    md5sum = hashlib.md5()
    with open(tmp_filename, 'rb') as tmp_f:
        for chunk in tmp_f.read(128):
            md5sum.update(chunk)

    file_md5sum = md5sum.hexdigest()
    file_obj, created = File.objects.get_or_create(md5sum=file_md5sum,
                                                   size=f.size)
    FileLink.objects.get_or_create(name=f.name, target=file_obj, owner=user)
    if created:
        # owners = {x.owner for x in file_obj.filelinks.all()}
        shutil.move(tmp_filename, file_obj.name)
    else:
        os.remove(tmp_filename)

    info = dict(size=f.size, name=f.name, created=created)
    return info
