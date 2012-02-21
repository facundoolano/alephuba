import requests
import StringIO
from alephuba.lib.ifileit import Ifileit, IfileitApiError
from pyquery import PyQuery as pq
from alephuba.aleph.models import Materia, Archivo, Documento, TITULO_MAX_LENGTH,\
    EXTENSION_MAX_LENGTH
from django.contrib.auth.models import User
import re

APUNTES_URL = 'http://apuntes.foros-fiuba.com.ar'
INCREMENTAL = True

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


def get_filename(request):
    return re.findall("filename=(\S+)", request.headers['Content-Disposition']
                      )[0].replace('"', '')

def upload_archivo(link, archivo):
    request = requests.get(link)
    
    sio = StringIO.StringIO(request.content)
    sio.name = get_filename(request)
    archivo.link = Ifileit.upload(sio)
    
    archivo.extension = sio.name.split('.')[-1][:EXTENSION_MAX_LENGTH]
    archivo.tamanio = int(request.headers.get('Content-Length', 0))
    

def guardar_archivo(materia, nombre, link):
    
    if INCREMENTAL and Documento.objects.filter(materia=materia, 
                                titulo=nombre[:TITULO_MAX_LENGTH]):
        return
    
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
        upload_archivo(link, archivo)
    except IfileitApiError as e:
        print e
        return
    
    archivo.save()

def load_apuntes():
    
    if not INCREMENTAL:
        Documento.objects.all().delete()
        Archivo.objects.all().delete()
    
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