'''
Forms para crear/editar modelos.
'''
from django import forms
from alephuba.aleph import models
from django.contrib.auth.forms import UserCreationForm
from alephuba.aleph.models import UserProfile
from django.contrib.auth.models import User

class DocumentoModelForm(forms.ModelForm):
    
    class Meta:
        model = models.Documento
        exclude = ('subido_por',)
        
class UserForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('username', 'email')

class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        exclude = ('user')