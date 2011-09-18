from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from alephuba.aleph.model_forms import UserForm
from django.utils import simplejson
from aleph.models import Documento

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

def autocomplete_documento(request):
    
    doc = request.REQUEST['term']
        
    options =  [documento.titulo for documento in Documento.objects.busqueda_rapida(doc)]
    
    return HttpResponse(simplejson.dumps(options), mimetype='application/json')    
        