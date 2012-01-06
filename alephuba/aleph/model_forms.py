# -*- encoding: utf-8 -*-
'''
Forms para crear/editar modelos.
'''
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from alephuba.aleph.models import Documento, Carrera, UserProfile
from django.http import HttpResponse
import json
from alephuba.lib.openlibrary import get_author_and_title


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


#TODO json views?
def validate_isbn(request):
    isbn = request.POST['isbn']
    valid = not isbn or is_valid_isbn10(isbn) or is_valid_isbn13(isbn)
    
    result = {'valid' : valid}
    if valid:
        result['autor'], result['titulo'] = get_author_and_title(isbn)
    
    return HttpResponse(json.dumps(result), mimetype='application/json')

class DocumentoModelForm(forms.ModelForm):
    
    doc_file = forms.FileField(label='Archivo') 
    
    class Meta:
        model = Documento
        exclude = ('subido_por', 'olid', 'link')
        
    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn').upper()
        
        if isbn and not is_valid_isbn10(isbn) and not is_valid_isbn13(isbn):
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

