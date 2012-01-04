# Create your views here.
from django.views.generic.list import ListView
from alephuba.noticias import models

class NoticiasView(ListView):
    
    template_name = 'home.html'
    paginate_by=10
    queryset = models.Entrada.objects.order_by('-fecha')
