from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from alephuba import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^$', direct_to_template, {'template': 'index.html'}, name='home'),
    url(r'^admin/', include(admin.site.urls), name='admin'),
    
    #SOLO PARA DESARROLLO    
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
)
