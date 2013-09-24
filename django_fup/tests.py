import os
import json

from django.test import TestCase as DjangoTestCase
from django.db import models
from django.forms.models import inlineformset_factory
from django.forms import ModelForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db import connection, DatabaseError
from django.db.models.loading import load_app
from django.core.management import sql
from django.core.management.color import no_style
from django.conf import settings

from file_uploads.forms import AtLeastOneImageFormSet
from file_uploads.models import TempImage, UPLOAD_PATH
from file_uploads.widgets import FileUploadsImageWidget


class TestDummy(models.Model):
    pass


class TestDummyImage(models.Model):
    image = models.ImageField(upload_to='test_upload')
    dummy = models.ForeignKey(
        'TestDummy', related_name="images")


class TestDummyAttr(models.Model):
    attr = models.CharField(max_length=255)
    dummy = models.ForeignKey(
        'TestDummy', related_name="attrs")


class TestDummyForm(ModelForm):

    class Meta:
        model = TestDummy


class TestDummyImageForm(ModelForm):

    class Meta:
        model = TestDummy


class TestCase(DjangoTestCase):
    initiated = False

    @classmethod
    def setUpClass(cls, *args, **kwargs):
        if not TestCase.initiated:
            TestCase.create_models_from_app('file_uploads.tests')
            TestCase.initiated = True
        super(TestCase, cls).setUpClass(*args, **kwargs)

    @classmethod
    def create_models_from_app(cls, app_name):
        """
        Manually create Models (used only for testing)
        from the specified string app name.
        Models are loaded from the module "<app_name>.models"
        """
        app = load_app(app_name)
        asql = sql.sql_create(app, no_style(), connection)
        cursor = connection.cursor()
        for statement in asql:
            try:
                cursor.execute(statement)
            except DatabaseError, excn:
                print excn.message


class AtLeastOneImageFormSetTest(TestCase):

    data = {
        'attrs-TOTAL_FORMS': u'3',
        'attrs-INITIAL_FORMS': u'0',
        'attrs-MAX_NUM_FORMS': u'3',
        'attrs-0-id': '',
        'attrs-0-attr': u'',
        'attrs-1-id': '',
        'attrs-1-attr': u'',
        'attrs-2-id': '',
        'attrs-2-attr': u''}

    def setUp(self):
        self.formset = inlineformset_factory(
            TestDummy, TestDummyAttr,
            formset=AtLeastOneImageFormSet,
            extra=3, max_num=3)
        self.dummy = TestDummy()
        self.dummy.save()

    def test_validate_empty(self):
        formset = self.formset(data=self.data, instance=self.dummy)
        self.assertEquals(formset.is_valid(), False)
        self.assertEquals(
            formset.errors, [{'attr': [u'This field is required.']}, {}, {}])

    def test_validate_one(self):
        data = self.data.copy()
        data.update({'attrs-0-attr': 'Attr 0'})
        formset = self.formset(data=data, instance=self.dummy)
        self.assertEquals(formset.is_valid(), True)


class FileUploadsImageWidgetTest(TestCase):

    widget_name = 'test-widget'
    widget_id = 'id_%s' % widget_name
    expected = u'<div class="image">' \
        + '<a class="add" data-target="#modal-upload" href="#" ' \
        + 'data-source="%(uploader_url)s" data-toggle="modal" ' \
        + 'data-upload="%(uploader_upload_url)s" >' \
        + '<img src="%(img_src)s" /></a>' \
        + '<input type="hidden" id="%(widget_id)s" name="%(widget_id)s" ' \
        + 'value="%(value)s" /></div>' \
        + '<noscript><input type="file" name="%(widget_name)s" ' \
        + 'id="%(widget_id)s" /></noscript>'

    defaults = {
        'uploader_upload_url': reverse('file-uploader-upload'),
        'uploader_url': reverse('file-uploader'),
        'widget_name': widget_name,
        'widget_id': widget_id}

    def setUp(self):
        self.image_path = (
            os.path.join(
                os.path.dirname(__file__),
                'testing/test.png'))
        self.image = SimpleUploadedFile(
            'test.png',
            open(self.image_path).read(),
            'image/png')
        self.temp_image = TempImage(
            original=self.image, content_type=self.image.content_type)
        self.temp_image.save()
        self.widget = FileUploadsImageWidget()

    def tearDown(self):
        self.temp_image.delete()

    def test_value_from_datadict(self):
        """
        when the form is submitted the submitted filename should be transformed
        into the associated temp image
        """
        data = {'id_%s' % self.widget_name: self.temp_image.original.name}
        files = []
        result = self.widget.value_from_datadict(data, files, self.widget_name)
        self.assertEquals(result.size, self.image.size)
        self.assertEquals(result.content_type, self.image.content_type)

    def test_render_empty(self):
        """
        this test renders the widget without any
        associated images temporary or otherwise
        """
        value = ''
        result = self.widget.render(
            self.widget_name, value,
            {'id': self.widget_id})
        values = self.defaults.copy()
        values.update(
            {'value': '/static/file_uploads/images/question.small.gif',
             'img_src': '/static/file_uploads/images/question.small.gif'})
        self.assertEquals(result, self.expected % values)

    def test_render_uploaded(self):
        """
        this test simulates the situation where the form is re-rendered,
        perhaps due to error and the widget must show the
        *temp* image that has already been uploaded
        """

        data = {'id_%s' % self.widget_name: self.temp_image.original.name}
        files = []
        value = self.widget.value_from_datadict(data, files, self.widget_name)
        result = self.widget.render(
            self.widget_name, value,
            {'id': self.widget_id})
        values = self.defaults.copy()
        values.update(
            {'value': self.temp_image.original.name,
             'img_src': self.temp_image.original.name})
        self.assertEquals(result, self.expected % values)

    def test_render_existing(self):
        """
        In this case there is an image associated with the dummy obj.
        When the widget is rendered it should show the *saved* image
        """
        dummy = TestDummy()
        dummy.save()
        dummy_image = TestDummyImage(dummy=dummy, image=self.image)
        dummy_image.save()
        result = self.widget.render(
            self.widget_name, dummy_image.image,
            {'id': 'id_%s' % self.widget_name})
        values = self.defaults.copy()
        values.update(
            {'value': dummy_image.pk,
             'img_src': dummy_image.image.name})
        self.assertEquals(result, self.expected % values)


