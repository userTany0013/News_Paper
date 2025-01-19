from django import template


register = template.Library()


a = ["Редиска", "редиска"]


@register.filter()
def currency(value):
    for i in a:
        value = value.replace(i[1:], "*" * len(i[1:]))
    return value
