from django.http import HttpResponse
from django.utils import simplejson

from alephuba.aleph.models import Documento, Vote
from alephuba.lib.openlibrary import get_author_and_title
from alephuba.aleph.forms import is_valid_isbn10, is_valid_isbn13
import json


def get_suggestions(documento, term):
    """ 
    Dado un documento, extrae los nombres que se deben mostrar como su 
    sugerencia.
    """
    
    results = []
    if term in documento.titulo.lower():
        results.append(documento.titulo)
    
    if documento.autor and term in documento.autor.lower():
        results.append(documento.autor)
        
    for materia in documento.materia.all():
        if term in materia.nombre.lower() or term in materia.codigo.lower():
            results.append(unicode(materia))
    
    return results

LIMITE_SUGERENCIAS = 7

def autocomplete_documento(request):

    termino = request.REQUEST['term'].lower()
    lista_documentos = Documento.objects.busqueda_rapida(termino)

    opciones = []

    for documento in lista_documentos:
        opciones += get_suggestions(documento, termino)
        
        #deja de iterar cuando alcanzo el limite
        opciones = list(set(opciones))
        if len(opciones) >= LIMITE_SUGERENCIAS:
            opciones = opciones[:LIMITE_SUGERENCIAS]
            break 
        
    return HttpResponse(simplejson.dumps(opciones), mimetype='application/json')

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

