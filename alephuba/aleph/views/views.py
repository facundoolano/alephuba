from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from alephuba.aleph.forms import UserForm, MirrorModelForm, BusquedaMateriaForm,\
    ContactoForm

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.utils import simplejson as json
from django import http

from alephuba.aleph import models
from alephuba.lib import openlibrary
from django.template.loader import render_to_string
from alephuba.lib.ifileit import Ifileit, IfileitApiError
from alephuba import settings
from alephuba.aleph.forms import DocumentoModelForm
from django.core.urlresolvers import reverse
from django.core.mail.message import EmailMessage
from random import shuffle
from alephuba.aleph.models import EXTENSION_MAX_LENGTH
import requests

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
    
    return render_to_response('usuarios/registracion.html', {'form' : form}, context_instance=RequestContext(request))

def contacto(request):

    if request.method == 'GET':
        form = ContactoForm()
    else:
        form = ContactoForm(request.POST)

        if form.is_valid():
            email = EmailMessage(request.user.email + " : " + form.cleaned_data['tema'],
                                 form.cleaned_data['mensaje'], to = settings.ADMINS_EMAILS)
            email.send()

            return render_to_response('exito_contacto.html', {}, context_instance=RequestContext(request))

    return render_to_response('contacto.html', {'form' : form}, context_instance=RequestContext(request))

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

class DocumentoPorMateriaList(ListView):
    """ 
    Busqueda por materia y carrera.    
    """
    
    template_name = 'documentos/busqueda_materia.html'
    paginate_by=5
    
    def get_context_data(self, **kwargs):

        context = super(DocumentoPorMateriaList, self).get_context_data(**kwargs)
        context.update({'form' : BusquedaMateriaForm(self.request.GET) })
        
        return context
    
    def get_queryset(self):
        
        form = BusquedaMateriaForm(self.request.GET)
        form.is_valid()
        
        carrera = form.cleaned_data['carreras']
        materia = form.cleaned_data['materias']
        
        if materia:
            return models.Documento.objects.filter(materia=materia)
        elif carrera:
            return models.Documento.objects.filter(carrera=carrera)
        
        return models.Documento.objects.all()
    

class JSONResponseMixin(object):
    """
    Mixin que renderiza a string un template y lo responde como json 
    """
    
    def render_to_response(self, context):
        content = render_to_string(self.template_name, context)
        
        return http.HttpResponse(json.dumps({'content' : content}), 
                                 content_type='application/json')

class UpdateDocumentoList(JSONResponseMixin, DocumentoList):
    """ Update de la lista de documentos para evitar refrescar. """
    
    template_name = 'documentos/documento_list_content.html'
    
class UpdateDocumentoPorMateriaList(JSONResponseMixin, DocumentoPorMateriaList):
    """ Update de la lista de documentos por materia para evitar refrescar. """
    
    template_name = 'documentos/documento_list_content.html'


class DocumentoDetail(DetailView):
    model = models.Documento
    template_name = 'documentos/documento.html'
    context_object_name = 'documento'
    
    def get_context_data(self, **kwargs):

        context = super(DetailView, self).get_context_data(**kwargs)
        
        documento = self.object

        informacion = models.Vote.objects.obtener_informacion_documento(documento)
        usuario_voto = models.Vote.objects.usuario_ha_votado(self.request.user, documento)

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
    
    def _upload_file(self, doc_file, archivo):
        """
        Si los uploads estan activados, envia el archivo a ifile.it y guarda los
        atributos en el modelo pasado
        """
        
        archivo.tamanio = doc_file.size
        archivo.extension = doc_file.name.split('.')[-1][:EXTENSION_MAX_LENGTH]
        
        if settings.UPLOAD_ACTIVADO:
            self._scramble_name(doc_file)
            archivo.link = Ifileit.upload(doc_file)
        else:
            archivo.link = 'http://fake.com'
        

class DocumentoCreate(ArchivoBaseView):
    template_name = 'documentos/add_documento.html'
    form_class = DocumentoModelForm
    success_url = '/docs'
    
    def _make_archivo(self, form):
        archivo = models.Archivo()
        archivo.documento = self.object
        archivo.subido_por = self.request.user
        self._upload_file(form.files['doc_file'], archivo)
        archivo.save()
    
    def form_valid(self, form):
        """ 
        Setea el OLID en base al ISBN y crea el archivo inlcuido en el form.
        """
        
        if form.instance.isbn:
            form.instance.olid = openlibrary.get_OLID(form.instance.isbn)
            
        response = super(DocumentoCreate, self).form_valid(form)
        
        try:
            self._make_archivo(form)
        except IfileitApiError:
            form.instance.delete()
            return HttpResponseRedirect(reverse('upload_error'))
        
        return response
    

class MirrorCreate(ArchivoBaseView):
    template_name = 'documentos/add_mirror.html'
    form_class = MirrorModelForm
    
    def _load_link(self, archivo, link):
        """ Completa los campos del archivo con la informacion del link. """
        
        archivo.link = link
        archivo.extension = 'link'
        headers = requests.get(link).headers
        
        extension = headers['content-type'].split('/')[-1]
        if extension in settings.UPLOAD_TYPES:
            archivo.extension = extension
            archivo.tamanio = int(headers['content-length'])
            
    
    def get_success_url(self):
        return reverse('documento', args=[self.kwargs['documento_id']])
    
    def form_valid(self, form):
        
        archivo = form.instance
        archivo.documento = models.Documento.objects.get(
                                                id=self.kwargs['documento_id'])
        
        archivo.subido_por = self.request.user
        
        if form.cleaned_data['link']:
            self._load_link(archivo, form.cleaned_data['link'])
        else:
            try:
                self._upload_file(form.files['doc_file'], archivo)
            except:
                return HttpResponseRedirect(reverse('upload_error'))
        
        return super(MirrorCreate, self).form_valid(form)
    