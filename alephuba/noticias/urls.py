from django.conf.urls.defaults import *
from alephuba.noticias.views import NoticiasView

urlpatterns = patterns('',

    url(r'^$', NoticiasView.as_view(), name='home'),
          
)