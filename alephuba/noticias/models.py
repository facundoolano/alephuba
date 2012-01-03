from django.db import models
from django.contrib.auth.models import User as AuthUser
from tinymce import models as tinymce_models

class Entrada(models.Model):
    titulo = models.CharField(max_length=50)
    contenido = tinymce_models.HTMLField()
    autor = models.ForeignKey(AuthUser)
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.titulo