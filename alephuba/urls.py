from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from alephuba import settings
from django.views.generic.base import TemplateView
from alephuba.aleph.views.generic_views import DocumentoList, DocumentoDetail,\
    DocumentoCreate
from aleph.views import views
import django.contrib.auth.views

admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^admin/', include(admin.site.urls), name='admin'),
    
    url(r'^docs/$', DocumentoList.as_view(), name='documentos'),
    url(r'^docs/(?P<pk>\d+)/$', DocumentoDetail.as_view(), name='documento'),
    url(r'^docs/add/$', DocumentoCreate.as_view(), name='add_documento'),
    
    url(r'^registracion/$', views.registration, name='registracion'),
    url(r'^login/$', django.contrib.auth.views.login, {'template_name': 'login.html'} , name='login'),
    url(r'^logout/$', django.contrib.auth.views.logout, {'template_name': 'index.html'}, name='logout'),
    url(r'^mi_cuenta/$', TemplateView.as_view(template_name='mi_cuenta.html'), name='mi_cuenta'),
    
    #SOLO PARA DESARROLLO    
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
)
