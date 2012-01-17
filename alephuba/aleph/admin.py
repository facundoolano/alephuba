from django.contrib import admin
from alephuba.aleph.models import Carrera, Materia, Documento, UserProfile, Vote,\
    Archivo

admin.site.register(Carrera)
admin.site.register(Materia)
admin.site.register(Documento)
admin.site.register(Archivo)
admin.site.register(UserProfile)
admin.site.register(Vote)

