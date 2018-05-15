import json

from django import template
from django.http import QueryDict

register = template.Library()


@register.filter
def lookup(list, index):
    return list[index]


@register.filter
def replace(value, args):
    qs = QueryDict(args)

    if 'search' in qs and 'replacement' in qs:
        return value.replace(qs['search'], qs['replacement'])

    return value

@register.filter
def jsondumps(value):
    return json.dumps(value)