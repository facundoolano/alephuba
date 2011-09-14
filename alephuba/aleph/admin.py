from django.contrib import admin
from alephuba.aleph.models import Carrera, Materia, Documento
from aleph.models import UserProfile


admin.site.register(Carrera)
admin.site.register(Materia)
admin.site.register(Documento)
admin.site.register(UserProfile)

