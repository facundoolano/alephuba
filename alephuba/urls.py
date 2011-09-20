from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from alephuba import settings
from django.views.generic.base import TemplateView
from alephuba.aleph.views.generic_views import DocumentoList, DocumentoDetail,\
    DocumentoCreate
from aleph.views import views, json_views
import django.contrib.auth.views

admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^$', django.contrib.auth.views.login, {'template_name': 'index.html'}, name='home'),
    url(r'^admin/', include(admin.site.urls), name='admin'),
    
    url(r'^docs/$', DocumentoList.as_view(), name='documentos'),
    url(r'^docs/(?P<pk>\d+)/$', DocumentoDetail.as_view(), name='documento'),
    url(r'^docs/add/$', DocumentoCreate.as_view(), name='add_documento'),
    
    url(r'^registracion/$', views.registration, name='registracion'),
    url(r'^logout/$', django.contrib.auth.views.logout, {'next_page' : '/'}, name='logout'),
    url(r'^mi_cuenta/$', TemplateView.as_view(template_name='mi_cuenta.html'), name='mi_cuenta'),
    url(r'^cambio_contrasenia/$', django.contrib.auth.views.password_change,
       {'template_name': 'cambio_contrasenia.html'}, name='cambio_contrasenia'),
    url(r'cambio_contrasenia/done/$', django.contrib.auth.views.password_change_done, {'template_name': 'mi_cuenta.html'}), 
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^autocomplete_documento/', json_views.autocomplete_documento, name='autocomplete_documento'),

    #SOLO PARA DESARROLLO    
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
)
