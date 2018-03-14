from django import template

register = template.Library()

@register.filter
def lookup(list, index):
    return list[index]