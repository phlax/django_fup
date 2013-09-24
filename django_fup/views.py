import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings

from file_uploads.models import TempImage
from file_uploads.utils import validate_uploaded_image
from file_uploads.exceptions import ImageUploadError


def max_image_size():
    return getattr(settings, 'MAX_IMAGE_SIZE', 2097152)
TPL_FILE_UPLOADER = "file_uploads/file_uploader_view.html"


@login_required
def file_uploader(request, template_name=TPL_FILE_UPLOADER):
    context = {}
    return render_to_response(
        template_name, context,
        context_instance=RequestContext(request))


def normalize_filename(filename):
    return filename


# TODO: improve error responses
@login_required
def file_uploader_json(request, *la, **kwa):
    success = False
    upfile = request.FILES.get('qqfile')
    filesize = upfile and upfile.size or 0
    filename = upfile and upfile.name or None

    context = {
        'success': success}

    if not upfile or not filename:
        return HttpResponse(
            json.dumps(context, cls=DjangoJSONEncoder),
            content_type='text/plain; charset=utf-8')

    if filesize > max_image_size():
        return HttpResponse(
            json.dumps(context, cls=DjangoJSONEncoder),
            content_type='text/plain; charset=utf-8')

    try:
        validate_uploaded_image(upfile)
        success = True
    except ImageUploadError:
        return HttpResponse(
            json.dumps(context, cls=DjangoJSONEncoder),
            content_type='text/plain; charset=utf-8')

    temp_image = TempImage()
    temp_image.save()
    original = temp_image.original
    original.save(filename, upfile, True)
    temp_image.content_type = upfile.content_type
    temp_image.save()

    # let Ajax Upload know whether we saved it or not
    context = {
        'success': True,
        'filename': temp_image.original.name,
        'url': temp_image.get_absolute_url(),
        'id': temp_image.id}

    return HttpResponse(
        json.dumps(context, cls=DjangoJSONEncoder),
        content_type='text/plain; charset=utf-8')
