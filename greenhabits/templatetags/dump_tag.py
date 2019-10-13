from django import template

register = template.Library()
# Custom tag for diagnostics
@register.filter()
def dump(var):
    print('dump var',var )
    return vars(var)
