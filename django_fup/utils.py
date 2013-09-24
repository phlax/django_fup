import cStringIO

try:
    from PIL import Image
    Image
except:
    import Image

from django.utils.translation import ugettext as _

from file_uploads.exceptions import ImageUploadError


def validate_uploaded_image(upfile, min_width=None, min_height=None):
    upfile.open()
    upfile.seek(0)
    try:
        image = Image.open(cStringIO.StringIO(upfile.read()))
    except:
        raise ImageUploadError(
            _('The uploaded file was not recognised as an image'))

    if image.size[0] < min_width:
        raise ImageUploadError(
            _('The image must be at least %s pixels wide' % min_width))

    if image.size[1] < min_height:
        raise ImageUploadError(
            _('The image must be at least %s pixels high' % min_height))
