from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Returns the value for the key in the dictionary, or 0 if the key is not found."""
    return dictionary.get(key, 0)
