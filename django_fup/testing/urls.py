from django.conf.urls.defaults import patterns, include

urlpatterns = patterns(
    '',
    (r'^accounts/', include('django.contrib.auth.urls')),
    (r'^file_uploads/', include('file_uploads.urls')))
