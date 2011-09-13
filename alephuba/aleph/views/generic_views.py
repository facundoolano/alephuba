'''
Vistas genericas.
'''
from alephuba.aleph import models
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from alephuba.aleph.model_forms import DocumentoModelForm

class DocumentoList(ListView):
    queryset = models.Documento.objects.order_by('-fecha_subida')
    template_name = 'documento_list.html'
    paginate_by=5
    
class DocumentoDetail(DetailView):
    model = models.Documento
    template_name = 'documento.html'
    context_object_name = 'documento'

class DocumentoCreate(CreateView):
    template_name = 'add_documento.html'
    form_class = DocumentoModelForm
    success_url = '/docs'
    
    def form_valid(self, form):
        """ Agrega al usuario logueado como el que subio el documento. """
        
        form.instance.subido_por = self.request.user        
        return super(DocumentoCreate, self).form_valid(form)