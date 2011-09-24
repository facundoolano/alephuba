from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from alephuba.aleph.model_forms import UserForm
from aleph.models import Vote

VOTE_DIRECTIONS = {'up' : 1, 'down' : -1}

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

def vote_on_document(request, document_pk, direction):
    
    if request.method == 'POST':
        vote_value = VOTE_DIRECTIONS[direction]
        Vote.objects.record_vote(document_pk, request.user, vote_value)
    
    return HttpResponseRedirect('/docs/' + document_pk)