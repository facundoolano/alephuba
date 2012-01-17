# -*- encoding: utf-8 -*-
from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from alephuba.aleph.models import Documento, Carrera, UserProfile, Archivo
from alephuba import settings


def is_valid_isbn10(isbn):
    if len(isbn) != 10:
        return False
    
    if not isbn[:9].isdigit():
        return False
    
    if not isbn[9].isdigit() and isbn[9] != 'X':
        return False
    
    return True

def is_valid_isbn13(isbn):
    return len(isbn) == 13 and isbn.isdigit()

class ArchivoBaseForm(forms.ModelForm):
    """ Form base para la subida de un archivo. """
    
    doc_file = forms.FileField(label='Archivo')
    
    def clean_doc_file(self):
        doc_file = self.cleaned_data['doc_file']
        
        if not doc_file:
            return doc_file
        
        if doc_file._size > settings.MAX_UPLOAD_SIZE:
            raise forms.ValidationError(
                    """El archivo no puede superar los 100mb.""")
        
        file_type = doc_file.name.split('.')[-1]
        if file_type not in settings.UPLOAD_TYPES:
            raise forms.ValidationError("""Formato no permitido.""")
        
        return doc_file 

class DocumentoModelForm(ArchivoBaseForm):
    
    detalles = forms.CharField(label='Detalles', widget=forms.Textarea())
    
    class Meta:
        model = Documento
        exclude = ('olid')
        
    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn').upper()
        
        if isbn and not is_valid_isbn10(isbn) and not is_valid_isbn13(isbn):
            raise forms.ValidationError(
                    """El ISBN debe ser un número de 10 o 13 dígitos.""")
        
        return isbn

class MirrorModelForm(ArchivoBaseForm):
    
    fuente = forms.ChoiceField(label='Fuente', choices=(('ARC', 'Archivo'), 
                                                  ('URL', 'Dirección URL')))
    
    doc_file = forms.FileField(label='Archivo', required=False)
    link = forms.URLField(label='URL', required=False)
    
    class Meta:
        model = Archivo
        fields = ('fuente', 'doc_file', 'link', 'detalles')

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

class BusquedaRapidaForm(forms.Form):
    qs_documento = forms.CharField()

def quick_search(request):
    """
    Context processor para agregar la form de busqueda rapida en todas las
    paginas.
    """
    return {'qs_form' : BusquedaRapidaForm()}