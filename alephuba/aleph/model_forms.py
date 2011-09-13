'''
Forms para crear/editar modelos.
'''
from django import forms
from alephuba.aleph import models

class DocumentoModelForm(forms.ModelForm):
    
    class Meta:
        model = models.Documento
        exclude = ('subido_por',)