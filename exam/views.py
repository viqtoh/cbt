from django.shortcuts import render
from .models import *
# Create your views here.


def examPage(request, passcode, active, question):
	course = Course.objects.filter(recent=True).first()
	sections = course.sections.all()
	if(active > sections.count()):
		active = sections.count()
	realactive = sections[active -1]
	try:
		realquestion = realactive.questions.all()[question - 1]
		answers = realquestion.options.all()
	except IndexError:
		try:
			realquestion = realactive.questions.all()[0]
			answers = realquestion.options.all()
		except IndexError:
			realquestion = None
			answers = None
	questions = realactive.questions.all()
	context ={
	'sections':sections,
	'active':active,
	'course':course,
	'question':realquestion,
	'questions':questions,
	'passcode':passcode,
	'questionNo':question,
	'answers':answers,
	}
	return render(request, 'exampage.html', context)

def welcome(request, passcode):
	context ={
	'passcode':passcode,
	}
	return render(request, 'welcome.html', context)