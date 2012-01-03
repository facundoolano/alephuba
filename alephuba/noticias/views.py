# Create your views here.
from django.views.generic.list import ListView
from alephuba.noticias import models

class NoticiasView(ListView):
    
    template_name = 'home.html'
    paginate_by=5
    model = models.Entrada
