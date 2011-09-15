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
    
    def __init__(self, *args, **kw):
        
        super(UserCreationForm, self).__init__(*args, **kw)
        
        self.profile_form = UserProfileForm(*args, **kw)
        self.fields.update(self.profile_form.fields)
        self.initial.update(self.profile_form.initial)
    
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        self.errors.update(self.profile_form.errors)
        return cleaned_data
    
    def save(self, commit=True):
        user = super(UserForm, self).save(commit)
        user_profile = self.profile_form.save(commit = False)
        user_profile.user = user
        user_profile.save()
        
        return user
    
    class Meta:
        model = User
        fields = ('username', 'email')

class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        exclude = ('user')