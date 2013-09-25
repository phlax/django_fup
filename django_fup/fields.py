from south.modelsinspector import add_introspection_rules
from django.db import models
from django.db.models.fields.files import ImageFieldFile


class TempImageFieldFile(ImageFieldFile):

    def save(self, name, content, *la, **kwa):
        if hasattr(content, 'content_type'):
            self.instance.content_type = content.content_type
        return super(TempImageFieldFile, self).save(name, content, *la, **kwa)


class TempImageField(models.ImageField):
    attr_class = TempImageFieldFile

    def generate_filename(self, instance, name):
        return '%s%s_%s' % (self.upload_to, instance.uuid.hex, name)


add_introspection_rules([], ["^django_fup\.fields\.TempImageField"])
