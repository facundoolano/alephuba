# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User as AuthUser, User
from django.db.models import Q

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

SCORES = (
    (u'+1', +1),
    (u'-1', -1),
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
            return self.order_by('-fecha_subida')
        
        #se usan Q objects para hacer un OR en vez de AND
        return self.filter(Q(autor__icontains=termino)|
                           Q(titulo__icontains=termino)
                           ).order_by('-fecha_subida')

class Documento(models.Model):
    objects = DocumentoManager()
    
    titulo = models.CharField('Título', max_length=TITULO_MAX_LENGTH, 
                              unique=True)
    autor = models.CharField(max_length=NOMBRE_MAX_LENGTH)
    
    carrera = models.ManyToManyField(Carrera, blank=True, null=True)
    materia = models.ManyToManyField(Materia, blank=True, null=True)
    
    detalles = models.TextField(blank=True, null=True)
    
    tipo = models.CharField('Tipo de documento', max_length=3, 
                                choices=DOCUMENTO_CHOICES, default='LIB')
    
    
    link = models.URLField()
    mirror = models.URLField(blank=True, null=True)
    subido_por = models.ForeignKey(AuthUser)
    fecha_subida = models.DateTimeField('Fecha de subida', auto_now_add=True)
    
    def __unicode__(self):
        return self.titulo

class VoteManager(models.Manager):
    
    def record_vote(self, document_pk, user, vote_value):
        
        # TODO : Falta fijarse si ya existia el voto.
        self.create(user=user, document=Documento.objects.get(pk=document_pk), vote_value=vote_value)

class Vote(models.Model):
    user = models.ForeignKey(User)
    document = models.ForeignKey(Documento)
    vote_value = models.SmallIntegerField(choices=SCORES)
    
    objects = VoteManager()
    
    def __unicode__(self):
        return "%s, %s : %d" % (self.user, self.document, self.vote_value)

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    carrera = models.ForeignKey(Carrera, null=True)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])