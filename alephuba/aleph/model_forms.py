'''
Forms para crear/editar modelos.
'''
from django import forms
from alephuba.aleph import models
from django.contrib.auth.forms import UserCreationForm
from alephuba.aleph.models import UserProfile

class DocumentoModelForm(forms.ModelForm):
    
    class Meta:
        model = models.Documento
        exclude = ('subido_por',)
        
class RegistrationForm(UserCreationForm):
    
    class Meta:
        model = UserProfile
        fields = ("username", "email", "carrera")
    
    