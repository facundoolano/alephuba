from django import template
from alephuba.settings import MEDIA_URL
from alephuba.aleph.isbn_utils import get_cover
import urllib2

register = template.Library()

@register.filter
def book_cover(documento, arg=False):
    img_src = ''
    
    if documento.olid:
        img_src = get_cover('olid', documento.olid, 'M')
    
    if documento.isbn:
        img_src = get_cover('isbn', documento.isbn, 'M')
    
    if img_src:
        try:
            urllib2.urlopen(img_src)
            return img_src
        except urllib2.URLError:
            pass
    
    #Cover generica
    return '{media}img/Blank.jpg'.format(media=MEDIA_URL)
    
