# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Carrera'
        db.create_table('aleph_carrera', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=80)),
            ('detalles', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('aleph', ['Carrera'])

        # Adding model 'Materia'
        db.create_table('aleph_materia', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('carrera', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aleph.Carrera'], null=True, blank=True)),
            ('codigo', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
            ('detalles', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('aleph', ['Materia'])

        # Adding model 'Documento'
        db.create_table('aleph_documento', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('autor', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True)),
            ('tipo', self.gf('django.db.models.fields.CharField')(default='LIB', max_length=3)),
            ('isbn', self.gf('django.db.models.fields.CharField')(max_length=13, null=True, blank=True)),
            ('olid', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
        ))
        db.send_create_signal('aleph', ['Documento'])

        # Adding M2M table for field carrera on 'Documento'
        db.create_table('aleph_documento_carrera', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('documento', models.ForeignKey(orm['aleph.documento'], null=False)),
            ('carrera', models.ForeignKey(orm['aleph.carrera'], null=False))
        ))
        db.create_unique('aleph_documento_carrera', ['documento_id', 'carrera_id'])

        # Adding M2M table for field materia on 'Documento'
        db.create_table('aleph_documento_materia', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('documento', models.ForeignKey(orm['aleph.documento'], null=False)),
            ('materia', models.ForeignKey(orm['aleph.materia'], null=False))
        ))
        db.create_unique('aleph_documento_materia', ['documento_id', 'materia_id'])

        # Adding model 'Archivo'
        db.create_table('aleph_archivo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('documento', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aleph.Documento'])),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('extension', self.gf('django.db.models.fields.CharField')(max_length=5, null=True, blank=True)),
            ('tamanio', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('subido_por', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('fecha_subida', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('detalles', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('aleph', ['Archivo'])

        # Adding model 'Vote'
        db.create_table('aleph_vote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('document', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aleph.Documento'])),
            ('vote_value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('aleph', ['Vote'])

        # Adding model 'UserProfile'
        db.create_table('aleph_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('carrera', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aleph.Carrera'], null=True)),
        ))
        db.send_create_signal('aleph', ['UserProfile'])


    def backwards(self, orm):
        
        # Deleting model 'Carrera'
        db.delete_table('aleph_carrera')

        # Deleting model 'Materia'
        db.delete_table('aleph_materia')

        # Deleting model 'Documento'
        db.delete_table('aleph_documento')

        # Removing M2M table for field carrera on 'Documento'
        db.delete_table('aleph_documento_carrera')

        # Removing M2M table for field materia on 'Documento'
        db.delete_table('aleph_documento_materia')

        # Deleting model 'Archivo'
        db.delete_table('aleph_archivo')

        # Deleting model 'Vote'
        db.delete_table('aleph_vote')

        # Deleting model 'UserProfile'
        db.delete_table('aleph_userprofile')


    models = {
        'aleph.archivo': {
            'Meta': {'object_name': 'Archivo'},
            'detalles': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'documento': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aleph.Documento']"}),
            'extension': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'fecha_subida': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'subido_por': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'tamanio': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'aleph.carrera': {
            'Meta': {'object_name': 'Carrera'},
            'detalles': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'})
        },
        'aleph.documento': {
            'Meta': {'object_name': 'Documento'},
            'autor': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'carrera': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['aleph.Carrera']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '13', 'null': 'True', 'blank': 'True'}),
            'materia': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['aleph.Materia']", 'null': 'True', 'blank': 'True'}),
            'olid': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.CharField', [], {'default': "'LIB'", 'max_length': '3'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'aleph.materia': {
            'Meta': {'object_name': 'Materia'},
            'carrera': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aleph.Carrera']", 'null': 'True', 'blank': 'True'}),
            'codigo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'detalles': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'aleph.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'carrera': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aleph.Carrera']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'aleph.vote': {
            'Meta': {'object_name': 'Vote'},
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aleph.Documento']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'vote_value': ('django.db.models.fields.FloatField', [], {})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['aleph']
