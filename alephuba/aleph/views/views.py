from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from alephuba.aleph.forms import UserForm, MirrorModelForm

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
from django.core.urlresolvers import reverse
from random import shuffle


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


class ArchivoBaseView(CreateView):
    """ Clase base para una view que crea una instancia de Archivo. """

    def get_context_data(self, **kwargs):
        context = super(ArchivoBaseView, self).get_context_data(**kwargs)
        context['site_available'] = Ifileit.ping()
        
        return context
    
    def _scramble_name(self, doc_file):
        """ Separa nombre y extension, y mezcla el nombre. """
        
        terms = doc_file.name.split('.')
        extension = terms.pop()
        
        name_list = list('.'.join(terms))
        shuffle(name_list)
        
        doc_file.name = ''.join(name_list) + '.' + extension
    
    def _get_upload_link(self, doc_file):
        """
        Si los uploads estan activados, envia el archivo a ifile.it y crea
        la instancia de Archivo.
        """
        
        if settings.UPLOAD_ACTIVADO:
            self._scramble_name(doc_file)
            return Ifileit.upload(doc_file)
        
        return "http://fake.com"
    

class DocumentoCreate(ArchivoBaseView):
    template_name = 'documentos/add_documento.html'
    form_class = DocumentoModelForm
    success_url = '/docs'
    
    def _make_archivo(self, form):
        archivo = models.Archivo()
        archivo.documento = self.object
        archivo.detalles = form.cleaned_data['detalles']
        archivo.subido_por = self.request.user
        archivo.link = self._get_upload_link(form.files['doc_file'])
        archivo.save()
    
    def form_valid(self, form):
        """ 
        Setea el OLID en base al ISBN y crea el archivo inlcuido en el form.
        """
        
        if form.instance.isbn:
            form.instance.olid = openlibrary.get_OLID(form.instance.isbn)
            
        response = super(DocumentoCreate, self).form_valid(form)
        
        self._make_archivo(form)
        
        return response
    

class MirrorCreate(ArchivoBaseView):
    template_name = 'documentos/add_mirror.html'
    form_class = MirrorModelForm
    
    def get_success_url(self):
        return reverse('documento', args=[self.kwargs['documento_id']])
    
    def form_valid(self, form):
        
        archivo = form.instance
        archivo.documento = models.Documento.objects.get(
                                                id=self.kwargs['documento_id'])
        archivo.subido_por = self.request.user
        archivo.link = (form.cleaned_data['link'] or 
                        self._get_upload_link(form.files['doc_file']))
        
        return super(MirrorCreate, self).form_valid(form)
    