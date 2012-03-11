from django.contrib import admin
from alephuba.aleph.models import Carrera, Materia, Documento, UserProfile, Vote,\
    Archivo

class MateriaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre')
    search_fields = ['codigo', 'nombre']

class ArchivoAdmin(admin.ModelAdmin):
    list_display = ('documento', 'link', 'subido_por')
    search_fields = ['subido_por__username', 'documento__titulo']

class DocumentoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'tipo']
    search_fields = ['titulo', 'autor']
    list_filter = ['tipo']

class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'document', 'vote_value']
    search_fields = ['user__username', 'document__titulo']

admin.site.register(Carrera)
admin.site.register(Materia, MateriaAdmin)
admin.site.register(Documento, DocumentoAdmin)
admin.site.register(Archivo, ArchivoAdmin)
admin.site.register(UserProfile)
admin.site.register(Vote, VoteAdmin)

