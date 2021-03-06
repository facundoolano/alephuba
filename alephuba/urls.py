from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic.base import TemplateView, RedirectView

from alephuba.aleph.views import views
from alephuba import settings

import django.contrib.auth.views

admin.autodiscover()

urlpatterns = patterns('',
    
    (r'^docs/', include('aleph.urls')),
    (r'^noticias/', include('noticias.urls')),
    (r'^alertas/', include('alertas.urls')),
    
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^tinymce/', include('tinymce.urls')),
    
    url(r'^$', RedirectView.as_view(url='noticias/')),
    
    #TODO no deberia ir en otra parte?
    url(r'^login/$', django.contrib.auth.views.login, {'template_name': 'usuarios/login.html'}, name='login'),
    url(r'^registracion/$', views.registration, name='registracion'),
    url(r'^logout/$', django.contrib.auth.views.logout_then_login, name='logout'),
    url(r'^mi_cuenta/$', TemplateView.as_view(template_name='usuarios/mi_cuenta.html'), name='mi_cuenta'),
    url(r'^cambio_contrasenia/$', django.contrib.auth.views.password_change,
       {'template_name': 'usuarios/cambio_contrasenia.html'}, name='cambio_contrasenia'),
    url(r'cambio_contrasenia/done/$', django.contrib.auth.views.password_change_done, {'template_name': 'usuarios/mi_cuenta.html'}), 
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^acerca/$', TemplateView.as_view(template_name='acerca.html'), name='acerca'),
    url(r'^contacto/$', views.contacto, name='contacto'),
    
    url(r'^cuentas/password/reset/$', 'django.contrib.auth.views.password_reset', {'post_reset_redirect' : '/cuentas/password/reset/done/'}),
    url(r'^cuentas/password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    url(r'^cuentas/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'post_reset_redirect' : '/cuentas/password/done/'}),
    url(r'^cuentas/password/done/$', 'django.contrib.auth.views.password_reset_complete'),

    #SOLO PARA DESARROLLO    
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
)
