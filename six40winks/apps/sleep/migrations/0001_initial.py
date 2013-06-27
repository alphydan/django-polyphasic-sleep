# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SleepPhase'
        db.create_table(u'sleep_sleepphase', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sleep_phase', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('date_bin', self.gf('django.db.models.fields.DateField')()),
            ('start_dt', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_dt', self.gf('django.db.models.fields.DateTimeField')()),
            ('comments', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'sleep', ['SleepPhase'])

        # Adding model 'SleepDay'
        db.create_table(u'sleep_sleepday', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_bin', self.gf('django.db.models.fields.DateField')()),
            ('total_sleep', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('rem_sleep', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('light_sleep', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('deep_sleep', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'sleep', ['SleepDay'])


    def backwards(self, orm):
        # Deleting model 'SleepPhase'
        db.delete_table(u'sleep_sleepphase')

        # Deleting model 'SleepDay'
        db.delete_table(u'sleep_sleepday')


    models = {
        u'sleep.sleepday': {
            'Meta': {'ordering': "['date_bin']", 'object_name': 'SleepDay'},
            'date_bin': ('django.db.models.fields.DateField', [], {}),
            'deep_sleep': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'light_sleep': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rem_sleep': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'total_sleep': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'sleep.sleepphase': {
            'Meta': {'ordering': "['start_dt']", 'object_name': 'SleepPhase'},
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date_bin': ('django.db.models.fields.DateField', [], {}),
            'end_dt': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sleep_phase': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'start_dt': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['sleep']