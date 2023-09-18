from django.shortcuts import render, redirect
from .models import *
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
# Create your views here.


def examPage(request, passcode, active, question):
	course = Course.objects.filter(active=True).first()
	student = StudentDetails.objects.filter(passcode=passcode).first()
	if(student == None):
		return redirect('user:home')
	exam = student.exams.filter(course=course).first()
	sections = course.sections.all()
	if(sections.count() < 1):
		return redirect('user:home')
	if(exam==None):
		exam = Examination(course=course)
		exam.save()
		student.exams.add(exam)
		student.save()
	if(exam.status == 'submitted'):
		return_url = reverse('exam:submitted', args=[passcode])
		return redirect(return_url)
	start = exam.start
	time = timezone.now()
	realtime = time - start
	allsecs = course.time *60
	seconds = allsecs - realtime.seconds
	if(active > sections.count()):
		active = 1
	realactive = sections[active -1]
	try:
		realquestion = realactive.questions.all()[question - 1]
		answers = realquestion.options.all()
		got = True
	except IndexError:
		try:
			realquestion = realactive.questions.all()[0]
			answers = realquestion.options.all()
			got = True
		except IndexError:
			realquestion = None
			answers = None
			got = False
	except ValueError:
		realquestion = None
		answers = None
		got = False
	inians = None
	if(got):
		for ans in realquestion.options.all():
			for answer in exam.answers.all():
				if (ans.id == answer.id):
					inians = ans
	if (request.method == 'POST'):
		nav=request.POST.get('nav')
		uanswer = request.POST.get('answer')
		if(uanswer != None and uanswer != ''):
			uanswer = int(uanswer)
			ranswer = realquestion.options.all()[uanswer-1]
			uquestion = question
			exam.questions.add(realquestion)
			exam.answers.add(ranswer)
			exam.save()
		submit = request.POST.get('rsubmit')
		if(submit == 'true'):
			exam.status='submitted'
			exam.save()
			return_url = reverse('exam:submitted', args=[passcode])
			return redirect(return_url)
		if(nav=='prev'):
			if(question <= 2):
				question -= 1
			if(question < 1):
				active = active -1
				if(active < 1):
					active = course.sections.all().count()
				try:
					question = Section.objects.filter(id=active).first().questions.all().count()
				except AttributeError:
					question = 1
		else:
			question +=1
			if(question > Section.objects.filter(id=active).first().questions.all().count()):
				active = active + 1
				question = 1
		return_url = reverse('exam:exampage', args=[passcode, active, question])
		return redirect(return_url)
	questions = realactive.questions.all()
	context ={
	'allsecs':allsecs,
	'seconds':seconds,
	'inians':inians,
	'exam':exam,
	'sections':sections,
	'active':active,
	'course':course,
	'question':realquestion,
	'questions':questions,
	'passcode':passcode,
	'questionNo':question,
	'answers':answers,
	'student':student,
	}
	return render(request, 'exampage.html', context)

def welcome(request, passcode):
	student = StudentDetails.objects.filter(passcode=passcode).first()
	exam = student.exams.filter(course__active=True).first()
	if(exam!=None):
		if(exam.status == 'submitted'):
			return_url = reverse('exam:submitted', args=[passcode])
			return redirect(return_url)
	if(student == None):
		return redirect('user:home')
	course = Course.objects.filter(active=True).first()
	context ={
	'student':student,
	'course':course,
	'passcode':passcode,
	}
	return render(request, 'welcome.html', context)

def submitted(request, passcode):
	student = StudentDetails.objects.filter(passcode=passcode).first()
	course = Course.objects.filter(active=True).first()
	exam = student.exams.filter(course__active=True).first()
	context ={
	'exam':exam,
	'course':course,
	'student':student,
	}
	return render(request, 'submitted.html', context)