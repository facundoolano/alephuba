from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from alephuba.aleph.forms import UserForm

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.utils import simplejson as json
from django import http

from alephuba.aleph import models
from alephuba.lib import openlibrary
from django.template.loader import render_to_string
from alephuba.lib.ifileit import Ifileit
from alephuba import settings
from alephuba.aleph.forms import DocumentoModelForm


#FIXME usar class based form view
def registration(request):
    
    if request.method == 'GET':
        form = UserForm()
    else:
        form = UserForm(request.POST)
        
        if form.is_valid():
            form.save()
            
            user = authenticate(username=request.POST['username'],
                                password=request.POST['password1'])
            
            login(request, user)
            
            return HttpResponseRedirect('/')
    
    return render_to_response('registracion.html', {'form' : form}, context_instance=RequestContext(request))

def busqueda_por_materia(request):
    
    return render_to_response('documentos/busqueda_materia.html', {}, context_instance=RequestContext(request))


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
        

class AjaxDocumentoList(DocumentoList):
    """
    Vista para actualizar el listado de documentos sin tener que refrescar la 
    pagina. 
    """
    
    template_name = 'documentos/documento_list_content.html'
    
    def render_to_response(self, context):
        content = render_to_string(self.template_name, context)
        
        return http.HttpResponse(json.dumps({'content' : content}), 
                                 content_type='application/json')


class DocumentoDetail(DetailView):
    model = models.Documento
    template_name = 'documentos/documento.html'
    context_object_name = 'documento'
    
    def get_context_data(self, **kwargs):

        context = super(DetailView, self).get_context_data(**kwargs)
        
        informacion = models.Vote.objects.obtener_informacion_documento(self.get_object())
        usuario_voto = models.Vote.objects.usuario_ha_votado(self.request.user, self.get_object())

        context['usuario_ya_voto'] = usuario_voto
        context['promedio_rating'] = str(round(informacion[0], 1)) # casteo feo, pero necesario
        context['cantidad_votos'] = informacion[1]
        
        return context

class DocumentoCreate(CreateView):
    template_name = 'documentos/add_documento.html'
    form_class = DocumentoModelForm
    success_url = '/docs'
    
    
    def get_context_data(self, **kwargs):
        context = super(DocumentoCreate, self).get_context_data(**kwargs)
        context['site_available'] = Ifileit.ping()
        
        return context
    
    def form_valid(self, form):
        """ 
        Agrega al usuario logueado como el que subio el documento, setea el 
        OLID e intenta hacer upload del archivo subido.
        """
        
        form.instance.subido_por = self.request.user
        
        if form.instance.isbn:
            form.instance.olid = openlibrary.get_OLID(form.instance.isbn)
        
        #manejar upload
        if settings.UPLOAD_ACTIVADO:
            doc_file = form.files['doc_file']
            form.instance.link = Ifileit.upload(doc_file)
        else:
            form.instance.link='http://fake.com'
        
        return super(DocumentoCreate, self).form_valid(form)