from django.conf.urls.defaults import *

from django.views.generic.base import RedirectView, TemplateView

from alephuba.aleph.views.views import DocumentoList, DocumentoDetail, DocumentoCreate,\
    MirrorCreate, UpdateDocumentoList, UpdateDocumentoPorMateriaList
from alephuba.aleph.views import views, jsonviews


urlpatterns = patterns('',

            url(r'^$', RedirectView.as_view(url='buscar'), name='documentos'),
            url(r'^buscar/$', DocumentoList.as_view(), name='buscar'),
            url(r'^buscar/update/$', UpdateDocumentoList.as_view(), name='buscar_update'),
            url(r'^(?P<pk>\d+)/$', DocumentoDetail.as_view(), name='documento'),
            url(r'^buscar/materia/$', views.DocumentoPorMateriaList.as_view() , name='busqueda_por_materia'),
            url(r'^buscar/materia/update/$', UpdateDocumentoPorMateriaList.as_view(), name='filtrar_materia_update'),
            url(r'^add/$', DocumentoCreate.as_view(), name='add_documento'),
            url(r'^mirror/(?P<documento_id>\d+)/$', MirrorCreate.as_view(), name='add_mirror'),
            url(r'^autocomplete/', jsonviews.autocomplete_documento, name='autocomplete_documento'),
            url(r'^autocomplete_autor/', jsonviews.autocomplete_autor, name='autocomplete_autor'),
            url(r'^(?P<document_pk>\d+)/vote/(?P<vote>(\d+|\d+\.\d{1}))$', jsonviews.vote_on_document),
            url(r'^(?P<document_pk>\d+)/descarga$', jsonviews.contar_descarga),
            url(r'^isbn/', jsonviews.validate_isbn, name='validate_isbn'),
            url(r'^get_materias/', jsonviews.get_materias, name='get_materias'),
            
            url(r'^upload_error/', TemplateView.as_view(template_name='documentos/upload_error.html'), name='upload_error'),
          
)

