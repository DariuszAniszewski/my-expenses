import math
from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()


def pln(int_amount):
    zloty = math.floor(int_amount / 100)
    grosz = int_amount - 100 * zloty
    return f"{intcomma(zloty)},{grosz} PLN"


register.filter('pln', pln)
