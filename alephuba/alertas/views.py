# Create your views here.
from django.views.generic.edit import CreateView
from django import forms
from alephuba.alertas.models import Alerta
from alephuba.aleph.models import Archivo
from django.core.urlresolvers import reverse
from django.core.mail.message import EmailMessage
from alephuba import settings

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
        
        form.instance.archivo = Archivo.objects.get(id=self.kwargs['archivo_id'])
        form.instance.autor = self.request.user
        is_valid = super(ReportarView, self).form_valid(form)

        if is_valid:
            mensaje = 'Mensaje del usuario %s :\n\n%s' % (self.request.user.username, form.cleaned_data['mensaje'])

            email = EmailMessage("Alerta del documento '" + form.instance.archivo.documento.titulo + "'",
                                 mensaje, to = settings.ADMINS_EMAILS)
            email.send()

        return is_valid
