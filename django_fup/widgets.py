import uuid

from django.utils.safestring import mark_safe
from django.forms import widgets
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from file_uploads.models import TempImage


class FileUploadsImageWidget(widgets.ClearableFileInput):

    template_file_uploader = (
        '<div class="image">'
        + '<a class="add" data-target="%(data-target)s" href="#" '
        + 'data-source="%(data-source)s" data-toggle="%(data-toggle)s" '
        + 'data-upload="%(data-upload)s" >'
        + '<img src="%(img_src)s" /></a>'
        + '<input type="hidden" id="%(input_id)s" name="%(input_id)s" '
        + 'value="%(img_id)s" />'
        + '</div>')

    def value_from_datadict(self, data, files, name):
        filename = data.get('id_%s' % name)
        if filename:
            filename = filename.split('/').pop()

            # test the uuid is valid
            if filename and len(filename) > 32:
                try:
                    uuid.UUID(filename[:32])
                except ValueError:
                    # not a uuid!
                    return
            else:
                return

            try:
                temp_image = TempImage.objects.get(
                    uuid=filename[:32])
                return SimpleUploadedFile(
                    filename,
                    temp_image.original.read(),
                    temp_image.content_type)
            except ObjectDoesNotExist:
                return

    def render(self, name, value, attrs=None):
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label}

        template = u'%(input)s<noscript>%(noscript)s</noscript>'
        img_default = '%sdjango-fup/img/question.small.gif' % settings.STATIC_URL

        if isinstance(value, SimpleUploadedFile):
            img_src = TempImage.objects.get(
                uuid=value.name[:32]).get_absolute_url()
        else:
            img_src = value and value.url or img_default

        if hasattr(value, 'instance'):
            img_id = value.instance.pk
        else:
            img_id = img_src

        input_attrs = {
            'img_src': img_src,
            'img_id': img_id,
            'input_name': attrs['id'][3:],
            'input_id': attrs['id'],
            'data-toggle': 'modal',
            'data-target': '#modal-upload',
            'data-source': reverse('file-uploader'),
            'data-upload': reverse('file-uploader-upload')}

        substitutions['input'] = self.template_file_uploader % input_attrs
        substitutions['noscript'] = super(
            widgets.ClearableFileInput, self).render(name, value, attrs)

        if value and hasattr(value, "url"):
            if not self.is_required:
                # add a remove button
                pass

        return mark_safe(template % substitutions)
