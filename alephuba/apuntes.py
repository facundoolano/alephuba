import requests
import StringIO
from alephuba.lib.ifileit import Ifileit, IfileitApiError
from pyquery import PyQuery as pq
from alephuba.aleph.models import Materia, Archivo, Documento, TITULO_MAX_LENGTH
from django.contrib.auth.models import User

APUNTES_URL = 'http://apuntes.foros-fiuba.com.ar'

def get_links(url):
    d = pq(requests.get(APUNTES_URL + url).text)
    links = d('.entry a')
    return [pq(link).attr('href') for link in links]


def get_archivos(url):
    d = pq(requests.get(APUNTES_URL + url).text)
    divs_archivos = d('.file')
    
    archivos = []
    for div in divs_archivos:
        nombre = pq(div).find('h4').html()
        link = APUNTES_URL + pq(div).find('.download a').attr('href')
        archivos.append((nombre, link))
    
    return archivos

def upload_archivo(nombre, link):
    r = requests.get(link)
    sio = StringIO.StringIO(r.content)
    sio.name = nombre
    return Ifileit.upload(sio)

def guardar_archivo(materia, nombre, link):
    
    print "Procesando archivo", nombre
    
    doc = Documento()
    doc.titulo = nombre[:TITULO_MAX_LENGTH]
    doc.tipo= 'APU'
    doc.save()
    doc.materia.add(materia)
    doc.save()
    
    archivo = Archivo()
    archivo.documento = doc
    archivo.subido_por = User.objects.get(id=1)
    
    try:
        archivo.link = upload_archivo(nombre, link)
    except IfileitApiError as e:
        print e
        return
    
    archivo.save()

def load_apuntes():
    
    for depto in get_links('/apuntes'):
        for materia in get_links(depto):
            codigo = materia.split('/', 2)[2].replace('/', '.')[:-1]
            
            print "procesando", codigo
            m_model = Materia.objects.filter(codigo=codigo)
            if not m_model:
                print "Materia no existente"
                continue
            
            for archivo in get_archivos(materia):
                guardar_archivo(m_model[0], *archivo)
            
load_apuntes()