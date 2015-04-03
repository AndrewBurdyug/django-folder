from django.conf import settings
from folder.errors import BadData

FOLDER_MAX_FILE_SIZE = 1024 * 1024 * 1024 * 2
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


def handle_uploaded_file(f):
    """
    """

    if f.size >= FOLDER_MAX_FILE_SIZE:
        raise BadData('size', f.size)

    with open('/tmp/1', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    info = dict(size=f.size, name=f.name)
    return info
