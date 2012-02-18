# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User as AuthUser
from alephuba.aleph.models import Archivo

MOTIVO_CHOICES = (
                  ('link', 'Link caído'),
                  ('file', 'Archivo inválido'),
                  ('otro', 'Otro')
                  )


# Create your models here.
class Alerta(models.Model):
    
    archivo = models.ForeignKey(Archivo)
    motivo = models.CharField(max_length=5, choices=MOTIVO_CHOICES, 
                              default='link')
    mensaje = models.TextField()
    autor = models.ForeignKey(AuthUser)
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return '%s - %s' % (self.archivo.documento, self.get_motivo_display())
    