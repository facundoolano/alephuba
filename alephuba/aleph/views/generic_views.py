'''
Vistas genericas.
'''
from alephuba.aleph import models
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

class DocumentoList(ListView):
    queryset = models.Documento.objects.order_by('fecha_subida')
    template_name = 'documento_list.html'
    paginate_by=5
    
class DocumentoDetail(DetailView):
    model = models.Documento
    template_name = 'documento.html'
    context_object_name = 'documento'