from django import template
from datetime import datetime, timedelta
from django.utils.timesince import timesince
from django.utils.timezone import utc

register = template.Library()

@register.filter
def div( dividend, divisor ):
    """
    Divides the dividend by divisor, returns float upto one decimal point.
    Returns empty string on any error.
    """
    try:
        dividend = float( dividend )
        divisor = float( divisor )
        return round((dividend / divisor), 1)
    except: pass
    return ''

@register.filter    
def subtract(value, arg):
    return value - arg

@register.filter
def feed_time(value):
    now = datetime.utcnow().replace(tzinfo=utc)
    try:
        difference = now - value
    except:
        return value

    #difference = now - value
    
    if  value.strftime('%y') != now.strftime('%y'):
		return value.strftime('%d')+' '+value.strftime('%b')+' '+value.strftime('%y')
    
    if difference < timedelta(minutes=1):
        return 'just now'
    elif difference < timedelta(hours=1):
		return timesince(value).split(' ')[0]# + 'm'
    elif difference < timedelta(days=1):
		return timesince(value).split(',')[0]# + 'h'
    elif difference >= timedelta(days=1):
		return value.strftime('%d')+' '+value.strftime('%b')

@register.filter
def set_length(text, text_length):
	if len(text) > text_length:
		return (text[0:text_length]) + '...'
	else:
		return text
