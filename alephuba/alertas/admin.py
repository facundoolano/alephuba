from django.contrib import admin
from alephuba.alertas.models import Alerta

class AlertaAdmin(admin.ModelAdmin):
    list_display = ('archivo', 'motivo', 'autor')

admin.site.register(Alerta, AlertaAdmin)