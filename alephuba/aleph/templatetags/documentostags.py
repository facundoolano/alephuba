from django import template
from alephuba.settings import MEDIA_URL
from alephuba.aleph.isbn_utils import get_cover

register = template.Library()

@register.filter
def book_cover(documento, arg=False):
    img_src = ''
    
    if documento.olid:
        img_src = get_cover('olid', documento.olid, 'M')
    
    if not img_src and documento.isbn:
        img_src = get_cover('isbn', documento.isbn, 'M')
    
    return img_src or '{media}img/Blank.jpg'.format(media=MEDIA_URL)
    
