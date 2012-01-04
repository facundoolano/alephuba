from django.db import models
from tinymce import models as tinymce_models
from django.db.models.signals import post_save
from alephuba.aleph.models import Documento
from django.core.urlresolvers import reverse

class Entrada(models.Model):
    titulo = models.CharField(max_length=80)
    contenido = tinymce_models.HTMLField()
    autor = models.CharField(max_length=20, default='aleph uba')
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.titulo


CONTENIDO_UPLOAD = "<p>El documento <b><a href='{url}'>{titulo}</a></b> \
                    de <b>{autor}</b> fue subido por <b>{usuario}</b>.</p>"
                    
def publicar_upload(sender, **kwargs):
    
    if kwargs['created']:
        documento = kwargs['instance']
        
        entrada = Entrada()
        entrada.titulo = documento.titulo
        entrada.contenido = CONTENIDO_UPLOAD.format(
                                        url=reverse('documento', 
                                                    args=[documento.pk]),
                                        titulo=documento.titulo,
                                        autor=documento.autor,
                                        usuario=documento.subido_por.username)
        entrada.save()
    

post_save.connect(publicar_upload, Documento, dispatch_uid="publicar_upload")