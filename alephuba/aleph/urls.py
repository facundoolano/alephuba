from django.conf.urls.defaults import *

from django.views.generic.base import RedirectView

from alephuba.aleph.views.generic_views import DocumentoList, DocumentoDetail, DocumentoCreate,\
    AjaxDocumentoList
from alephuba.aleph.views import views, json_views
from alephuba.aleph.model_forms import validate_isbn


urlpatterns = patterns('',

            url(r'^$', RedirectView.as_view(url='buscar'), name='documentos'),
            url(r'^buscar/$', DocumentoList.as_view(), name='buscar'),
            url(r'^buscar/update/$', AjaxDocumentoList.as_view(), name='buscar_update'),
            url(r'^(?P<pk>\d+)/$', DocumentoDetail.as_view(), name='documento'),
            url(r'^buscar/materia/$', views.busqueda_por_materia , name='busqueda_por_materia'),
            url(r'^add/$', DocumentoCreate.as_view(), name='add_documento'),
            url(r'^autocomplete/', json_views.autocomplete_documento, name='autocomplete_documento'),
            url(r'^(?P<document_pk>\d+)/vote/(?P<vote>(\d+|\d+\.\d{1}))$', json_views.vote_on_document),
            url(r'^isbn/', validate_isbn, name='validate_isbn'),
            url(r'^progress/', json_views.get_upload_progress, name='upload_progress'),
          
)
