# encoding: utf-8
import datetime
import uuid

from south.db import db
from south.v2 import SchemaMigration
from django.db import models

import uuid

from file_uploads.models import TempImage


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'TempImage.filename'
        db.delete_column('file_uploads_tempimage', 'filename')

        # Adding field 'TempImage.content_type'
        db.add_column('file_uploads_tempimage', 'content_type', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True), keep_default=False)

        # Changing field 'TempImage.original'
        db.alter_column('file_uploads_tempimage', 'original', self.gf('file_uploads.fields.TempImageField')(max_length=100))

        # Changing field 'TempImage.uuid'
        db.delete_column('file_uploads_tempimage', 'uuid')
        db.add_column('file_uploads_tempimage', 'uuid', self.gf('uuidfield.fields.UUIDField')(max_length=32, blank=True, null=True))

        
        for temp_image in TempImage.objects.all():
            temp_image.uuid = uuid.uuid4().hex
            temp_image.save()

        db.alter_column('file_uploads_tempimage', 'uuid', self.gf('uuidfield.fields.UUIDField')(unique=True, max_length=32, blank=False, null=False))

        # Adding unique constraint on 'TempImage', fields ['uuid']
        db.create_unique('file_uploads_tempimage', ['uuid'])

        for m in TempImage.objects.all():
            m.uuid = u'' + str(uuid.uuid1().hex)
            m.save()

    def backwards(self, orm):
        
        # Removing unique constraint on 'TempImage', fields ['uuid']
        db.delete_unique('file_uploads_tempimage', ['uuid'])

        # Adding field 'TempImage.filename'
        db.add_column('file_uploads_tempimage', 'filename', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True), keep_default=False)

        # Deleting field 'TempImage.content_type'
        db.delete_column('file_uploads_tempimage', 'content_type')

        # Changing field 'TempImage.original'
        db.alter_column('file_uploads_tempimage', 'original', self.gf('django.db.models.fields.files.ImageField')(max_length=100))

        # Changing field 'TempImage.uuid'
        db.alter_column('file_uploads_tempimage', 'uuid', self.gf('django.db.models.fields.CharField')(max_length=36))


    models = {
        'file_uploads.tempimage': {
            'Meta': {'object_name': 'TempImage'},
            'content_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original': ('file_uploads.fields.TempImageField', [], {'max_length': '100'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'blank': 'True'})
        }
    }

    complete_apps = ['file_uploads']
