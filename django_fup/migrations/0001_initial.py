# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TempImage'
        db.create_table(u'django_fup_tempimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('uuidfield.fields.UUIDField')(unique=True, max_length=32, blank=True)),
            ('content_type', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('original', self.gf('django_fup.fields.TempImageField')(max_length=100)),
            ('data', self.gf('django.db.models.fields.TextField')(default='{}', blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'django_fup', ['TempImage'])

    def backwards(self, orm):
        # Deleting model 'TempImage'
        db.delete_table(u'django_fup_tempimage')

    models = {
        u'django_fup.tempimage': {
            'Meta': {'object_name': 'TempImage'},
            'content_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "'{}'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original': ('django_fup.fields.TempImageField', [], {'max_length': '100'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'blank': 'True'})
        }
    }

    complete_apps = ['django_fup']