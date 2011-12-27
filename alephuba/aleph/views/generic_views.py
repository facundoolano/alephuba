'''
Vistas genericas.
'''
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from alephuba.aleph import models
from alephuba.aleph.model_forms import DocumentoModelForm
from alephuba.aleph.isbn_utils import get_OLID

class DocumentoList(ListView):
    """ 
    Listado de documentos, con busqueda rapida incorporada. Se busca en GET
    el termino por el que se filtra el listado.    
    """
    
    template_name = 'documentos/documento_list.html'
    paginate_by=5
    
    def get_queryset(self):
        doc = self.request.GET.get('qs_documento') 
        return models.Documento.objects.busqueda_rapida(doc)
        
    
class DocumentoDetail(DetailView):
    model = models.Documento
    template_name = 'documentos/documento.html'
    context_object_name = 'documento'
    
    def get_context_data(self, **kwargs):

        context = super(DetailView, self).get_context_data(**kwargs)
        
        informacion = models.Vote.objects.obtener_informacion_documento(self.get_object())
        usuario_voto = models.Vote.objects.usuario_ha_votado(self.request.user, self.get_object())

        context['usuario_ya_voto'] = usuario_voto
        context['promedio_rating'] = str(informacion[0]) # casteo feo, pero necesario
        context['cantidad_votos'] = informacion[1]
        
        return context

class DocumentoCreate(CreateView):
    template_name = 'documentos/add_documento.html'
    form_class = DocumentoModelForm
    success_url = '/docs'
    
    def form_valid(self, form):
        """ Agrega al usuario logueado como el que subio el documento. """
        
        form.instance.subido_por = self.request.user
        
        if form.instance.isbn:
            form.instance.olid = get_OLID(form.instance.isbn)
        
        return super(DocumentoCreate, self).form_valid(form)