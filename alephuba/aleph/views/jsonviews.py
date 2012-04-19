from django.http import HttpResponse
from django.utils import simplejson

from alephuba.aleph.models import Documento, Vote, Materia, DescargaDocumento
from alephuba.lib.openlibrary import get_author_and_title
from alephuba.aleph.forms import is_valid_isbn10, is_valid_isbn13
import json

from datetime import datetime

def autocomplete_documento(request):

    termino = request.REQUEST['term'] + '*'
    opciones = Documento.objects.sugerencias(termino, limite=7)

    return HttpResponse(simplejson.dumps(opciones), mimetype='application/json')

def autocomplete_autor(request):
    termino = request.REQUEST['term'].lower()
    autores = Documento.objects.filter(autor__icontains=termino).values_list('autor', flat=True).distinct()
    
    return HttpResponse(simplejson.dumps(list(autores)), mimetype='application/json')

def vote_on_document(request, document_pk, vote):

    sucess = Vote.objects.try_record_vote(document_pk, request.user, vote)

    return HttpResponse(simplejson.dumps(sucess), mimetype='application/json')

def contar_descarga(request, document_pk):

    documento = Documento.objects.get(pk=document_pk)

    if DescargaDocumento.objects.filter(usuario=request.user, documento=documento, fecha=datetime.now().date()).exists():
        return HttpResponse('', mimetype='application/json')

    try:
        descarga = DescargaDocumento(usuario=request.user, documento=documento)
        descarga.save()
        return HttpResponse('sucess', mimetype='application/json')
    except:
        return HttpResponse('failure', mimetype='application/json')

def get_materias(request):
    depto = int(request.GET['departamento'])
    materias = list(Materia.objects.con_documentos().filter(
                    departamento__id=depto).values('id', 'codigo', 'nombre'))
    
    return HttpResponse(simplejson.dumps(materias), mimetype='application/json')

def validate_isbn(request):
    
    isbn = request.POST['isbn'].upper().strip().replace('-', '')
    result = {'valid' : True, 'autor' : '', 'titulo' : ''}
    
    if isbn:
        valid = is_valid_isbn10(isbn) or is_valid_isbn13(isbn)

        result['valid'] = valid

        if valid:
            result['autor'], result['titulo'] = get_author_and_title(isbn)
    
    return HttpResponse(json.dumps(result), mimetype='application/json')

def validate_doc_unicity(request):
    pass

