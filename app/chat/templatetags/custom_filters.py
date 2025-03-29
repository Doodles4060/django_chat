from django import template
from datetime import datetime

register = template.Library()

@register.filter
def formatiso(date: datetime):
    return date.isoformat()
