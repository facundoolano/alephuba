# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        
        orm.Departamento.objects.create(codigo="63", nombre="Química")
        orm.Departamento.objects.create(codigo="61", nombre="Matemática")
        orm.Departamento.objects.create(codigo="76", nombre="Ingeniería Química")
        orm.Departamento.objects.create(codigo="73", nombre="Ingeniería Naval")
        orm.Departamento.objects.create(codigo="67", nombre="Ingeniería Mecánica")
        orm.Departamento.objects.create(codigo="78", nombre="Idiomas")
        orm.Departamento.objects.create(codigo="69", nombre="Hidráulica")
        orm.Departamento.objects.create(codigo="71", nombre="Gestión Industrial")
        orm.Departamento.objects.create(codigo="68", nombre="Transporte")
        orm.Departamento.objects.create(codigo="62", nombre="Física")
        orm.Departamento.objects.create(codigo="64", nombre="Estabilidad")
        orm.Departamento.objects.create(codigo="65", nombre="Electrotecnia")
        orm.Departamento.objects.create(codigo="66", nombre="Electrónica")
        orm.Departamento.objects.create(codigo="74", nombre="Construcciones y Estructuras")
        orm.Departamento.objects.create(codigo="75", nombre="Computación")
        orm.Departamento.objects.create(codigo="70", nombre="Agrimensura")
        orm.Departamento.objects.create(codigo="CBC", nombre="CBC")
        
        for materia in orm.Materia.objects.all():
            codigo = materia.codigo.split('.')[0]
            deptos = orm.Departamento.objects.filter(codigo=codigo)
            if deptos:
                materia.departamento = deptos[0]
                materia.save()


    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration.")


    models = {
        'aleph.archivo': {
            'Meta': {'object_name': 'Archivo'},
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'})
        },
        'aleph.departamento': {
            'Meta': {'object_name': 'Departamento'},
            'codigo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'aleph.documento': {
            'Meta': {'object_name': 'Documento'},
            'autor': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'carrera': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['aleph.Carrera']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idioma': ('django.db.models.fields.CharField', [], {'default': "'ES'", 'max_length': '2'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '13', 'null': 'True', 'blank': 'True'}),
            'materia': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['aleph.Materia']", 'null': 'True', 'blank': 'True'}),
            'olid': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.CharField', [], {'default': "'LIB'", 'max_length': '3'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'aleph.materia': {
            'Meta': {'ordering': "('codigo',)", 'object_name': 'Materia'},
            'carrera': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aleph.Carrera']", 'null': 'True', 'blank': 'True'}),
            'codigo': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'departamento': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aleph.Departamento']", 'null': 'True', 'blank': 'True'}),
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
