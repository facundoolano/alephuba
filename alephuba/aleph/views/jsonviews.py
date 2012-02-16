from django.http import HttpResponse
from django.utils import simplejson

from alephuba.aleph.models import Documento, Vote
from alephuba.lib.openlibrary import get_author_and_title
from alephuba.aleph.forms import is_valid_isbn10, is_valid_isbn13
import json

def autocomplete_documento(request):

    termino = request.REQUEST['term']
    lista_documentos = Documento.objects.busqueda_rapida(termino)

    opciones = []

    for documento in lista_documentos:
        result = documento.titulo if termino.lower() in documento.titulo.lower() else documento.autor 
        opciones.append(result)

    return HttpResponse(simplejson.dumps(list(set(opciones))), mimetype='application/json')

def vote_on_document(request, document_pk, vote):

    sucess = Vote.objects.try_record_vote(document_pk, request.user, vote)

    return HttpResponse(simplejson.dumps(sucess), mimetype='application/json')


def validate_isbn(request):
    isbn = request.POST['isbn']
    valid = not isbn or is_valid_isbn10(isbn) or is_valid_isbn13(isbn)
    
    result = {'valid' : valid}
    if valid:
        result['autor'], result['titulo'] = get_author_and_title(isbn)
    
    return HttpResponse(json.dumps(result), mimetype='application/json')

def validate_doc_unicity(request):
    pass

