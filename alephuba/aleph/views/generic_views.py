'''
Vistas genericas.
'''
from alephuba.aleph import models
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from alephuba.aleph.model_forms import DocumentoModelForm
from alephuba.aleph.forms import BusquedaRapidaForm

class DocumentoList(ListView):
    """ Listado de documentos, con busqueda rapida incorporada. """
    
    template_name = 'documento_list.html'
    paginate_by=5
    
    def get_context_data(self, **kwargs):
        context = super(DocumentoList, self).get_context_data(**kwargs)
        context.update({'form' : BusquedaRapidaForm()})
        return context
    
    def get_queryset(self):
        doc = self.request.GET.get('documento') 
        if doc:
            return models.Documento.objects.busqueda_rapida(doc)
        
        return models.Documento.objects.order_by('-fecha_subida')
        
    
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