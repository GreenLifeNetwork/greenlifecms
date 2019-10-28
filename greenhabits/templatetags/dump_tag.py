from django import template

register = template.Library()

# Custom tag for debug
@register.filter()
def dump(var):
    if var:
        return vars(var)
