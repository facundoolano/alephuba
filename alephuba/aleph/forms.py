# -*- encoding: utf-8 -*-
from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from alephuba.aleph.models import Documento, Carrera, UserProfile, Archivo,\
    Materia
from alephuba import settings
from alephuba.aleph.fields import ReCaptchaField

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
        doc_file = self.files.get('doc_file')
        
        if doc_file:
        
            if doc_file._size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(
                        """El archivo no puede superar los 100mb.""")
            
            file_type = doc_file.name.split('.')[-1]
            if file_type not in settings.UPLOAD_TYPES:
                raise forms.ValidationError("""Formato no permitido.""")
        
        return doc_file 

class DocumentoModelForm(ArchivoBaseForm):

    isbn = forms.CharField(label='ISBN', required=False, 
                           widget=forms.TextInput(attrs={'maxlength' : 17}))
    
    class Meta:
        model = Documento
        exclude = ('olid')
        
    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn').upper().strip().replace('-', '')
        
        if isbn and not is_valid_isbn10(isbn) and not is_valid_isbn13(isbn):
            raise forms.ValidationError(
                    """El ISBN debe ser un número de 10 o 13 dígitos.""")
        
        return isbn

class MirrorModelForm(ArchivoBaseForm):
    
    fuente = forms.ChoiceField(label='Fuente', choices=(('ARC', 'Archivo'), 
                                                  ('URL', 'Dirección URL')))
    
    doc_file = forms.FileField(label='Archivo', required=False)
    link = forms.URLField(label='URL', required=False)
    
    def clean(self):
        cleaned_data = super(MirrorModelForm, self).clean()
        
        if cleaned_data['fuente'] == 'ARC':
            if not self.files.get('doc_file'):
                msg = u'Este campo es obligatorio'
                self._errors['doc_file'] = self.error_class([msg])
        else:
            if not cleaned_data['link']:
                msg = u'Este campo es obligatorio'
                self._errors['link'] = self.error_class([msg])
                del cleaned_data['link']
        
        return cleaned_data
    
    class Meta:
        model = Archivo
        fields = ('fuente', 'doc_file', 'link')

class UserForm(UserCreationForm):
    
    carrera = forms.ModelChoiceField(queryset=Carrera.objects.all(), required=False)
    captcha = ReCaptchaField()
    
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

class BusquedaMateriaForm(forms.Form):
    carreras = forms.ModelMultipleChoiceField(queryset=Carrera.objects.con_documentos(), required=False)
    materias = forms.ModelMultipleChoiceField(queryset=Materia.objects.con_documentos(), required=False)
    