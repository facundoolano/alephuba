'''
Funciones para obtener informacion a partir del ISBN de un libro.
'''
import urllib2
import json

#TODO ver si estas cosas corresponden en otra parte

URL_INFO = 'http://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data'
URL_COVERS = 'http://covers.openlibrary.org/b/{key}/{value}-{size}.jpg?default=false'

def get_OLID(isbn):
    """
    Consulta en la API de OpenLibrary usando el ISBN indicado, y devuelve el
    OLID del libro.
    """ 
    
    response = urllib2.urlopen(URL_INFO.format(isbn=isbn))
    js_dict = json.loads(response.read())
    key = 'ISBN:{isbn}'.format(isbn=isbn)
    if js_dict.has_key(key):
        return js_dict[key]['identifiers']['openlibrary'][0]
        
    
def get_cover(key, value, size):
    """ 
    Devuelve la url de la imagen de cover del libro. Key es isbn o olid, 
    value su valor y size puede ser S, M o L. 
    """
    
    return URL_COVERS.format(key=key, value=value, size=size)

    