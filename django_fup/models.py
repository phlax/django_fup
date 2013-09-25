from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _
from django_extensions.db.fields.json import JSONField

from uuidfield.fields import UUIDField

from django_fup.fields import TempImageField

UPLOAD_PATH = 'file_uploads/original/'


class TempImage(models.Model):
    """ A temporary image associated to a uuid
    """
    uuid = UUIDField(auto=True, max_length=32)

    content_type = models.CharField(
        max_length=100, blank=True, default='', null=False)

    original = TempImageField(
        upload_to=UPLOAD_PATH,
        blank=False, null=False)

    data = JSONField(blank=True, default='', null=False)
    created = models.DateTimeField(
        _('Created'),
        auto_now_add=True, editable=False)

    def get_absolute_url(self):
        return '%s%s' % (
            settings.MEDIA_URL, self.original.name)
