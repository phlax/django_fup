from django.conf.urls.defaults import url, patterns

from file_uploads.views import file_uploader, file_uploader_json


urlpatterns = patterns(
    '',
    url(r'^file-uploader/$',
        file_uploader,
        name="file-uploader"),
    url(r'^file-uploader-upload/$',
        file_uploader_json,
        name="file-uploader-upload"))
