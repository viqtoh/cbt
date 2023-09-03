from django import template

register = template.Library()

@register.simple_tag
def checklet(num):
	lets =('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')
	return (lets[num-1].upper())
