'''
Funciones para obtener informacion a partir del ISBN de un libro.
'''
import urllib2
import json

#TODO ver si estas cosas corresponden en otra parte

URL = 'http://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data'

def get_OLID(isbn):
    """
    Consulta en la API de OpenLibrary usando el ISBN indicado, y devuelve el
    OLID del libro.
    """ 
    
    response = urllib2.urlopen(URL.format(isbn=isbn))
    js_dict = json.loads(response.read())
    key = 'ISBN:{isbn}'.format(isbn=isbn)
    if js_dict.has_key(key):
        return js_dict[key]['identifiers']['openlibrary']
        
    
