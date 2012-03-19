# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User as AuthUser
from django.db.models import Q
from django.db.models.aggregates import Avg, Count

NOMBRE_MAX_LENGTH = 80
CODIGO_MATERIA_MAX_LENGTH = 10
TITULO_MAX_LENGTH = 80
EXTENSION_MAX_LENGTH = 5

DOCUMENTO_CHOICES = (
    ('LIB', 'Libro'),
    ('APU', 'Apunte'),
    ('INF', 'Informe'),
    ('EXA', 'Examen'),
    ('GEJ', 'Guia de Ejercicios'),
)

IDIOMA_DOCUMENTO_CHOICES = (
    ('ES', 'Español'),
    ('EN', 'Ingles'),
    ('OT', 'Otro')
)

class DocRelatedManager(models.Manager):
    
    def con_documentos(self):
        """ 
        Devuelve un qs de instancias que tienen asignado algun documento. 
        """
        return self.annotate(num_docs=Count('documento')).filter(num_docs__gt=0)

class Carrera(models.Model):
    objects = DocRelatedManager()
    
    nombre = models.CharField(max_length=NOMBRE_MAX_LENGTH, unique=True)

    def __unicode__(self):
        return self.nombre
    
class Materia(models.Model):
    objects = DocRelatedManager()
    
    nombre = models.CharField(max_length=NOMBRE_MAX_LENGTH)
    carrera = models.ForeignKey(Carrera, blank=True, null=True)
    codigo = models.CharField(max_length=CODIGO_MATERIA_MAX_LENGTH, unique=True)
    
    class Meta:
        ordering = ('codigo',)
    
    def __unicode__(self):
        return u'%s %s' % (self.codigo, self.nombre)
    

class DocumentoManager(models.Manager):
    
    def busqueda_rapida(self, termino):
        """
        Devuelve un queryset de los documentos cuyo autor o título contiene
        el termino especificado.
        """
        
        if not termino:
            return self.all().order_by('-id')
        
        #se usan Q objects para hacer un OR en vez de AND
        return self.filter(Q(autor__icontains=termino)|
                           Q(titulo__icontains=termino)|
                           Q(materia__nombre__icontains=termino)|
                           Q(materia__codigo__icontains=termino)
                           ).distinct().order_by('-id')
    
    def filtrar_materias(self, carreras, materias):
        """ 
        Devuelve un queryset de documentos que pertenecen a las carreras  o 
        materias especificadas.
        """
        result = self.all()
        
        if carreras:
            result = result.filter(carrera__in=carreras)
        
        if materias:
            result = result.filter(materia__in=materias)
        
        return result.order_by('-id')
                           
class Documento(models.Model):
    objects = DocumentoManager()
    
    titulo = models.CharField('Título', max_length=TITULO_MAX_LENGTH)
    autor = models.CharField(max_length=NOMBRE_MAX_LENGTH, blank=True, null=True)
    idioma = models.CharField(max_length=2, choices=IDIOMA_DOCUMENTO_CHOICES, default='ES')
    
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
    extension = models.CharField(max_length=EXTENSION_MAX_LENGTH, blank=True, null=True)
    tamanio = models.BigIntegerField('Tamaño', blank=True, null=True)
    subido_por = models.ForeignKey(AuthUser)
    fecha_subida = models.DateTimeField('Fecha de subida', auto_now_add=True)
    
    def __unicode__(self):
        return self.documento.titulo


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
        return u"%s, %s : %d" % (self.user, self.document, self.vote_value)

class UserProfile(models.Model):
    user = models.ForeignKey(AuthUser, unique=True)
    carrera = models.ForeignKey(Carrera, null=True)

AuthUser.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])