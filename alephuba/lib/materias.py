'''
Crawler para obtener las materias del wiki de Foros-Fiuba. Requiere los paquetes 'requests' y 'pyquery'.
'''
import requests
from pyquery import PyQuery as pq
from django.db.utils import IntegrityError
from alephuba.aleph.models import Materia

WIKI_URL = 'http://wiki.foros-fiuba.com.ar'

def get_departamentos():
    d = pq(requests.get(WIKI_URL).text)
    departamentos = d('#folded_1 .wikilink1')
    return [WIKI_URL + pq(depto).attr('href') for depto in departamentos]

def get_materias(url_depto):
    d = pq(requests.get(url_depto).text)
    materias_list = d('.idx .wikilink1')
    results = [] 
    for materia in materias_list:
        nombre = pq(materia).html()
        results += nombre.split('/') if '.' in nombre else []
    
    return results

def save_materia(materia):
    m = Materia()    
    m.codigo, m.nombre = materia.rsplit('.', 1)
    print 'Guardando %s' % materia
    try:
        m.save()
    except IntegrityError:
        print 'ERROR al guardar %s' % materia

def load_materias():
    urls_deptos = get_departamentos()
    
    materias = []
    for url in urls_deptos:
        materias += get_materias(url)
    
    Materia.objects.all().delete()
    
    for materia in materias:
        save_materia(materia)
    
load_materias()