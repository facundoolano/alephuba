from django.conf.urls.defaults import *
from alephuba.alertas.views import ReportarView

urlpatterns = patterns('',

    url(r'^reportar/(?P<archivo_id>\d+)/$', ReportarView.as_view(), name='reportar'),
          
)