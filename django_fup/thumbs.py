import os

from easy_thumbnails.files import get_thumbnailer

from django.conf import settings


class EasyThumbs(object):

    def thumbnail(self, src=None):
        relative_name = None
        if src is None:
            src = open(settings.FUP_THUMB_DEFAULT)
            relative_name = os.path.basename(
                settings.FUP_THUMB_DEFAULT)
        thumbnailer = get_thumbnailer(
            src, relative_name=relative_name)
        thumbnail_options = {}
        thumbnail_options.update({'size': (100, 100)})
        return thumbnailer.get_thumbnail(thumbnail_options)