class FileUploaderTest(TestCase):

    def setUp(self):
        self.user = User(username='test_user')
        self.user.set_password("password")
        self.user.save()
        self.image_path = os.path.join(
            os.path.dirname(__file__),  'testing/test.png')
        self.image = SimpleUploadedFile(
            'test.png',
            open(self.image_path).read(),
            'image/png')

        self.evil_image_path = os.path.join(
            os.path.dirname(__file__),
            'testing/test-evil.png')

    def tearDown(self):
        self.user.delete()
        self.client.logout()

    def login(self):
        self.client.login(username='test_user', password='password')

    def login_redirect(self, target):
        return '%s?next=%s' % (reverse('login'), reverse(target))

    def test_anon_cannot_get_uploader(self):
        self.assertRedirects(
            self.client.get(reverse('file-uploader')),
            self.login_redirect('file-uploader'))

    def test_anon_cannot_post_uploader(self):
        self.assertRedirects(
            self.client.post(reverse('file-uploader')),
            self.login_redirect('file-uploader'))

    def test_anon_cannot_get_uploader_upload(self):
        self.assertRedirects(
            self.client.get(reverse('file-uploader-upload')),
            self.login_redirect('file-uploader-upload'))

    def test_anon_cannot_post_uploader_upload(self):
        self.assertRedirects(
            self.client.post(reverse('file-uploader-upload')),
            self.login_redirect('file-uploader-upload'))

    def test_user_can_get_uploader(self):
        self.login()
        self.assertEquals(
            self.client.get(reverse('file-uploader-upload')).status_code, 200)

    def assert_json_has_plain_text_header(self, response):
        self.assertEquals(
            response['Content-Type'],
            'text/plain; charset=utf-8')

    def post_expects_json(self, url, image=None):
        if image:
            with open(image) as image_file:
                response = self.client.post(url, {'qqfile': image_file})
        else:
            return self.client.post(url)
        self.assert_json_has_plain_text_header(response)
        return json.loads(response.content)

    def test_post_json(self):
        self.login()
        self.assertFalse(
            self.post_expects_json(
                reverse('file-uploader-upload')).get('success'))

    def test_post_too_large(self):
        self.login()
        settings.MAX_IMAGE_SIZE = 1024
        self.assertFalse(
            self.post_expects_json(
                reverse('file-uploader-upload'),
                self.image_path).get('success'))
        delattr(settings, 'MAX_IMAGE_SIZE')

    def test_post_success(self):
        self.login()
        url = reverse('file-uploader-upload')
        result = self.post_expects_json(
            reverse('file-uploader-upload'),
            self.image_path)
        self.assertTrue(
            all([(x in result) for x in ['url', 'id', 'filename']]))
        self.assertTrue(result['success'])

    def test_post_non_image(self):
        self.login()
        self.assertFalse(
            self.post_expects_json(
                reverse('file-uploader-upload'),
                self.evil_image_path).get('success'))


class TempImageTest(TestCase):

    def setUp(self):
        self.image = SimpleUploadedFile(
            'test.png',
            open(
                os.path.join(
                    os.path.dirname(__file__),
                    'testing/test.png')).read())
        self.temp_image = TempImage(
            original=self.image,
            content_type=self.image.content_type)
        self.temp_image.save()

    def tearDown(self):
        self.temp_image.delete()

    def test_absolute_url(self):
        self.assertEquals(
            '%s%s' % (
                settings.MEDIA_URL, self.temp_image.original.name),
            self.temp_image.get_absolute_url())

    def test_uuid(self):
        self.assertEquals(
            len(self.temp_image.uuid), 32)

    def test_filename(self):
        self.assertEquals(
            self.temp_image.original.name,
            '%s%s_%s' % (
                UPLOAD_PATH, self.temp_image.uuid.hex, self.image.name))
