# Create your views here.
from django.views.generic.edit import CreateView
from django import forms
from alephuba.alertas.models import Alerta
from alephuba.aleph.models import Archivo
from django.core.urlresolvers import reverse

class AlertaForm(forms.ModelForm):
    class Meta:
        model = Alerta
        fields = ('motivo', 'mensaje')


class ReportarView(CreateView):
    template_name = 'reportar.html'
    form_class = AlertaForm
    
    def get_success_url(self):
        archivo = Archivo.objects.get(id=int(self.kwargs['archivo_id']))
        documento_id = archivo.documento.id
        return reverse('documento', args=[documento_id])
    
    def form_valid(self, form):
        
        form.instance.archivo = Archivo.objects.get(
                                                id=self.kwargs['archivo_id'])
        form.instance.autor = self.request.user
        return super(ReportarView, self).form_valid(form)
