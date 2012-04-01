# Create your views here.
from django.views.generic.list import ListView
from alephuba.noticias import models
from alephuba.aleph.models import Archivo
from django.contrib.auth.models import User
from django.db.models.aggregates import Count

class NoticiasView(ListView):
    
    template_name = 'home.html'
    paginate_by=3
    queryset = models.Entrada.objects.order_by('-fecha')
    
    
    def get_context_data(self, **kwargs):
        context = super(NoticiasView, self).get_context_data(**kwargs)
        
        archivos = Archivo.objects.order_by('-fecha_subida')[:5]
        usuarios = User.objects.values('username').annotate(Count('archivo')).order_by('-archivo__count')[:5]
        
        context.update({'archivos' : archivos, 'usuarios' : usuarios})
        
        return context