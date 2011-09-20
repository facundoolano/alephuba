from django.http import HttpResponse
from django.utils import simplejson

from aleph.models import Documento

def autocomplete_documento(request):
    
    doc = request.REQUEST['term']
        
    options = [documento.titulo for documento in Documento.objects.busqueda_rapida(doc)]
    
    return HttpResponse(simplejson.dumps(options), mimetype='application/json')