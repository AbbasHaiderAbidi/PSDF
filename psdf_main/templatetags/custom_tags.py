from django import template

register = template.Library()

@register.simple_tag
def multiply(qty, unit_price):
    return round(qty * unit_price)


@register.simple_tag
def substract(a, b):
    return round(a - b)
    

@register.simple_tag
def roundoff(abc):
    if len(str(abc))>=8:
        return str(round(float(abc)/10000000,2))+' Cr' 
    if len(str(abc))>=6:
        return str(round(float(abc)/100000,2))+' Lakhs'
    else:
        return str(abc)
    
