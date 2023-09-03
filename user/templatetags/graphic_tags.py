from django import template

register = template.Library()

@register.simple_tag
def checkGraph(object):
	try:
		object.url
		if(object.url ==''):
			return 0
		return 1
	except ValueError:
		return 0
