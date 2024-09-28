from django import template

register = template.Library()

@register.filter
def get_dosagem(receita):
    return receita.dosagem  # Ou a lógica que você precisar
