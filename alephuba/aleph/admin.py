from django.contrib import admin
from alephuba.aleph.models import Carrera, Materia, Documento, UserProfile, Vote,\
    Archivo

class MateriaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre')

class ArchivoAdmin(admin.ModelAdmin):
    list_display = ('documento', 'link')

admin.site.register(Carrera)
admin.site.register(Materia, MateriaAdmin)
admin.site.register(Documento)
admin.site.register(Archivo, ArchivoAdmin)
admin.site.register(UserProfile)
admin.site.register(Vote)

