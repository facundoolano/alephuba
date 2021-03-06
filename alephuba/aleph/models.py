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
    ('TES', 'Tesis'),
    ('PAP', 'Paper')
)

IDIOMA_DOCUMENTO_CHOICES = (
    ('ES', 'Español'),
    ('EN', 'Inglés'),
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

class Departamento(models.Model):
    codigo = models.CharField(max_length=CODIGO_MATERIA_MAX_LENGTH, unique=True)
    nombre = models.CharField(max_length=NOMBRE_MAX_LENGTH)
    
    def __unicode__(self):
        return u'%s - %s' % (self.codigo, self.nombre)

class Materia(models.Model):
    objects = DocRelatedManager()
    
    nombre = models.CharField(max_length=NOMBRE_MAX_LENGTH)
    
    carrera = models.ManyToManyField(Carrera, blank=True, null=True)
    departamento = models.ForeignKey(Departamento, blank=True, null=True)
    codigo = models.CharField(max_length=CODIGO_MATERIA_MAX_LENGTH, unique=True)
    
    class Meta:
        ordering = ('codigo',)
    
    def __unicode__(self):
        return u'%s %s' % (self.codigo, self.nombre)
    

class DocumentoManager(models.Manager):
    
    def sugerencias(self, termino, limite):
        """ 
        Devuelve una lista de terminos sugeridos en base al termino provisto,
        para ser usados en autocompletar. Se usa el mismo criterio que en la 
        busqueda rapida.
        """
        #TODO limitar resultados
        
        resultado = list(self.filter(titulo__search=termino).values_list(
                                                    'titulo', flat=True).distinct()[:limite])
        resultado += list(self.filter(materia__nombre__search=termino).values_list(
                                                    'materia__nombre', 
                                                    flat=True).distinct()
                                                    [:limite-len(resultado)])
        resultado += list(self.filter(autor__search=termino).values_list(
                                                    'autor', flat=True).distinct()
                                                    [:limite-len(resultado)])
        
        return resultado
        
        
    
    def busqueda_rapida(self, termino):
        """
        Devuelve un queryset de los documentos cuyo autor o título contiene
        el termino especificado.
        """
        
        if not termino:
            return self.all().order_by('-id')
        
        #se usan Q objects para hacer un OR en vez de AND
        return self.filter(Q(autor__search=termino)|
                           Q(titulo__search=termino)|
                           Q(materia__nombre__search=termino)|
                           Q(materia__codigo__search=termino)
                           ).distinct().order_by('-id')
    
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

class DescargaDocumento(models.Model):
    documento = models.ForeignKey(Documento, related_name='descargas')
    usuario = models.ForeignKey(AuthUser)
    fecha = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return u"%s : %s" % (self.documento.titulo, self.usuario.username)

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

    def obtener_promedio_documentos(self, lista_documentos):

        lista_promedios = []

        for documento in lista_documentos:
            resultado_query = self.filter(document=documento).aggregate(Avg('vote_value'))
            promedio_votos = resultado_query['vote_value__avg']
            lista_promedios.append(str(round(promedio_votos, 1)) if promedio_votos else '0.0')

        return lista_promedios

    def obtener_informacion_documento(self, documento):
        informacion = self.filter(document=documento).aggregate(promedio_votos = Avg('vote_value'),
                                                                cantidad_votos = Count('vote_value'))
        
        promedio_votos = informacion['promedio_votos'] if informacion['promedio_votos'] else 0 

        return (promedio_votos , informacion['cantidad_votos'])
    
    def usuario_ha_votado(self, user, documento):
        if self.filter(user=user, document=documento).exists():
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