from django import forms


class BusquedaRapidaForm(forms.Form):
    documento = forms.CharField()
