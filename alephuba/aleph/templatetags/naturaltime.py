from datetime import date, datetime

from django import template
from django.template import defaultfilters
from django.utils.translation import pgettext, ungettext, ugettext as _
from datetime import timedelta, tzinfo

register = template.Library()

ZERO = timedelta(0)

class UTC(tzinfo):
    """
    UTC implementation taken from Python's docs.

    Used only when pytz isn't available.
    """

    def __repr__(self):
        return "<UTC>"

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO

utc = UTC()

def is_aware(value):
    """
    Determines if a given datetime.datetime is aware.

    The logic is described in Python's docs:
    http://docs.python.org/library/datetime.html#datetime.tzinfo
    """
    return value.tzinfo is not None and value.tzinfo.utcoffset(value) is not None

#PARCHEADO A MANO PARA NO USAR INTERNATIONALIZATION Y DESCARTANDO FECHAS FUTURAS
@register.filter
def naturaltime(value):
    """
    For date and time values shows how many seconds, minutes or hours ago
    compared to current timestamp returns representing string.
    """
    if not isinstance(value, date): # datetime is a subclass of date
        return value

    now = datetime.now(utc if is_aware(value) else None)
    if value < now:
        delta = now - value
        if delta.days != 0:
            return 'hace %(delta)s' % {'delta': defaultfilters.timesince(value)}
        elif delta.seconds == 0:
            return 'ahora'
        elif delta.seconds < 60:
            return u'hace %(count)s segundos' % {'count': delta.seconds}
        elif delta.seconds // 60 < 60:
            count = delta.seconds // 60
            return u'hace %(count)s minutos' % {'count': count}
        else:
            count = delta.seconds // 60 // 60
            return u'hace %(count)s horas' % {'count': count}
