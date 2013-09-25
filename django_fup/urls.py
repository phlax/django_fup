from django.conf.urls.defaults import url, patterns

from django_fup.views import file_uploader, file_uploader_json


urlpatterns = patterns(
    '',
    url(r'^fup/?$',
        file_uploader,
        name="fup"),
    url(r'^fup/upload/?$',
        file_uploader_json,
        name="fup-upload"))
