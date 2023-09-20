from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from exam.models import *
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from django.urls import reverse
import random
from django.contrib.sessions.models import Session
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.

@login_required(login_url='', redirect_field_name='next')
def notifications(request):
	return render(request, 'notifications.html')

def sign_in(request):
	if(request.method=='POST'):
		email = request.POST['email']
		password = request.POST['password']
		user = authenticate(email=email, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect('user:admin')
			else:
				err= 'user account suspended'
				context={
				'error':err,
				'email':email,
				}
				return render(request, 'sign-in.html', context)
		else:
				err= 'incorrect username or password'
				context={
				'error':err,
				'email':email,
				}
				return render(request, 'sign-in.html', context)

	else:
		return render(request, 'sign-in.html')

@login_required(login_url='', redirect_field_name='next')
def admin(request):
	courses = Course.objects.all().order_by('-pk')
	if(request.method == 'POST'):
		name = request.POST.get('name')
		description = request.POST.get('description')
		time = request.POST.get('time')
		submit = request.POST.get('submit')
		show = request.POST.get('show')
		if(show == 'on'):
			show = True
			submit = ''
		else:
			show = False
		time = int(time)
		nwcourse = Course(name = name, description = description, time =time, submit=submit, show=show)
		nwcourse.save()
	context = {
	'courses':courses,
	}
	return render(request, 'courses.html', context)

@login_required(login_url='', redirect_field_name='next')
def sections(request, id):
	course = Course.objects.filter(id=id).first()
	sections = course.sections.all().order_by('-pk')
	if (request.method== 'POST'):
		name = request.POST.get('name')
		description = request.POST.get('description')
		submit = request.POST.get('submit')
		time = request.POST.get('time')
		show = request.POST.get('show')
		try:
			time = int(time)
		except ValueError:
			timeL = time.split('.')
			time= timeL[0]
			try:
				time = int(time)
			except ValueError:
				time = 1
		course.name = name
		course.description=description
		course.time=time
		if(show == 'on'):
			course.show = True
		else:
			course.show =False
			course.submit=submit
		course.save()
	context = {
	'course':course,
	'sections':sections,
	}
	return render(request, 'sections.html', context)

@login_required(login_url='', redirect_field_name='next')
def addSection(request, id):
	course = Course.objects.filter(id=id).first()
	if (request.method=='POST'):
		name = request.POST.get('name')
		section = Section(name=name)
		section.save()
		course.sections.add(section)
		course.save()
		return_url = return_url = reverse('user:sections', args=[id])
		return redirect(return_url)
	context ={
	'course':course,
	}
	return render(request, 'addsection.html', context)

@login_required(login_url='', redirect_field_name='next')
def questions(request, id):
	section = Section.objects.filter(id=id).first()
	questions = section.questions.all()
	if(request.method == 'POST'):
		question = request.POST.get('question')
		try:
			image = request.FILES['image']
		except MultiValueDictKeyError:
			image = ''
		answer1 = request.POST.get('answer1')
		answer2 = request.POST.get('answer2')
		answer3 = request.POST.get('answer3')
		answer4 = request.POST.get('answer4')
		answer = request.POST.get('answer')
		answer = int(answer)
		answer1 = Answer(answer=answer1)
		answer2 = Answer(answer=answer2)
		answer3 = Answer(answer=answer3)
		answer4 = Answer(answer=answer4)
		answer1.save()
		answer2.save()
		answer3.save()
		answer4.save()
		nquestion = Question(question=question, image=image)
		nquestion.save()
		nquestion.options.add(answer1,answer2,answer3,answer4)
		nquestion.save()
		options = nquestion.options.all()
		ans = options[answer-1]
		nquestion.answer=ans
		nquestion.save()
		section.questions.add(nquestion)
		section.save()
	context = {
	'section':section,
	'questions':questions,
	}
	return render(request, 'questions.html', context)

@login_required(login_url='', redirect_field_name='next')
def deleteQ(request,section_id, id):
	question = Question.objects.filter(id=id)
	question.delete()
	return_url = return_url = reverse('user:questions', args=[section_id])
	return redirect(return_url)

def sign_up_complete(request,email,first_name,last_name):
	if(request.method=='POST'):
		bvn = request.POST.get('bvn')
		nin = request.POST.get('nin')
		home = request.POST.get('home')
		number = request.POST.get('number')
		gender = request.POST.get('gender')
		marital = request.POST.get('marital')
		nwApplication = UserApplication(Email=email, First_name=first_name,Last_name=last_name,Bvn=bvn,Nin=nin,Home_address=home,Gender=gender, Marital_status=marital, Phone_number=number)
		nwApplication.save()
		return redirect('user:sign_up_success')
	return render(request, 'sign-up-complete.html')

def sign_up_success(request):
	return render(request, 'sign-up-success.html')

@login_required(login_url='', redirect_field_name='next')
def sign_out(request):
	user = request.user
	logout(request)
	return redirect('user:sign_in')

def home(request):
	course = Course.objects.filter(active=True).first()
	error= ''
	if (request.method=='POST'):
		passcode = request.POST.get('passcode')
		student = StudentDetails.objects.filter(passcode=passcode).first()
		if (student != None):
			return_url = reverse('exam:welcome', args=[passcode])
			return redirect(return_url)
		else:
			error = 'Invalid Passcode!'
	context ={
	'error':error,
	'course':course,
	}
	return render(request,'home.html', context)

@login_required(login_url='', redirect_field_name='next')
def deleteCourse(request, id):
	course = Course.objects.filter(id=id).first()
	course.delete()
	return redirect('user:admin')

@login_required(login_url='', redirect_field_name='next')
def deleteSection(request, id):
	section = Section.objects.filter(id=id).first()
	course = Course.objects.filter(sections__id=section.id).first()
	section.delete()
	return_url = return_url = reverse('user:sections', args=[course.id])
	return redirect(return_url)

@login_required(login_url='', redirect_field_name='next')
def makeActive(request, id):
	courses = Course.objects.all()
	course = courses.filter(id=id).first()
	for c in courses:
		c.active=False
		c.save()
	course.active=True
	course.save()
	return_url = return_url = reverse('user:sections', args=[course.id])
	return redirect(return_url)

@login_required(login_url='', redirect_field_name='next')
def studentDetails(request):
	students = StudentDetails.objects.all().order_by('-pk')
	if (request.method == 'POST'):
		rid =request.POST.get('id',None)
		if(rid == None):
			search = request.POST.get('search',None)
			if(search != None):
				return_url = return_url = reverse('user:studentsSearch', args=[search])
				return redirect(return_url)
			else:
				name = request.POST.get('name')
				reg = request.POST.get('reg')
				got = False
				while(got == False):
					passcode = ''
					for i in range(8):
						passr = random.randint(0,9)
						passcode += str(passr)
					if(StudentDetails.objects.filter(passcode=passcode).first() == None):
						got = True
						print('True')
						print(passcode)
					else:
						print('False')
						print(passcode)
				student = StudentDetails(name =name, passcode=passcode, reg=reg)
				student.save()
		else:
			student = StudentDetails.objects.filter(id=rid).first()
			action = request.POST.get('action')
			print(action)
			if(action == 'delete'):
				student.delete()
			if(action == 'status'):
				if(student.status == 'active'):
					student.status = 'inactive'
				else:
					student.status = 'active'
				student.save()
	paginator = Paginator(students, 20)
	page = request.GET.get('page')
	try:
		students = paginator.page(page)
	except PageNotAnInteger:
		students = paginator.page(1)
	except EmptyPage:
		students = paginator.page(paginator.num_pages)
	context = {
	'students':students,
	'page': page,
	}
	return render(request, 'students.html', context)

@login_required(login_url='', redirect_field_name='next')
def studentDetailsSearch(request, search):
	students = StudentDetails.objects.filter(name__contains=search).order_by('-pk')
	if (request.method == 'POST'):
		rid =request.POST.get('id',None)
		if(rid == None):
			rsearch = request.POST.get('search',None)
			if(rsearch != None):
				return_url = return_url = reverse('user:studentsSearch', args=[rsearch])
				return redirect(return_url)
			else:
				name = request.POST.get('name')
				got = False
				while(got == False):
					passcode = ''
					for i in range(8):
						passr = random.randint(0,9)
						passcode += str(passr)
					if(StudentDetails.objects.filter(passcode=passcode).first() == None):
						got = True
						print('True')
						print(passcode)
					else:
						print('False')
						print(passcode)
				student = StudentDetails(name =name, passcode=passcode)
				student.save()
		else:
			student = StudentDetails.objects.filter(id=rid).first()
			if(student.status == 'active'):
				student.status = 'inactive'
			else:
				student.status = 'active'
			student.save()
	paginator = Paginator(students, 20)
	page = request.GET.get('page')
	try:
		students = paginator.page(page)
	except PageNotAnInteger:
		students = paginator.page(1)
	except EmptyPage:
		students = paginator.page(paginator.num_pages)
	context = {
	'search':search,
	'students':students,
	'page': page,
	}
	return render(request, 'students.html', context)

@login_required(login_url='', redirect_field_name='next')
def examinations(request):
	exams = Course.objects.all().order_by('-pk')
	context ={
	'exams': exams,
	}
	return render(request, 'exams.html', context)

@login_required(login_url='', redirect_field_name='next')
def examination(request, id):
	courses = Course.objects.all().order_by('-pk')
	course = courses.filter(id=id).first()
	students= StudentDetails.objects.filter(exams__course=course)
	if (request.method == 'POST'):
		search = request.POST.get('search',None)
		if(search != None):
			return_url = return_url = reverse('user:examSearch', args=[id, search])
			return redirect(return_url)
	paginator = Paginator(students, 20)
	page = request.GET.get('page')
	try:
		students = paginator.page(page)
	except PageNotAnInteger:
		students = paginator.page(1)
	except EmptyPage:
		students = paginator.page(paginator.num_pages)
	context ={
	'course': course,
	'students':students,
	'page': page,
	}
	return render(request, 'exam.html', context)

@login_required(login_url='', redirect_field_name='next')
def examinationSearch(request, id, search):
	courses = Course.objects.all()
	course = courses.filter(id=id).first()
	students= StudentDetails.objects.filter(exams__course=course, name__contains=search)
	if (request.method == 'POST'):
		rsearch = request.POST.get('search',None)
		if(rsearch != None):
			return_url = return_url = reverse('user:examSearch', args=[id, rsearch])
			return redirect(return_url)
	paginator = Paginator(students, 20)
	page = request.GET.get('page')
	try:
		students = paginator.page(page)
	except PageNotAnInteger:
		students = paginator.page(1)
	except EmptyPage:
		students = paginator.page(paginator.num_pages)
	context ={
	'course': course,
	'students':students,
	'page': page,
	}
	return render(request, 'exam.html', context)

@login_required(login_url='', redirect_field_name='next')
def paper(request, course_id, id):
	try:
		paper = Examination.objects.filter(id=id).first()
		course = Course.objects.filter(id=course_id).first()
		student = StudentDetails.objects.filter(exams__id=paper.id).first()
	except AttributeError:
		return redirect('user:exams')
	context = {
	'exam':paper,
	'course':course,
	'student':student,
	}
	return render(request, 'paper.html', context)

@login_required(login_url='', redirect_field_name='next')
def deleteexam(request, course_id, id):
	exam = Examination.objects.filter(id=id).first()
	try:
		exam.delete()
	except AttributeError:
		pass
	return_url = return_url = reverse('user:exam', args=[course_id])
	return redirect(return_url)

def not_found(request):
	return HttpResponse('Not Found!')