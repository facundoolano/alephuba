from django.db import models
from tinymce import models as tinymce_models
from django.core.urlresolvers import reverse

class Entrada(models.Model):
    titulo = models.CharField(max_length=80)
    contenido = tinymce_models.HTMLField()
    autor = models.CharField(max_length=20, default='aleph uba')
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.titulo


CONTENIDO_UPLOAD = u"<p>El documento <b><a href='{url}'>{titulo}</a></b> \
                    {autor} fue subido.</p>"
                    
def publicar_upload(sender, **kwargs):
    
    if kwargs['created']:
        documento = kwargs['instance']
        
        entrada = Entrada()
        entrada.titulo = documento.titulo
        
        autor = u'de <b>{autor}</b>'.format(autor=documento.autor) if documento.autor else ''
        
        entrada.contenido = CONTENIDO_UPLOAD.format(
                                        url=reverse('documento', 
                                                    args=[documento.pk]),
                                        titulo=documento.titulo,
                                        autor=autor)
        entrada.save()
    
#desactivo noticias para subida de archivos.
#post_save.connect(publicar_upload, Documento, dispatch_uid="publicar_upload")