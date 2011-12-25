from django.http import HttpResponse
from django.utils import simplejson

from alephuba.aleph.models import Documento, Vote

VOTE_DIRECTIONS = {'up' : 1, 'down' : -1}

def autocomplete_documento(request):

    termino = request.REQUEST['term']
    lista_documentos = Documento.objects.busqueda_rapida(termino)

    opciones = []

    for documento in lista_documentos:
        result = documento.titulo if termino.lower() in documento.titulo.lower() else documento.autor 
        opciones.append(result)

    return HttpResponse(simplejson.dumps(list(set(opciones))), mimetype='application/json')

def vote_on_document(request, document_pk, direction):

    vote_value = VOTE_DIRECTIONS[direction]
    sucess = Vote.objects.try_record_vote(document_pk, request.user, vote_value)

    return HttpResponse(simplejson.dumps(sucess), mimetype='application/json')