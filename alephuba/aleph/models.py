# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User as AuthUser

NOMBRE_MAX_LENGTH = 80
CODIGO_MATERIA_MAX_LENGTH = 10
TITULO_MAX_LENGTH = 80

DOCUMENTO_CHOICES = (
    ('LIB', 'Libro'),
    ('APU', 'Apunte'),
    ('RES', 'Resumen'),
    ('INF', 'Informe'),
    ('EXA', 'Examen'),
)

class Carrera(models.Model):
    nombre = models.CharField(max_length=NOMBRE_MAX_LENGTH, unique=True)
    detalles = models.TextField(blank=True, null=True)
    
    def __unicode__(self):
        return self.nombre
    
class Materia(models.Model):
    nombre = models.CharField(max_length=NOMBRE_MAX_LENGTH, unique=True)
    carrera = models.ForeignKey(Carrera, blank=True, null=True)
    codigo = models.CharField(max_length=CODIGO_MATERIA_MAX_LENGTH, unique=True)
    detalles = models.TextField(blank=True, null=True)
    
    def __unicode__(self):
        return self.nombre
    

class Documento(models.Model):
    titulo = models.CharField('Título', max_length=TITULO_MAX_LENGTH, 
                              unique=True)
    autor = models.CharField(max_length=NOMBRE_MAX_LENGTH)
    
    carrera = models.ForeignKey(Carrera, blank=True, null=True)
    materia = models.ForeignKey(Materia, blank=True, null=True)
    
    detalles = models.TextField(blank=True, null=True)
    
    tipo = models.CharField('Tipo de documento', max_length=3, 
                                choices=DOCUMENTO_CHOICES, default='LIB')
    
    
    link = models.URLField()
    mirror = models.URLField(blank=True, null=True)
    subido_por = models.ForeignKey(AuthUser)
    fecha_subida = models.DateTimeField('Fecha de subida', auto_now_add=True)
    
    def __unicode__(self):
        return self.titulo
    