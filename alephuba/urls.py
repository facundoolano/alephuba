from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from alephuba import settings
from django.views.generic.base import TemplateView
from alephuba.aleph.views.generic_views import DocumentoList, DocumentoDetail

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^docs/$', DocumentoList.as_view(), name='documentos'),
    url(r'^docs/(?P<pk>\d+)/$', DocumentoDetail.as_view(), name='documento'),
    
    #SOLO PARA DESARROLLO    
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
)
