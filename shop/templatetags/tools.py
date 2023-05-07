from django import template
register = template.Library()


@register.filter()
def showPrice(value):
    return int(value)
@register.filter()
def mines(value, arg):
    exe = value - arg
    return int(exe)
@register.filter()
def calculateDiscount(value, arg):
    deprice = value*arg/100
    new_price = value-deprice
    return int(new_price)
@register.filter()
def multiple(value, arg):
    final_price = value * arg
    return int(final_price)