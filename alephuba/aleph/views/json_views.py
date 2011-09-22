from django.http import HttpResponse
from django.utils import simplejson

from aleph.models import Documento

def autocomplete_documento(request):
    
    termino = request.REQUEST['term']
    lista_documentos = Documento.objects.busqueda_rapida(termino)
    
    opciones = []
    
    for documento in lista_documentos:
        result = documento.titulo if termino.lower() in documento.titulo.lower() else documento.autor 
        opciones.append(result)
    
    return HttpResponse(simplejson.dumps(list(set(opciones))), mimetype='application/json')