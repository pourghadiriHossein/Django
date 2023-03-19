from django import template

register = template.Library()

@register.filter
def add_poulstar(value):
    return f"Poulstar: {value}"


@register.filter
def add_something(value, something):
    return f"{something}: {value}"
