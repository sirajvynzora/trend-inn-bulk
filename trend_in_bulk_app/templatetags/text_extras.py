from django import template

register = template.Library()


@register.filter
def splitlines_nonempty(value):
    """
    Split a text blob into non-empty lines (trimmed).
    Useful for rendering newline-separated fields as <li> items.
    """
    if not value:
        return []
    return [line.strip() for line in str(value).splitlines() if line.strip()]

