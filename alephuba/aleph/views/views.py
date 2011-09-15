from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from alephuba.aleph.model_forms import UserForm
from aleph.model_forms import UserProfileForm

def registration(request):
    
    if request.method == 'GET':
        user_form = UserForm()
        user_profile_form = UserProfileForm()
    else:
        user_form = UserForm(request.POST)
        user_profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and user_profile_form.is_valid():
            user = user_form.save()
            user_profile = user_profile_form.save(commit = False)
            user_profile.user = user
            user_profile.save()
            
            user = authenticate(username=request.POST['username'],
                                password=request.POST['password1'])
            
            login(request, user)
            
            return HttpResponseRedirect('/')
    
    return render_to_response('registracion.html', {'form' : user_form, 'p_form' : user_profile_form}, context_instance=RequestContext(request))    