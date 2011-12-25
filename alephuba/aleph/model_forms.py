# -*- encoding: utf-8 -*-
'''
Forms para crear/editar modelos.
'''
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from alephuba.aleph.models import Documento, Carrera, UserProfile

class DocumentoModelForm(forms.ModelForm):
    
    class Meta:
        model = Documento
        exclude = ('subido_por',)
        
    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        
        if isbn:
            if (not isbn.isdigit()) or (len(isbn) != 10 and len(isbn) != 13):
                raise forms.ValidationError(
                        """El ISBN debe ser un número de 10 o 13 dígitos.""")
        
        return isbn
        
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

