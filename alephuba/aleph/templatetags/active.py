from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def active(context, pattern):
    
    request = context['request']
    
    if request.path.startswith(pattern):
        return 'active'
    return ''