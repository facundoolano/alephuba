from django import forms


class BusquedaRapidaForm(forms.Form):
    qs_documento = forms.CharField()

def quick_search(request):
    """
    Context processor para agregar la form de busqueda rapida en todas las
    paginas.
    """
    return {'qs_form' : BusquedaRapidaForm()}