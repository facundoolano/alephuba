# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User as AuthUser
from django.db.models import Q
from django.db.models.aggregates import Avg, Count

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
    

class DocumentoManager(models.Manager):
    
    def busqueda_rapida(self, termino):
        """
        Devuelve un queryset de los documentos cuyo autor o título contiene
        el termino especificado.
        """
        
        if not termino:
            return self.all()
        
        #se usan Q objects para hacer un OR en vez de AND
        return self.filter(Q(autor__icontains=termino)|
                           Q(titulo__icontains=termino)
                           )
                           
class Documento(models.Model):
    objects = DocumentoManager()
    
    titulo = models.CharField('Título', max_length=TITULO_MAX_LENGTH, 
                              unique=True)
    autor = models.CharField(max_length=NOMBRE_MAX_LENGTH)
    
    carrera = models.ManyToManyField(Carrera, blank=True, null=True)
    materia = models.ManyToManyField(Materia, blank=True, null=True)
    
    tipo = models.CharField('Tipo de documento', max_length=3, 
                                choices=DOCUMENTO_CHOICES, default='LIB')
    
    isbn = models.CharField('ISBN', max_length=13, blank=True, null=True)
    olid = models.CharField('OLID', max_length=15, blank=True, null=True)
    
    def __unicode__(self):
        return self.titulo


class Archivo(models.Model):
    """ Un archivo descargable correspondiente a un documento. """
    
    documento = models.ForeignKey(Documento)
    
    link = models.URLField()
    subido_por = models.ForeignKey(AuthUser)
    fecha_subida = models.DateTimeField('Fecha de subida', auto_now_add=True)
    
    detalles = models.TextField(blank=True, null=True)


class VoteManager(models.Manager):
     
    def obtener_informacion_documento(self, documento):
        informacion = self.filter(document=documento).aggregate(promedio_votos = Avg('vote_value'),
                                                                cantidad_votos = Count('vote_value'))
        
        promedio_votos = informacion['promedio_votos'] if informacion['promedio_votos'] else 0 

        return (promedio_votos , informacion['cantidad_votos'])
    
    def usuario_ha_votado(self, user, documento):
        if self.filter(user=user, document=documento):
            return True
        
        return False
    
    def try_record_vote(self, document_pk, user, vote_value):
        
        document = Documento.objects.get(pk=document_pk)
        
        if self.usuario_ha_votado(user, document):
            return False
        
        self.create(user=user, document=document, vote_value=vote_value)
        
        return True

class Vote(models.Model):
    user = models.ForeignKey(AuthUser)
    document = models.ForeignKey(Documento)
    vote_value = models.FloatField()
    
    objects = VoteManager()
    
    def __unicode__(self):
        return "%s, %s : %d" % (self.user, self.document, self.vote_value)

class UserProfile(models.Model):
    user = models.ForeignKey(AuthUser, unique=True)
    carrera = models.ForeignKey(Carrera, null=True)

AuthUser.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])