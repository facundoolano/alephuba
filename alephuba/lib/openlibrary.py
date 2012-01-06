'''
Funciones para obtener informacion a partir del ISBN de un libro.
'''
import urllib2
import json

URL_INFO = 'http://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd={details}'
URL_COVERS = 'http://covers.openlibrary.org/b/{key}/{value}-{size}.jpg?default=false'

def _info_request(isbn, details):
    response = urllib2.urlopen(URL_INFO.format(isbn=isbn, details=details))
    js_dict = json.loads(response.read())
    key = 'ISBN:{isbn}'.format(isbn=isbn)
    if js_dict.has_key(key):
        return js_dict[key]
    
    return {}

def _get_book_data(isbn):
    return _info_request(isbn, 'data')

def _get_book_details(isbn):
    return _info_request(isbn, 'details').get('details', {})

def get_author_and_title(isbn):
    """ returns a tuple of author -just the first- and title+subtitle. """
    
    info = _get_book_details(isbn)
    
    subtitle = info.get('subtitle', '')
    title = info.get('title', '') + (': ' + subtitle if subtitle else '')
    
    authors = info.get('authors')
    author = authors[0]['name'] if authors else ''
    
    return author, title
    

def get_OLID(isbn):
    """
    Consulta en la API de OpenLibrary usando el ISBN indicado, y devuelve el
    OLID del libro.
    """ 
    return _get_book_data(isbn)['identifiers']['openlibrary'][0]
    
def get_cover(key, value, size):
    """ 
    Devuelve la url de la imagen de cover del libro. Key es isbn o olid, 
    value su valor y size puede ser S, M o L. 
    """
    
    return URL_COVERS.format(key=key, value=value, size=size)

    