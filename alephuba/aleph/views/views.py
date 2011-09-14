from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from aleph.model_forms import RegistrationForm

def registration(request):
    
    if request.method == 'GET':
        form = RegistrationForm()
    else:
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            form.save()
            
            user = authenticate(username=request.POST['username'],
                                password=request.POST['password1'])
            
            login(request, user)
            
            return HttpResponseRedirect('/')
    
    return render_to_response('registracion.html', {'form' : form}, context_instance=RequestContext(request))    