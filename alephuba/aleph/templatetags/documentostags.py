from django import template
from alephuba.settings import MEDIA_URL
from alephuba.lib import openlibrary

register = template.Library()

DOCUMENT_MAP = {
    'LIB' : 'libro.png',
    'APU' : 'apunte.png',
    'INF' : 'informe.png',
    'EXA' : 'examen.png',
    'GEJ' : 'guia.png'
}

@register.filter
def book_cover(documento, arg=False):
    img_src = '{media}img/tipos_documentos/'.format(media=MEDIA_URL) + DOCUMENT_MAP[documento.tipo]
    olid = False
    
    if documento.olid:
        img_src = openlibrary.get_cover('olid', documento.olid, 'M')
        olid = True
    
    if not olid and documento.isbn:
        img_src = openlibrary.get_cover('isbn', documento.isbn, 'M')
    
    return img_src
    

DEFAULT = 'empty.png'
EXTENSION_MAP = {'pdf' : 'pdf.png', 
                 'ps' : 'pdf.png', 
                 'doc' : 'doc.png', 
                 'xls' : 'xls.png', 
                 'rtf' : 'edit.png', 
                 'tex' : 'txt.png',
                 'odt' : 'edit.png', 
                 'jpg' : 'picture.png', 
                 'png' : 'picture.png', 
                 'zip' : 'zip.png', 
                 'rar' : 'zip.png', 
                 'tar.gz' : 'zip.png', 
                 'ppt' : 'ppt.png', 
                 'txt' : 'txt.png',
                 'link' : 'link.png'
                 }

@register.filter
def file_icon(archivo, arg=False):
    img_file = EXTENSION_MAP.get(archivo.extension, DEFAULT)
    
    return '{media}img/icons/{file}'.format(media=MEDIA_URL, file=img_file)