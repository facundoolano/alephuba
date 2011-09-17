'''
Forms para crear/editar modelos.
'''
from django import forms
from alephuba.aleph import models
from django.contrib.auth.forms import UserCreationForm
from alephuba.aleph.models import UserProfile
from django.contrib.auth.models import User
from alephuba.aleph.models import Carrera

class DocumentoModelForm(forms.ModelForm):
    
    class Meta:
        model = models.Documento
        exclude = ('subido_por',)
        
class UserForm(UserCreationForm):
    
    carrera = forms.ModelChoiceField(queryset=Carrera.objects.all(), required=False)  
    
    def save(self, commit=True):
        user = super(UserForm, self).save(commit)
        
        user_profile = UserProfile()
        user_profile.carrera = self.cleaned_data['carrera']
        user_profile.user = user
        
        user_profile.save()
        
        return user
    
    class Meta:
        model = User
        fields = ('username', 'email')

